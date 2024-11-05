#!/usr/bin/python3
# This file was automatically generated from drawio2cbd with the command:
#   DrawioConvert/__main__.py -F CBD -e g_function -sSrgv ./DrawioFiles/g_Function.drawio -E delta=1 -d ./DrawioFiles/generated/ -f

from pyCBD.Core import *
from pyCBD.lib.std import *

DELTA_T = 1

class g_function(CBD):
    def __init__(self, block_name):
        super().__init__(block_name, input_ports=['T'], output_ports=['OUT1'])

        # Create the Blocks
        self.addBlock(ConstantBlock("Y8TdmIJsYqVKhBDNhRFt-43", value=(2)))
        self.addBlock(ConstantBlock("Y8TdmIJsYqVKhBDNhRFt-45", value=(3)))
        self.addBlock(AdderBlock("Y8TdmIJsYqVKhBDNhRFt-47", numberOfInputs=(2)))
        self.addBlock(AdderBlock("Y8TdmIJsYqVKhBDNhRFt-52", numberOfInputs=(2)))
        self.addBlock(PowerBlock("Y8TdmIJsYqVKhBDNhRFt-57"))
        self.addBlock(InverterBlock("Y8TdmIJsYqVKhBDNhRFt-63"))
        self.addBlock(ProductBlock("Y8TdmIJsYqVKhBDNhRFt-67", numberOfInputs=(2)))

        # Create the Connections
        self.addConnection("T", "Y8TdmIJsYqVKhBDNhRFt-47", input_port_name='IN2')
        self.addConnection("T", "Y8TdmIJsYqVKhBDNhRFt-52", input_port_name='IN1')
        self.addConnection("Y8TdmIJsYqVKhBDNhRFt-43", "Y8TdmIJsYqVKhBDNhRFt-47", output_port_name='OUT1', input_port_name='IN1')
        self.addConnection("Y8TdmIJsYqVKhBDNhRFt-43", "Y8TdmIJsYqVKhBDNhRFt-57", output_port_name='OUT1', input_port_name='IN2')
        self.addConnection("Y8TdmIJsYqVKhBDNhRFt-45", "Y8TdmIJsYqVKhBDNhRFt-52", output_port_name='OUT1', input_port_name='IN2')
        self.addConnection("Y8TdmIJsYqVKhBDNhRFt-57", "Y8TdmIJsYqVKhBDNhRFt-63", output_port_name='OUT1', input_port_name='IN1')
        self.addConnection("Y8TdmIJsYqVKhBDNhRFt-67", "OUT1", output_port_name='OUT1')
        self.addConnection("Y8TdmIJsYqVKhBDNhRFt-63", "Y8TdmIJsYqVKhBDNhRFt-67", output_port_name='OUT1', input_port_name='IN2')
        self.addConnection("Y8TdmIJsYqVKhBDNhRFt-47", "Y8TdmIJsYqVKhBDNhRFt-67", output_port_name='OUT1', input_port_name='IN1')
        self.addConnection("Y8TdmIJsYqVKhBDNhRFt-52", "Y8TdmIJsYqVKhBDNhRFt-57", output_port_name='OUT1', input_port_name='IN1')


