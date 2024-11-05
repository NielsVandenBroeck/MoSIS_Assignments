#!/usr/bin/python3
# This file was automatically generated from drawio2cbd with the command:
#   DrawioConvert/__main__.py -F CBD -e g_function -sSrgv ./DrawioFiles/g_Function.drawio -E delta=1 -d ./DrawioFiles/generated/ -f

from g_Function import *
from pyCBD.simulator import Simulator

DELTA_T = 1

cbd = g_function("g_function")

# Run the Simulation
sim = Simulator(cbd)
sim.setDeltaT(DELTA_T)
sim.run(10)

# TODO: Process Your Simulation Results