#!/usr/bin/python3
# This file was automatically generated from drawio2cbd with the command:
#   DrawioConvert/__main__.py -F CBD -e g_function_2 -sSrgv ./DrawioFiles/g_Function_2.drawio -E delta=1 -d ./DrawioFiles/generated/ -f

from pyCBD.Core import *
from pyCBD.lib.std import *

DELTA_T = 1

class g_function_2(CBD):
    def __init__(self, block_name):
        super().__init__(block_name, input_ports=['T'], output_ports=['OUT1'])

        # Create the Blocks
        self.addBlock(PowerBlock("Y8TdmIJsYqVKhBDNhRFt-57"))
        self.addBlock(InverterBlock("Y8TdmIJsYqVKhBDNhRFt-63"))
        self.addBlock(InverterBlock("eiDzP09to_GWzpRDzbbx-3"))
        self.addBlock(ConstantBlock("eiDzP09to_GWzpRDzbbx-9", value=(2)))
        self.addBlock(ProductBlock("eiDzP09to_GWzpRDzbbx-13", numberOfInputs=(2)))
        self.addBlock(ConstantBlock("eiDzP09to_GWzpRDzbbx-18", value=(-1)))
        self.addBlock(AdderBlock("eiDzP09to_GWzpRDzbbx-21", numberOfInputs=(2)))
        self.addBlock(ConstantBlock("eiDzP09to_GWzpRDzbbx-28", value=(3)))
        self.addBlock(AdderBlock("eiDzP09to_GWzpRDzbbx-30", numberOfInputs=(2)))

        # Create the Connections
        self.addConnection("T", "eiDzP09to_GWzpRDzbbx-30", input_port_name='IN2')
        self.addConnection("eiDzP09to_GWzpRDzbbx-9", "Y8TdmIJsYqVKhBDNhRFt-57", output_port_name='OUT1', input_port_name='IN2')
        self.addConnection("Y8TdmIJsYqVKhBDNhRFt-57", "eiDzP09to_GWzpRDzbbx-3", output_port_name='OUT1', input_port_name='IN1')
        self.addConnection("eiDzP09to_GWzpRDzbbx-3", "eiDzP09to_GWzpRDzbbx-13", output_port_name='OUT1', input_port_name='IN1')
        self.addConnection("eiDzP09to_GWzpRDzbbx-18", "eiDzP09to_GWzpRDzbbx-13", output_port_name='OUT1', input_port_name='IN2')
        self.addConnection("Y8TdmIJsYqVKhBDNhRFt-63", "eiDzP09to_GWzpRDzbbx-21", output_port_name='OUT1', input_port_name='IN1')
        self.addConnection("eiDzP09to_GWzpRDzbbx-13", "eiDzP09to_GWzpRDzbbx-21", output_port_name='OUT1', input_port_name='IN2')
        self.addConnection("eiDzP09to_GWzpRDzbbx-21", "OUT1", output_port_name='OUT1')
        self.addConnection("eiDzP09to_GWzpRDzbbx-28", "eiDzP09to_GWzpRDzbbx-30", output_port_name='OUT1', input_port_name='IN1')
        self.addConnection("eiDzP09to_GWzpRDzbbx-30", "Y8TdmIJsYqVKhBDNhRFt-63", output_port_name='OUT1', input_port_name='IN1')
        self.addConnection("eiDzP09to_GWzpRDzbbx-30", "Y8TdmIJsYqVKhBDNhRFt-57", output_port_name='OUT1', input_port_name='IN1')


