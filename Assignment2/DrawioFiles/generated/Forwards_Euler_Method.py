#!/usr/bin/python3
# This file was automatically generated from drawio2cbd with the command:
#   DrawioConvert/__main__.py -F CBD -e forwards_euler_method -sSrgv ./DrawioFiles/Forwards_Euler_Method.drawio -E delta=1 -d ./DrawioFiles/generated/ -f

from pyCBD.Core import *
from pyCBD.lib.std import *

DELTA_T = 1

class forwards_euler_method(CBD):
    def __init__(self, block_name):
        super().__init__(block_name, input_ports=['IC', 'IN1'], output_ports=['OUT1'])

        # Create the Blocks
        self.addBlock(DelayBlock("wvZRwbNYt29LTI-XGSjr-144"))
        self.addBlock(DeltaTBlock("wvZRwbNYt29LTI-XGSjr-148"))
        self.addBlock(ProductBlock("wvZRwbNYt29LTI-XGSjr-150", numberOfInputs=(2)))
        self.addBlock(AdderBlock("wvZRwbNYt29LTI-XGSjr-155", numberOfInputs=(2)))
        self.addBlock(NegatorBlock("wvZRwbNYt29LTI-XGSjr-168"))
        self.addBlock(AdderBlock("wvZRwbNYt29LTI-XGSjr-173", numberOfInputs=(2)))

        # Create the Connections
        self.addConnection("IN1", "wvZRwbNYt29LTI-XGSjr-150", input_port_name='IN1')
        self.addConnection("wvZRwbNYt29LTI-XGSjr-148", "wvZRwbNYt29LTI-XGSjr-150", output_port_name='OUT1', input_port_name='IN2')
        self.addConnection("wvZRwbNYt29LTI-XGSjr-150", "wvZRwbNYt29LTI-XGSjr-155", output_port_name='OUT1', input_port_name='IN2')
        self.addConnection("wvZRwbNYt29LTI-XGSjr-150", "wvZRwbNYt29LTI-XGSjr-168", output_port_name='OUT1', input_port_name='IN1')
        self.addConnection("IC", "wvZRwbNYt29LTI-XGSjr-173", input_port_name='IN1')
        self.addConnection("wvZRwbNYt29LTI-XGSjr-144", "wvZRwbNYt29LTI-XGSjr-155", output_port_name='OUT1', input_port_name='IN1')
        self.addConnection("wvZRwbNYt29LTI-XGSjr-173", "wvZRwbNYt29LTI-XGSjr-144", output_port_name='OUT1', input_port_name='IC')
        self.addConnection("wvZRwbNYt29LTI-XGSjr-168", "wvZRwbNYt29LTI-XGSjr-173", output_port_name='OUT1', input_port_name='IN2')
        self.addConnection("wvZRwbNYt29LTI-XGSjr-155", "OUT1", output_port_name='OUT1')
        self.addConnection("wvZRwbNYt29LTI-XGSjr-155", "wvZRwbNYt29LTI-XGSjr-144", output_port_name='OUT1', input_port_name='IN1')


