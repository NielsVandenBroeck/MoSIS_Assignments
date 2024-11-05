#!/usr/bin/python3
# This file was automatically generated from drawio2cbd with the command:
#   DrawioConvert/__main__.py -F CBD -e trapezoid_rule -sSrgv ./DrawioFiles/Trapezoid_Rule.drawio -E delta=1 -d ./DrawioFiles/generated/ -f

from Trapezoid_Rule import *
from pyCBD.simulator import Simulator

DELTA_T = 1

cbd = trapezoid_rule("trapezoid_rule")

# Run the Simulation
sim = Simulator(cbd)
sim.setDeltaT(DELTA_T)
sim.run(10)

# TODO: Process Your Simulation Results