#!/usr/bin/python3
# This file was automatically generated from drawio2cbd with the command:
#   __main__.py -F CBD -e Clock_item -sSrgv -f UntitledDiagram3.drawio -E delta=0.1 -v

from pyCBD.Core import *
from pyCBD.lib.std import *

DELTA_T = 0.1

class Clock_item(CBD):
    def __init__(self, block_name):
        super().__init__(block_name, input_ports=[], output_ports=['OUT8'])

        # Create the Blocks
        self.addBlock(TimeBlock("NdaAwexLkHMtAoHr-By2-73"))

        # Create the Connections
        self.addConnection("NdaAwexLkHMtAoHr-By2-73", "OUT8", output_port_name='OUT1')


