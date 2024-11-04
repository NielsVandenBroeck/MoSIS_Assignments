#!/usr/bin/python3
# This file was automatically generated from drawio2cbd with the command:
#   __main__.py -F CBD -e Clock_item -sSrgv -f UntitledDiagram3.drawio -E delta=0.1 -v

from UntitledDiagram3 import *
from pyCBD.simulator import Simulator

DELTA_T = 0.1

cbd = Clock_item("Clock_item")

# Run the Simulation
sim = Simulator(cbd)
sim.setDeltaT(DELTA_T)
sim.run(10)

print(cbd.getSignals())
# TODO: Process Your Simulation Results