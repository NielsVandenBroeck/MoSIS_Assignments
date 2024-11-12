#!/usr/bin/python3
# This file was automatically generated from drawio2cbd with the command:
#   DrawioConvert/__main__.py -F CBD -e forward_euler_method -sSrgv ./DrawioFiles/Forward_Euler_Method.drawio -E delta=1 -d ./DrawioFiles/generated/ -f

from pyCBD.Core import *
from pyCBD.lib.std import *

DELTA_T = 1

class forward_euler_method(CBD):
    def __init__(self, block_name):
        super().__init__(block_name, input_ports=['IN1', 'IC'], output_ports=['OUT1'])

        # Create the Blocks
        self.addBlock(DelayBlock("H1DVWqrLM_NFR8ge84JM-6"))
        self.addBlock(DeltaTBlock("H1DVWqrLM_NFR8ge84JM-10"))
        self.addBlock(ProductBlock("H1DVWqrLM_NFR8ge84JM-12", numberOfInputs=(2)))
        self.addBlock(AdderBlock("H1DVWqrLM_NFR8ge84JM-17", numberOfInputs=(2)))
        self.addBlock(NegatorBlock("RXzqZUEvsSW9Q8SqqrWO-42"))
        self.addBlock(AdderBlock("RXzqZUEvsSW9Q8SqqrWO-46", numberOfInputs=(2)))

        # Create the Connections
        self.addConnection("IN1", "H1DVWqrLM_NFR8ge84JM-12", input_port_name='IN1')
        self.addConnection("H1DVWqrLM_NFR8ge84JM-10", "H1DVWqrLM_NFR8ge84JM-12", output_port_name='OUT1', input_port_name='IN2')
        self.addConnection("H1DVWqrLM_NFR8ge84JM-12", "H1DVWqrLM_NFR8ge84JM-17", output_port_name='OUT1', input_port_name='IN2')
        self.addConnection("H1DVWqrLM_NFR8ge84JM-12", "RXzqZUEvsSW9Q8SqqrWO-42", output_port_name='OUT1', input_port_name='IN1')
        self.addConnection("IC", "RXzqZUEvsSW9Q8SqqrWO-46", input_port_name='IN1')
        self.addConnection("H1DVWqrLM_NFR8ge84JM-6", "H1DVWqrLM_NFR8ge84JM-17", output_port_name='OUT1', input_port_name='IN1')
        self.addConnection("RXzqZUEvsSW9Q8SqqrWO-46", "H1DVWqrLM_NFR8ge84JM-6", output_port_name='OUT1', input_port_name='IC')
        self.addConnection("RXzqZUEvsSW9Q8SqqrWO-42", "RXzqZUEvsSW9Q8SqqrWO-46", output_port_name='OUT1', input_port_name='IN2')
        self.addConnection("H1DVWqrLM_NFR8ge84JM-17", "OUT1", output_port_name='OUT1')
        self.addConnection("H1DVWqrLM_NFR8ge84JM-17", "H1DVWqrLM_NFR8ge84JM-6", output_port_name='OUT1', input_port_name='IN1')


