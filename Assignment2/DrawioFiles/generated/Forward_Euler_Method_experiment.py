#!/usr/bin/python3
# This file was automatically generated from drawio2cbd with the command:
#   DrawioConvert/__main__.py -F CBD -e forward_euler_method -sSrgv ./DrawioFiles/Forward_Euler_Method.drawio -E delta=1 -d ./DrawioFiles/generated/ -f

from Forward_Euler_Method import *
from pyCBD.simulator import Simulator

DELTA_T = 1

cbd = forward_euler_method("forward_euler_method")

# Run the Simulation
sim = Simulator(cbd)
sim.setDeltaT(DELTA_T)
sim.run(10)

# TODO: Process Your Simulation Results