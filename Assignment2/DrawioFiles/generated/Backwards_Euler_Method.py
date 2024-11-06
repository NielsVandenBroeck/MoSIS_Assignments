#!/usr/bin/python3
# This file was automatically generated from drawio2cbd with the command:
#   DrawioConvert/__main__.py -F CBD -e backwards_euler_method -sSrgv ./DrawioFiles/Backwards_Euler_Method.drawio -E delta=1 -d ./DrawioFiles/generated/ -f

from pyCBD.Core import *
from pyCBD.lib.std import *

DELTA_T = 1

class backwards_eurler_method(CBD):
    def __init__(self, block_name):
        super().__init__(block_name, input_ports=['IN1', 'IC'], output_ports=['OUT1'])

        # Create the Blocks
        self.addBlock(DelayBlock("A_Bu4HxSgUgRhryUP4xk-6"))
        self.addBlock(DeltaTBlock("A_Bu4HxSgUgRhryUP4xk-10"))
        self.addBlock(ProductBlock("A_Bu4HxSgUgRhryUP4xk-12", numberOfInputs=(2)))
        self.addBlock(AdderBlock("A_Bu4HxSgUgRhryUP4xk-17", numberOfInputs=(2)))
        self.addBlock(DelayBlock("A_Bu4HxSgUgRhryUP4xk-32"))
        self.addBlock(ConstantBlock("zQRr1qEUXGNRx-g26WuO-1", value=(0)))

        # Create the Connections
        self.addConnection("IN1", "A_Bu4HxSgUgRhryUP4xk-12", input_port_name='IN1')
        self.addConnection("A_Bu4HxSgUgRhryUP4xk-10", "A_Bu4HxSgUgRhryUP4xk-12", output_port_name='OUT1', input_port_name='IN2')
        self.addConnection("A_Bu4HxSgUgRhryUP4xk-17", "OUT1", output_port_name='OUT1')
        self.addConnection("A_Bu4HxSgUgRhryUP4xk-17", "A_Bu4HxSgUgRhryUP4xk-6", output_port_name='OUT1', input_port_name='IN1')
        self.addConnection("IC", "A_Bu4HxSgUgRhryUP4xk-32", input_port_name='IC')
        self.addConnection("A_Bu4HxSgUgRhryUP4xk-6", "A_Bu4HxSgUgRhryUP4xk-17", output_port_name='OUT1', input_port_name='IN1')
        self.addConnection("A_Bu4HxSgUgRhryUP4xk-32", "A_Bu4HxSgUgRhryUP4xk-17", output_port_name='OUT1', input_port_name='IN2')
        self.addConnection("A_Bu4HxSgUgRhryUP4xk-12", "A_Bu4HxSgUgRhryUP4xk-32", output_port_name='OUT1', input_port_name='IN1')
        self.addConnection("zQRr1qEUXGNRx-g26WuO-1", "A_Bu4HxSgUgRhryUP4xk-6", output_port_name='OUT1', input_port_name='IC')


