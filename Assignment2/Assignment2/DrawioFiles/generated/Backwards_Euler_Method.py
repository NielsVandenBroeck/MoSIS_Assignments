#!/usr/bin/python3
# This file was automatically generated from drawio2cbd with the command:
#   DrawioConvert/__main__.py -F CBD -e backwards_euler_method -sSrgv ./DrawioFiles/Backwards_Euler_Method.drawio -E delta=1 -d ./DrawioFiles/generated/ -f

from pyCBD.Core import *
from pyCBD.lib.std import *

DELTA_T = 1

class backwards_euler_method(CBD):
    def __init__(self, block_name):
        super().__init__(block_name, input_ports=['IC', 'IN1'], output_ports=['OUT1'])

        # Create the Blocks
        self.addBlock(DelayBlock("VrSbkfLm2oYFl8fiRDUs-7"))
        self.addBlock(DeltaTBlock("VrSbkfLm2oYFl8fiRDUs-11"))
        self.addBlock(ProductBlock("VrSbkfLm2oYFl8fiRDUs-13", numberOfInputs=(2)))
        self.addBlock(AdderBlock("VrSbkfLm2oYFl8fiRDUs-18", numberOfInputs=(2)))
        self.addBlock(DelayBlock("VrSbkfLm2oYFl8fiRDUs-31"))
        self.addBlock(ConstantBlock("VrSbkfLm2oYFl8fiRDUs-38", value=(0)))

        # Create the Connections
        self.addConnection("IN1", "VrSbkfLm2oYFl8fiRDUs-13", input_port_name='IN1')
        self.addConnection("VrSbkfLm2oYFl8fiRDUs-11", "VrSbkfLm2oYFl8fiRDUs-13", output_port_name='OUT1', input_port_name='IN2')
        self.addConnection("VrSbkfLm2oYFl8fiRDUs-18", "OUT1", output_port_name='OUT1')
        self.addConnection("VrSbkfLm2oYFl8fiRDUs-18", "VrSbkfLm2oYFl8fiRDUs-7", output_port_name='OUT1', input_port_name='IN1')
        self.addConnection("IC", "VrSbkfLm2oYFl8fiRDUs-31", input_port_name='IC')
        self.addConnection("VrSbkfLm2oYFl8fiRDUs-7", "VrSbkfLm2oYFl8fiRDUs-18", output_port_name='OUT1', input_port_name='IN1')
        self.addConnection("VrSbkfLm2oYFl8fiRDUs-31", "VrSbkfLm2oYFl8fiRDUs-18", output_port_name='OUT1', input_port_name='IN2')
        self.addConnection("VrSbkfLm2oYFl8fiRDUs-13", "VrSbkfLm2oYFl8fiRDUs-31", output_port_name='OUT1', input_port_name='IN1')
        self.addConnection("VrSbkfLm2oYFl8fiRDUs-38", "VrSbkfLm2oYFl8fiRDUs-7", output_port_name='OUT1', input_port_name='IC')


