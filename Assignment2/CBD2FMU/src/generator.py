"""
A module that allows the creation of the file required for FMUs,
w.r.t. the FMU 2.0 specification.

Note:
	The :code:`DerivatorBlock` will be explicitly converted to Euler's
	backwards formula. Under the assumption that the delta between
	intervals is small enough, this will be sufficient in most cases.


Note:
	The :code:`IntegratorBlock` is marked as derivative for the FMU,
	ensuring that for ModelExchange, this will be solved by the platform
	itself. For CoSimulation, the Forward Euler formula is used. This can
	be done because:

	.. math::
		& OUT1 = \\int IN1\\ dt \\\\
		\\iff & der(OUT1) = IN1


Danger:
	Algebraic loops cannot be solved yet and will therefore throw an
	error when present in a model.


This module has the following requirements:

* `Jinja2 <https://jinja.palletsprojects.com/en/3.0.x/>`_ (code generation)
* `fmpy <https://fmpy.readthedocs.io/en/latest/>`_ (FMU compilation)
* `CBD Simulator` (for extracting model information)

The jinja template files are located in the :code:`templates` folder.
All static files (i.e., files present in all FMUs) can be found in the
:code:`static` folder.
"""
# CBD simulator
from pyCBD.Core import BaseBlock
from pyCBD.scheduling import TopologicalScheduler
from pyCBD.loopsolvers.linearsolver import LinearSolver
from pyCBD.depGraph import createDepGraph
from pyCBD.converters.latexify import CBD2Latex, Time
from pyCBD import naivelog

try:
	from CBD.loopsolvers.sympysolver import SympySolver
	SYMPY_SOLVER_FOUND = True
except ImportError:
	SympySolver = None
	SYMPY_SOLVER_FOUND = False

# FMU generation
from jinja2 import Template
from fmpy.util import compile_platform_binary

import shutil as su
import os, uuid, sys, re
import tempfile

from dataclasses import dataclass
from enum import Enum

@dataclass
class Variable:
	"""
	Identifies a model variable for the FMU.
	Helper/dataclass for containing all important information.

	See Also:
		FMI 2.0 and 3.0 Specification(s), section 2.2.7.

	Attributes:
		index (int):		The variable's 1-based index in the modelDescription.xml
		name (str):			The full, unique name for the variable. Should be mangled to
							still identify the original CBD model in the FMU.
		path (str):         The Variable's path in the CBD model.
		initial (str):		Shows how the variable is to be initialized. Can be :code:`exact`
							(for a predefined initial value), :code:`calculated` (to be computed
							at initialization during runtime) or :code:`approx` if the variable
							is the initial guess for an algebraic loop. For the CBD2FMU generator,
							:code:`approx` is not used. Defaults to :code:`calculated`.
		causality (str):	Either :code:`parameter` (the variable is a model param),
							:code:`calculatedParameter` (for tunable variables), :code:`input`
							(for model input), :code:`output` (for model output), :code:`local`
							(for variables, local to the FMU; i.e. the internal vars) or
							:code:`independent` (to identify the time variable).
							For the CBD2FMU generator, :code:`calculatedParameter` and
							:code:`independent` are not used. Defaults to :code:`local`.
		variability (str):	Identifies the variable dependency. Is one of :code:`constant` (for
							never-changing values), :code:`fixed` (when constant after
							initialization), :code:`tunable` (when constant between external
							events), :code:`discrete` (constant between events) or
							:code:`continuous` (no ristrictions). For CBDs, all signals are
							:code:`continuous`, except for values from a :code:`ConstantBlock`,
							which are :code:`constant`. Defaults to :code:`continuous`.
		start (float):		Starting value for the variable. Only to be set when :code:`initial`
							is :code:`exact` (for CBDs).
		derivative (int):	If this variable is the derivative of another variable X, this field
							must be X's derivative.
		wbd (bool):         Short for 'will be derived'. When :code:`True`, another variable will
							refer hereto as a derivative. This prevents the variable from being
							hidden.
		visible (bool):     When :code:`True`, this variable is exposed in the modelDescription.xml.
	"""
	index: int
	name: str
	path: str
	initial: str = "calculated"
	causality: str = "local"
	variability: str = "continuous"
	start: float = None
	derivative: int = None
	wbd: bool = False
	visible: bool = True

	def replace(self, a, b):
		"""
		Replaces :code:`a` with :code:`b` in the variable's name.
		Wrapper function around :code:`self.name.replace(a, b)`.
		"""
		self.name.replace(a, b)
		return self

	def __hash__(self):
		return self.index


class FMUInterface:
	"""
	FMU mode to generate for.
	This is either :code:`ModelExchange`, :code:`CoSimulation` or both.
	Take a look at the FMU Specification to find the differences and
	usages of these modes.

	While FMU 3.0 is also allowed, the Scheduled Execution target is
	not part of this generation module.
	"""
	ModelExchange = 0b01
	CoSimulation = 0b10
	BOTH = 0b11


class SolverType(Enum):
	"""
	Helper class to select which solver to use for algebraic equations.
	"""
	LINEAR = 0
	SYMPY = 1


@dataclass
class ExperimentSetup:
	"""
	Helper dataclass to setup the default FMU experiment used.

	Attributes:
		start (float):		Starting time of the experiment.
		end (float):		Ending time of the experiment.
		tolerance (float):	The tolerance for adaptive step-size.
		delta (float):		The initial or fixed delta to use as time-steps.
	"""
	start: float = 0.0
	end: float = 3.0
	tolerance: float = 1e-6
	delta: float = 0.01


class Generator:
	"""
	Main generation class. Generates all files for the FMU.

	Note:
		This class does **not** change the original model.

	Warning:
		This class only works if the dependency graph is fixed
		after the first iteration. I.e., iteration 0 can be
		different, but all others must be the same.

	Args:
		model (CBD):		CBD model that needs to be converted to an FMU.
		model_name (str):	The model identifier / FMU class name. Defaults to the model root's
							block name.
		file_name (str):	The name of the FMU file to generate, including the :code:`.fmu` extension.
							Defaults to the :attr:`model_name`, followed with :code:`.fmu`.
		fmu_version (int):  FMU version to generate for. Must be 2 or 3. FMU 3.0 is currently still in
							beta and thus subject to change.
		mode (FMUInterface):		    The mode of the FMU. Implies the environment in which it must be
							active.
							Defaults to both :code:`ModelExchange` and :code:`CoSimulation`.
		solver_type (SolverType):		Method for solving algebraic loops. Defaults to symbolic solving
							(using sympy), but can also be changed to linear (Gauss-Jordan) solving.
		experiment (ExperimentSetup):	The default experiment to use when loading the FMU in another
							tool. This is only an example experiment setup, providing information to
							a user about the main usage context (or validity frame) of the FMU. This
							information will not be used for anything else. It is up to the user to
							ensure this FMU is used as intended.
		description (str):	A short model description. Defaults to the empty string.
		c_only (bool):      When set, only C-code is generated, which can be compiled using
							:code:`gcc model.c lsolve.c -lm`. The files are generated in a sub-folder
							called :code:`gen`.
		hide (iter):		An iterable of variable name (block path with :code:`_` as separator)
							patterns to hide from the FMU. This will make them invisible for FMU
							simulators. A :code:`*` acts as a wildcard. When :code:`None`, no variables
							are hidden. Note that input ports, output ports, derivatives and derivative
							references cannot be hidden. Defaults to :code:`None`.
		keep (iter):		An iterable of variable name (block path with :code:`_` as separator)
							patterns to show in the FMU. This will exclude them from the patterns set in
							:attr:`hide`. A :code:`*` acts as a wildcard. When :code:`None`, no variables
							are excluded. Defaults to :code:`None`.
	"""
	def __init__(self, model, model_name=None, file_name=None, fmu_version=2, mode=FMUInterface.BOTH,
	             solver_type=SolverType.SYMPY, experiment=ExperimentSetup(), description="",
	             c_only=False, hide=None, keep=None):
		assert fmu_version in [2, 3], "Can only generate FMUs with version 2 or 3."
		self.model = model.clone()
		self.model.flatten(ignore=["IntegratorBlock", "Clock"])
		self.ori_names = {}

		# remove all non-alphanumeric symbols; but keep links for in FMU
		for block in self.get_blocks():
			ori_name = block.getBlockName()
			ori_path = block.getPath()
			new_name = re.sub("[^a-zA-Z0-9_]", "_", ori_name)
			block.setBlockName(new_name)
			self.ori_names[block.getPath('_')] = ori_path

		self.data = {}
		self.data["model_name"] = model_name or self.model.getBlockName()
		self.data["file_name"] = file_name or (self.data["model_name"] + ".fmu")
		self.data["mode"] = mode
		self.data["experiment"] = experiment
		self.data["description"] = description
		self.data["guid"] = str(uuid.uuid4())
		self.data["c_only"] = c_only
		if c_only:
			# C-code is based on FMU 2.0, so enforce this!
			self.data["fmu_version"] = 2
		else:
			self.data["fmu_version"] = fmu_version

		for block in self.model.getBlocks():
			block.setBlockName(block.getBlockName().replace("-", "_"))
		self.scheduler = TopologicalScheduler()

		self.solver_type = solver_type
		if solver_type == SolverType.LINEAR and not SYMPY_SOLVER_FOUND:
			self.solver = LinearSolver(naivelog.logger)
		elif SYMPY_SOLVER_FOUND and solver_type == SolverType.SYMPY:
			self.solver = SympySolver(naivelog.logger)

		self.hide_patterns = hide or []
		self.keep_patterns = keep or ['*']

	def get_blocks(self):
		"""
		Gets all the blocks from the flattened model.
		"""
		return self.model.getBlocks()

	def get_order(self, curIt):
		"""
		Gets the topological order of the blocks at a specific iteration.

		Args:
			curIt (int): The iteration to get the order at.
		"""
		depGraph = createDepGraph(self.model, curIt, True)
		for block in self.model.getBlocks():
			deps = block.getDependencies(curIt)
			if curIt == 0:
				if block.getBlockType() == "IntegratorBlock":
					pass # TODO: what was it that I wanted to do here?
					# depGraph.unsetDependency(block, block.getPortConnectedToInput("IN1").block)
			else:
				for d in deps:
					if d.block.getBlockType() == "IntegratorBlock":
						depGraph.unsetDependency(block, d.block)
		return self.scheduler.schedule(depGraph, curIt, 0.0)

	def obtain_eqs_from_order(self, order, curIt):
		"""
		Given the order in which the blocks must be executed,
		this function will use the :class:`CBD2Latex` class to
		construct the C-representation for the functions.

		Args:
			order:		  List of components, topologically ordered.
			curIt (int):	The current iteration.

		Returns:
			A list of tuples like :code:`[([LHS, ...], RHS), ...]`;
			where the :code:`LHS` identifies an ordered list of
			left-hand sides (when there are multiple, it means an
			algebraic loop); and :code:`RHS` the string-representation
			of the results.
		"""
		conf = {
			"path_sep": '_',
			"ignore_path": False,
			"escape_nonlatex": False,
			"time_format": "",
			"path_prefix": "_",
			"ignore": ["IntegratorBlock", "DerivatorBlock"]
		}
		ltx = CBD2Latex(self.model, **conf)
		eqs = [x for x in ltx.eq(Time(0, curIt == "i")).split("\n")]
		if eqs[-1] == '':
			eqs.pop()
		res_order = []
		# reverse the order to allow scheduling at end as well
		for c in reversed(order):
			c_order = []
			if len(c) == 1:  # NO ALGEBRAIC LOOP
				block = c[0]
				if isinstance(block, Port): continue

				# Assumes no special blocks that change the deps exist
				deps = [x.block for x in block.getDependencies(1 if curIt == "i" else curIt)]
				path = '_' + block.getPath("_")

				for out in block.getOutputPortNames():
					if block.getBlockType() == "WireBlock": continue
					if block.getBlockType() == "IntegratorBlock" and curIt == "i": continue
					p = path + "_" + out
					if block.getBlockType() == "DelayBlock" and len(deps) == 0:
						# CBD2Latex is always ordered, so second equation for delay is it > 0
						for e in reversed(eqs):
							if e.startswith(p):
								c_order.insert(0, e)
								break
					elif block.getBlockType() == "DerivatorBlock":
						# NOTE: This code is mainly here for backwards compatibility,
						#       currently, the DerivatorBlocks will also be flattened,
						#       which implies that the following formula will be applied
						#       either way. While this is a variable overhead, it does
						#       not take away from the FMU efficiency.
						#
						# In order to use backwards euler, the previous input must be stored
						# Otherwise, the created equations will override this value
						c_order.insert(0, "%s_IN1_prev = %s_IN1" % (path, path))

						if curIt == "i":
							# Apply a backwards euler for the derivator
							c_order.insert(0, "{p}_OUT1 = ({p}_IN1 - {p}_IN1_prev) / delta".format(p=path))
						else:
							c_order.insert(0, "%s_OUT1 = %s_IC" % (path, path))
					elif block.getBlockType() == "TimeBlock":
						if out == "relative":
							c_order.insert(0, "%s = cbd->time - %s" % (p, str(self.data["experiment"].start)))
						else:
							c_order.insert(0, "%s = cbd->time" % p)
					elif block.getBlockType() in ["Clock", "DummyClock"]:
						# Clock Usage Assumption: Clock should be replaced by internal Clock wlog
						# It is up to the user to correctly use the Clock in the model.
						if out == "time":
							c_order.insert(0, "%s = cbd->time" % p)
						elif out == "rel_time":
							c_order.insert(0, "%s = cbd->time - %s" % (p, str(self.data["experiment"].start)))
						elif out == "delta":
							c_order.insert(0, "%s = delta" % p)
					elif block.getBlockType() == "DeltaTBlock":
						c_order.insert(0, "%s = delta" % p)
					elif block.getBlockType() == "InverterBlock":
						c_order.insert(0, "%s = 1.0/%s_IN1" % (p, path))
					else:
						for e in eqs:
							if e.startswith(p):
								c_order.insert(0, e)
								break
				for inp in block.getInputPortNames():
					if block.getBlockType() in ["WireBlock", "OutputPortBlock"]: continue
					# Backwards compatibility: delta_t is not a port anymore
					if block.getBlockType() in ["IntegratorBlock", "DerivatorBlock"] and inp == "delta_t": continue
					p = path + "_" + inp
					bcti = block.getPortConnectedToInput(inp).block
					in_deps = bcti in deps

					tae = ""
					if bcti.getBlockType() in ["InputPortBlock", "WireBlock"]:
						tae = "%s = _%s" % (p, bcti.getPath("_"))
					else:
						for e in eqs:
							if e.startswith(p):
								tae = e
								break
					if curIt == 0 and block.getBlockType() == "IntegratorBlock":
						if inp == "IN1":
							# At it 0, the integrator only outputs its IC, so the IN1 can be deferred
							# This also ensures that integrator loops are solved correctly
							res_order.append(tae)
						else:
							c_order.insert(0, tae)
					elif curIt == "i" and block.getBlockType() == "DelayBlock" and inp in ["IN1", "IC"]:
						# Do not update delay before new values of delay are computed
						res_order.append(tae)
					elif in_deps:
						c_order.insert(0, tae)
					else:
						c_order.append(tae)
				if block.getBlockType() in ["WireBlock", "InputPortBlock", "OutputPortBlock"]:
					b, p = block.getBlockConnectedToInput("IN1")
					if b.getBlockType() in ["OutputPortBlock", "WireBlock"]:
						c_order.append("%s = _%s" % (path, b.getPath('_')))
					else:
						c_order.append("%s = _%s_%s" % (path, b.getPath('_'), p))
			else:  # ALGEBRAIC LOOP!
				self.solver.checkValidity(self.model.getPath("."), c)
				if self.solver_type == SolverType.LINEAR:
					other = []
					known = {}
					for block in c:
						path = "_" + block.getPath("_")
						for inp, b in block.getLinksIn().items():
							var = path + "_" + inp
							prev = block.getBlockConnectedToInput(inp).block
							for e in eqs:
								if e.startswith(var):
									if prev not in c:
										c_order.insert(0, e)
										known[var[1:]] = var

						for inp in block.getInputPortNames():
							var = path + "_" + inp
							if var in known: continue
							for e in eqs:
								if e.startswith(var):
									other.insert(0, e)
									break

					# Get matrix representation
					m1, m2 = self.solver.get_matrix(c, '_', known)
					mat = m1.concat(m2)

					deps = {}
					for b in c:
						D = [b.getBlockConnectedToInput(x) for x in b.getInputPortNames()]
						deps[b] = [b.block.getPath('_') + '_' + b.output_port for b in D if b.block in c]

					if mat.rows == 1:
						# TODO: fix this?
						raise NotImplementedError("Suspected singular matrix. However, currently cannot find an example "
												  "that enters this branch. Please contact the repository owner with this "
												  "error and all associated files.")
						# nc = ([deps[c[mat[0].index(1)]]], mat[0][-1])
						# print("NC:", nc)
					else:
						dlist = []
						for b in c:
							for d in deps[b]:
								if d not in dlist:
									dlist.append(d)
						sm = "{" + mat.format(', ', '{}', "%f", ', ').replace("{,", "{").replace(", }", " }") + "}"
						nc = (dlist, sm)

					c_order.append(nc)
					c_order += other
				elif self.solver_type == SolverType.SYMPY:
					solution, sol = self.solver.getComponentCache(c)
					resp = solution.args[0].subs({x: "_%s" % x for x in solution.free_symbols})
					for i, eq in enumerate(resp):
						c_order.insert(0, "_%s = %s" % (sol[i], eq))
					print(resp)
			res_order = c_order + res_order
		for port in self.model.getOutputPorts():
			tpath = '_%s_%s' % (port.block.getPath("_"), port.name)
			source = port.getIncoming().source
			spath = '_%s_%s' % (source.block.getPath("_"), source.name)
			res_order.append("%s = %s" % (tpath, spath))
		return res_order

	def obtain_var_info(self):
		"""
		Creates the structures used mainly for the modelDescription.xml,
		using the :class:`Variable` class. All input and output ports of each
		block have their own :code:`local` variables. The main inputs/outputs
		are marked as such. For the :code:`IntegratorBlock`, the output is marked
		as the input's derivative.

		Returns:
			A tuple of the variables, the outputs, the derivatives and the unknown
			initials.
		"""
		variables = []

		def must_hide(vname, can_hide=True):
			if not can_hide:
				print("WARNING: Could not hide '%s', as it is required to be visible in FMU." % vname, file=sys.stderr)
				return False
			for keep in self.keep_patterns:
				keep = keep.replace(".", r"\.").replace('*', '.*')
				if re.fullmatch(keep, vname):
					return False
			for ignore in self.hide_patterns:
				ignore = ignore.replace(".", r"\.").replace('*', '.*')
				if re.fullmatch(ignore, vname):
					return True
			return False

		def add_var(block, port=None, **kwargs):
			cidx = len([v for v in variables if v.visible]) + 1
			name = block.getPath('_')
			path = self.ori_names.get(name, name)
			if port is not None and port != "":
				name += '_' + port
				path += '.' + port
			var = Variable(cidx, name, path, **kwargs)
			ch = var.causality in ["output", "input"] or var.derivative is not None or var.wbd
			if must_hide(path, not ch):
				var.visible = False
				var.index = -1
			variables.append(var)
			return var

		for port in self.model.getInputPorts():
			add_var(port.block, port.name, start=0, initial=None, causality="input")
		for port in self.model.getOutputPorts():
			add_var(port.block, port.name, causality="output")
		for block in self.get_blocks():
			if block.getBlockType() == "OutputPortBlock":
				add_var(block, causality="output")
			elif block.getBlockType() == "InputPortBlock":
				add_var(block, causality="input")
			elif block.getBlockType() == "WireBlock":
				add_var(block)
			elif block.getBlockType() == "ConstantBlock":
				add_var(block, "OUT1", initial="exact", start=block.getValue(), variability="constant")
			elif block.getBlockType() == "IntegratorBlock":
				add_var(block, "IC")
				var_in = add_var(block, "IN1", wbd=True)
				add_var(block, "OUT1", derivative=var_in.index)
			elif block.getBlockType() == "DerivatorBlock":
				add_var(block, "IC")
				add_var(block, "IN1")
				add_var(block, "OUT1")
				add_var(block, "IN1_prev", visible=False)
			else:
				for port in block.getInputPortNames():
					add_var(block, port)
				for port in block.getOutputPortNames():
					add_var(block, port)
		variables = [v.replace("-", "_") for v in variables]

		outputs = [v for v in variables if v.causality == "output"]
		ders = [v for v in variables if v.derivative is not None]
		drefs = [v for v in variables for d in ders if v.index == d.derivative]
		initials = list(set(outputs) | set(ders) | set(drefs))

		return variables, outputs, ders, initials

	def generate_file(self, tmp, which, eqs0, eqs, vinf):
		"""
		Generates the a file for the FMU, based on the templates.

		Args:
			tmp (str):  	Temporary path to create the files at.
			which (str):	The type to generate. Must be one of :code:`source`,
							:code:`header` or :code:`model`.
			eqs0 (list):	Equations at time 0.
			eqs (list):		Equations at time i.
			vinf (tuple):	Result of the :meth:`obtain_var_info` call.
		"""
		if which == "source":
			fname = "model.c"
			tname = fname
		elif which == "header":
			fname = "model.h"
			if self.data["c_only"]:
				fname = "code.h"
			tname = fname
		elif which == "model":
			fname = "modelDescription{v}.xml".format(v=self.data["fmu_version"])
			tname = "modelDescription.xml"
		elif which == "build":
			fname = "buildDescription.xml"
			tname = fname
		elif which == "version":
			fname = "version.h"
			tname = fname
		else:
			raise NotImplementedError("Unknown file template requested.")

		path = os.path.dirname(os.path.realpath(__file__))
		tpath = os.path.realpath(tmp)
		filename = os.path.join(path, "templates/%s" % fname)
		with open(filename, 'r') as file:
			template = Template(file.read(), trim_blocks=True, lstrip_blocks=True)

		variables, outputs, ders, initials = vinf

		contents = template.render(model=self.data,
									equations0=eqs0,
									equations=eqs,
									outputs=outputs,
									derivatives=ders,
									initials=initials,
									variables = variables)

		with open(os.path.join(tpath, tname), 'w') as file:
			file.write(contents)

	def generate_fmu(self):
		"""
		Generates the FMU in a temporary directory, compresses the
		files and copies it to the current location.
		"""
		path = os.path.dirname(os.path.realpath(__file__))

		# create temp directory
		if self.data["c_only"]:
			sdir = "gen"
		else:
			tdir = tempfile.TemporaryDirectory()
			sdir = os.path.join(tdir.name, "sources")
		if not os.path.isdir(sdir):
			os.mkdir(sdir)
		else:
			for file in os.listdir(sdir):
				os.remove(os.path.join(sdir, file))

		# Obtain the data
		comp0 = self.get_order(0)
		comp = self.get_order(1)
		eqs0 = self.obtain_eqs_from_order(comp0, 0)
		eqs = self.obtain_eqs_from_order(comp, "i")
		vinf = self.obtain_var_info()

		# Write the modelDescription.xml
		if not self.data["c_only"]:
			gen.generate_file(tdir.name, "model", eqs0, eqs, vinf)

		# Write the model sources
		gen.generate_file(sdir, "version", eqs0, eqs, vinf)
		gen.generate_file(sdir, "header", eqs0, eqs, vinf)
		gen.generate_file(sdir, "source", eqs0, eqs, vinf)
		if self.data["fmu_version"] > 2:
			gen.generate_file(sdir, "build", eqs0, eqs, vinf)

		for file in os.listdir(os.path.join(path, "static")):
			if os.path.isfile(os.path.join(sdir, file)): continue
			if not (file.endswith(".h") or file.endswith(".c")): continue
			if not self.data["c_only"]:
				if file == "fmiFunctions{v}.c".format(v=self.data["fmu_version"]):
					su.copyfile(os.path.join(path, "static", file), os.path.join(sdir, "fmiFunctions.c"))
				elif not file.startswith("fmiFunctions"):
					su.copyfile(os.path.join(path, "static", file), os.path.join(sdir, file))
			else:
				if file in ["all.c", "fmiFunctions2.c", "fmiFunctions3.c"]:
					continue
				su.copyfile(os.path.join(path, "static", file), os.path.join(sdir, file))

		# Compress temp directory
		if not self.data["c_only"]:
			fname = su.make_archive(self.data["file_name"], "zip", tdir.name)
			su.move(fname, os.path.join(".", self.data["file_name"]))

			tdir.cleanup()

	def compile_fmu(self):
		"""
		Compiles the generated FMU, using :code:`fmpy`.
		"""
		if self.data["c_only"]:
			# TODO: Fix this
			print("WARNING: Cannot compile C-code. Use 'gcc model.c lsolve.c -lm'.", file=sys.stderr)
		else:
			fmu = os.path.join(".", self.data["file_name"])
			if os.path.isfile(fmu):
				compile_platform_binary(fmu)


if __name__ == '__main__':
	from pyCBD.Core import *
	from pyCBD.lib.std import *
	from DrawioFiles.generated.PID_controller import *

	class BouncingBall(CBD):
		def __init__(self):
			CBD.__init__(self, "BouncingBall", [], ["vout", "hout"])
			self.addBlock(ConstantBlock("g", -9.81))
			self.addBlock(ConstantBlock("v0", 0.0))
			self.addBlock(ConstantBlock("h0", 1.0))
			# self.addBlock(ConstantBlock("dt", 0.1))
			self.addBlock(IntegratorBlock("v"))
			self.addBlock(IntegratorBlock("h"))
			self.addBlock(DelayBlock("delay"))

			self.addConnection("g", "v")
			self.addConnection("v", "h")
			self.addConnection("v", "vout")
			self.addConnection("h", "hout")
			self.addConnection("h", "delay")
			self.addConnection("v0", "v", input_port_name="IC")
			self.addConnection("h0", "h", input_port_name="IC")
			self.addConnection("h0", "delay", input_port_name="IC")
			# self.addConnection("dt", "v", input_port_name="delta_t")
			# self.addConnection("dt", "h", input_port_name="delta_t")

	class SinGen(CBD):
		def __init__(self):
			CBD.__init__(self, "SinGen", [], ["OUT1"])
			self.addBlock(TimeBlock("time"))
			self.addBlock(GenericBlock("sin", "sin"))
			#self.addBlock(DerivatorBlock("der"))

			self.addConnection("time", "sin")
			self.addConnection("sin", "OUT1")
			#self.addConnection("sin", "der")
			# NOTE: this should actually be '1', instead of 0, as der(sin(t)) = cos(t)
			#self.addConnection("time", "der", input_port_name="IC")
			# self.addConnection("time", "der", input_port_name="delta_t")
			#self.addConnection("der", "OUT2")

	class Loop(CBD):
		def __init__(self):
			CBD.__init__(self, "Loop", [], ["x", "y"])
			self.addBlock(ConstantBlock("two", 2))
			self.addBlock(ConstantBlock("five", 5))
			self.addBlock(AdderBlock("sum"))
			self.addBlock(IntegratorBlock("int"))

			self.addConnection("two", "sum")
			self.addConnection("int", "sum")
			self.addConnection("five", "int", input_port_name="IC")
			self.addConnection("sum", "int")
			self.addConnection("sum", "y")
			self.addConnection("int", "x")

	class Oscillator(CBD):
		def __init__(self):
			CBD.__init__(self, "Oscillator", [], ["x"])
			self.addBlock(ConstantBlock("zero", 0))
			self.addBlock(ConstantBlock("one", 1))
			self.addBlock(NegatorBlock("neg"))
			self.addBlock(IntegratorBlock("int1"))
			self.addBlock(IntegratorBlock("int2"))

			self.addConnection("one", "int1", input_port_name="IC")
			self.addConnection("zero", "int2", input_port_name="IC")
			self.addConnection("int2", "neg")
			self.addConnection("neg", "int1")
			self.addConnection("int1", "int2")
			self.addConnection("int2", "x")

	class Double(CBD):
		def __init__(self):
			CBD.__init__(self, "Double", ["single"], ["double"])
			self.addBlock(ConstantBlock("two", 2))
			self.addBlock(ProductBlock("mult"))

			self.addConnection("two", "mult")
			self.addConnection("single", "mult")
			self.addConnection("mult", "double")


	model = PID_controller("PID_controller")
	model.flatten(psep="_")
	# model = AddOneBlock("A1")

	gen = Generator(model, experiment=ExperimentSetup(end=4, delta=1e-3), hide=None, fmu_version=2,)
	#gen = Generator(model, experiment=ExperimentSetup(end=40, delta=0.001), fmu_version=2, hide=None, keep=["neg.OUT*"])
	gen.generate_fmu()
	gen.compile_fmu()
