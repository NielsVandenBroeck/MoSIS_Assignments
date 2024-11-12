#!/usr/bin/python3
# This file was automatically generated from drawio2cbd with the command:
#   DrawioConvert/__main__.py -F CBD -e trapezoid_rule -sSrgv ./DrawioFiles/Trapezoid_Rule.drawio -E delta=1 -d ./DrawioFiles/generated/ -f

from pyCBD.Core import *
from pyCBD.lib.std import *

DELTA_T = 1

class trapezoid_rule(CBD):
    def __init__(self, block_name):
        super().__init__(block_name, input_ports=['IN1', 'IC'], output_ports=['OUT1'])

        # Create the Blocks
        self.addBlock(DeltaTBlock("_Kh1ClBUE4M_aFZzjY7V-70"))
        self.addBlock(ProductBlock("_Kh1ClBUE4M_aFZzjY7V-72", numberOfInputs=(2)))
        self.addBlock(DelayBlock("_Kh1ClBUE4M_aFZzjY7V-82"))
        self.addBlock(AdderBlock("_Kh1ClBUE4M_aFZzjY7V-86", numberOfInputs=(2)))
        self.addBlock(ProductBlock("_Kh1ClBUE4M_aFZzjY7V-91", numberOfInputs=(2)))
        self.addBlock(ConstantBlock("_Kh1ClBUE4M_aFZzjY7V-97", value=(0.5)))
        self.addBlock(AdderBlock("_Kh1ClBUE4M_aFZzjY7V-100", numberOfInputs=(2)))
        self.addBlock(DelayBlock("_Kh1ClBUE4M_aFZzjY7V-105"))
        self.addBlock(NegatorBlock("_Kh1ClBUE4M_aFZzjY7V-112"))
        self.addBlock(AdderBlock("_Kh1ClBUE4M_aFZzjY7V-115", numberOfInputs=(2)))

        # Create the Connections
        self.addConnection("IN1", "_Kh1ClBUE4M_aFZzjY7V-82", input_port_name='IN1')
        self.addConnection("IN1", "_Kh1ClBUE4M_aFZzjY7V-86", input_port_name='IN2')
        self.addConnection("_Kh1ClBUE4M_aFZzjY7V-70", "_Kh1ClBUE4M_aFZzjY7V-72", output_port_name='OUT1', input_port_name='IN2')
        self.addConnection("IC", "_Kh1ClBUE4M_aFZzjY7V-82", input_port_name='IC')
        self.addConnection("IC", "_Kh1ClBUE4M_aFZzjY7V-115", input_port_name='IN2')
        self.addConnection("_Kh1ClBUE4M_aFZzjY7V-82", "_Kh1ClBUE4M_aFZzjY7V-86", output_port_name='OUT1', input_port_name='IN1')
        self.addConnection("_Kh1ClBUE4M_aFZzjY7V-86", "_Kh1ClBUE4M_aFZzjY7V-91", output_port_name='OUT1', input_port_name='IN2')
        self.addConnection("_Kh1ClBUE4M_aFZzjY7V-91", "_Kh1ClBUE4M_aFZzjY7V-72", output_port_name='OUT1', input_port_name='IN1')
        self.addConnection("_Kh1ClBUE4M_aFZzjY7V-97", "_Kh1ClBUE4M_aFZzjY7V-91", output_port_name='OUT1', input_port_name='IN1')
        self.addConnection("_Kh1ClBUE4M_aFZzjY7V-72", "_Kh1ClBUE4M_aFZzjY7V-100", output_port_name='OUT1', input_port_name='IN2')
        self.addConnection("_Kh1ClBUE4M_aFZzjY7V-72", "_Kh1ClBUE4M_aFZzjY7V-112", output_port_name='OUT1', input_port_name='IN1')
        self.addConnection("_Kh1ClBUE4M_aFZzjY7V-100", "OUT1", output_port_name='OUT1')
        self.addConnection("_Kh1ClBUE4M_aFZzjY7V-100", "_Kh1ClBUE4M_aFZzjY7V-105", output_port_name='OUT1', input_port_name='IN1')
        self.addConnection("_Kh1ClBUE4M_aFZzjY7V-105", "_Kh1ClBUE4M_aFZzjY7V-100", output_port_name='OUT1', input_port_name='IN1')
        self.addConnection("_Kh1ClBUE4M_aFZzjY7V-112", "_Kh1ClBUE4M_aFZzjY7V-115", output_port_name='OUT1', input_port_name='IN1')
        self.addConnection("_Kh1ClBUE4M_aFZzjY7V-115", "_Kh1ClBUE4M_aFZzjY7V-105", output_port_name='OUT1', input_port_name='IC')


