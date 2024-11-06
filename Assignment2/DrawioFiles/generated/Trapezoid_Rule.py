#!/usr/bin/python3
# This file was automatically generated from drawio2cbd with the command:
#   DrawioConvert/__main__.py -F CBD -e trapezoid_rule -sSrgv ./DrawioFiles/Trapezoid_Rule.drawio -E delta=1 -d ./DrawioFiles/generated/ -f

from pyCBD.Core import *
from pyCBD.lib.std import *

DELTA_T = 1

class trapezoid_rule(CBD):
    def __init__(self, block_name):
        super().__init__(block_name, input_ports=['IC', 'IN1'], output_ports=['OUT1'])

        # Create the Blocks
        self.addBlock(DeltaTBlock("RprQI59_ezlDkIdyMx8F-110"))
        self.addBlock(ProductBlock("RprQI59_ezlDkIdyMx8F-112", numberOfInputs=(2)))
        self.addBlock(DelayBlock("RprQI59_ezlDkIdyMx8F-122"))
        self.addBlock(AdderBlock("RprQI59_ezlDkIdyMx8F-126", numberOfInputs=(2)))
        self.addBlock(ProductBlock("RprQI59_ezlDkIdyMx8F-131", numberOfInputs=(2)))
        self.addBlock(ConstantBlock("RprQI59_ezlDkIdyMx8F-137", value=(0.5)))
        self.addBlock(AdderBlock("RprQI59_ezlDkIdyMx8F-140", numberOfInputs=(2)))
        self.addBlock(DelayBlock("RprQI59_ezlDkIdyMx8F-145"))
        self.addBlock(ConstantBlock("2pB3fr3-j1_Edrij6ADm-1", value=(0)))

        # Create the Connections
        self.addConnection("IN1", "RprQI59_ezlDkIdyMx8F-122", input_port_name='IN1')
        self.addConnection("IN1", "RprQI59_ezlDkIdyMx8F-126", input_port_name='IN2')
        self.addConnection("RprQI59_ezlDkIdyMx8F-110", "RprQI59_ezlDkIdyMx8F-112", output_port_name='OUT1', input_port_name='IN2')
        self.addConnection("IC", "RprQI59_ezlDkIdyMx8F-122", input_port_name='IC')
        self.addConnection("RprQI59_ezlDkIdyMx8F-122", "RprQI59_ezlDkIdyMx8F-126", output_port_name='OUT1', input_port_name='IN1')
        self.addConnection("RprQI59_ezlDkIdyMx8F-126", "RprQI59_ezlDkIdyMx8F-131", output_port_name='OUT1', input_port_name='IN2')
        self.addConnection("RprQI59_ezlDkIdyMx8F-131", "RprQI59_ezlDkIdyMx8F-112", output_port_name='OUT1', input_port_name='IN1')
        self.addConnection("RprQI59_ezlDkIdyMx8F-137", "RprQI59_ezlDkIdyMx8F-131", output_port_name='OUT1', input_port_name='IN1')
        self.addConnection("RprQI59_ezlDkIdyMx8F-112", "RprQI59_ezlDkIdyMx8F-140", output_port_name='OUT1', input_port_name='IN2')
        self.addConnection("RprQI59_ezlDkIdyMx8F-140", "OUT1", output_port_name='OUT1')
        self.addConnection("RprQI59_ezlDkIdyMx8F-140", "RprQI59_ezlDkIdyMx8F-145", output_port_name='OUT1', input_port_name='IN1')
        self.addConnection("RprQI59_ezlDkIdyMx8F-145", "RprQI59_ezlDkIdyMx8F-140", output_port_name='OUT1', input_port_name='IN1')
        self.addConnection("2pB3fr3-j1_Edrij6ADm-1", "RprQI59_ezlDkIdyMx8F-145", output_port_name='OUT1', input_port_name='IC')


