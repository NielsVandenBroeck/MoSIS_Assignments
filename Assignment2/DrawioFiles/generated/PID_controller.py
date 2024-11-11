#!/usr/bin/python3
# This file was automatically generated from drawio2cbd with the command:
#   DrawioConvert/__main__.py -F CBD -e g_function -sSrgv ./DrawioFiles/PID_controller.drawio -E delta=1 -d ./DrawioFiles/generated/ -f

from pyCBD.Core import *
from pyCBD.lib.std import *

DELTA_T = 1

class PID_controller(CBD):
    def __init__(self, block_name):
        super().__init__(block_name, input_ports=['IN'], output_ports=['OUT'])

        # Create the Blocks
        self.addBlock(ConstantBlock("xFvxAx3d5TRpq_XM0aEQ-93", value=(26)))
        self.addBlock(ConstantBlock("xFvxAx3d5TRpq_XM0aEQ-95", value=(1)))
        self.addBlock(ConstantBlock("xFvxAx3d5TRpq_XM0aEQ-97", value=(10)))
        self.addBlock(ConstantBlock("xFvxAx3d5TRpq_XM0aEQ-105", value=(10)))
        self.addBlock(NegatorBlock("xFvxAx3d5TRpq_XM0aEQ-108"))
        self.addBlock(AdderBlock("xFvxAx3d5TRpq_XM0aEQ-111", numberOfInputs=(2)))
        self.addBlock(DerivatorBlock("xFvxAx3d5TRpq_XM0aEQ-117"))
        self.addBlock(AdderBlock("xFvxAx3d5TRpq_XM0aEQ-121", numberOfInputs=(2)))
        self.addBlock(AdderBlock("xFvxAx3d5TRpq_XM0aEQ-125", numberOfInputs=(2)))
        self.addBlock(ProductBlock("xFvxAx3d5TRpq_XM0aEQ-129", numberOfInputs=(2)))
        self.addBlock(ProductBlock("xFvxAx3d5TRpq_XM0aEQ-135", numberOfInputs=(2)))
        self.addBlock(IntegratorBlock("xFvxAx3d5TRpq_XM0aEQ-140"))
        self.addBlock(ProductBlock("xFvxAx3d5TRpq_XM0aEQ-145", numberOfInputs=(2)))
        self.addBlock(ConstantBlock("xFvxAx3d5TRpq_XM0aEQ-158", value=(0)))

        # Create the Connections
        self.addConnection("IN", "xFvxAx3d5TRpq_XM0aEQ-108", input_port_name='IN1')
        self.addConnection("xFvxAx3d5TRpq_XM0aEQ-105", "xFvxAx3d5TRpq_XM0aEQ-111", output_port_name='OUT1', input_port_name='IN2')
        self.addConnection("xFvxAx3d5TRpq_XM0aEQ-108", "xFvxAx3d5TRpq_XM0aEQ-111", output_port_name='OUT1', input_port_name='IN1')
        self.addConnection("xFvxAx3d5TRpq_XM0aEQ-93", "xFvxAx3d5TRpq_XM0aEQ-129", output_port_name='OUT1', input_port_name='IN1')
        self.addConnection("xFvxAx3d5TRpq_XM0aEQ-111", "xFvxAx3d5TRpq_XM0aEQ-129", output_port_name='OUT1', input_port_name='IN2')
        self.addConnection("xFvxAx3d5TRpq_XM0aEQ-111", "xFvxAx3d5TRpq_XM0aEQ-117", output_port_name='OUT1', input_port_name='IN1')
        self.addConnection("xFvxAx3d5TRpq_XM0aEQ-111", "xFvxAx3d5TRpq_XM0aEQ-140", output_port_name='OUT1', input_port_name='IN1')
        self.addConnection("xFvxAx3d5TRpq_XM0aEQ-95", "xFvxAx3d5TRpq_XM0aEQ-135", output_port_name='OUT1', input_port_name='IN1')
        self.addConnection("xFvxAx3d5TRpq_XM0aEQ-140", "xFvxAx3d5TRpq_XM0aEQ-135", output_port_name='OUT1', input_port_name='IN2')
        self.addConnection("xFvxAx3d5TRpq_XM0aEQ-97", "xFvxAx3d5TRpq_XM0aEQ-145", output_port_name='OUT1', input_port_name='IN1')
        self.addConnection("xFvxAx3d5TRpq_XM0aEQ-117", "xFvxAx3d5TRpq_XM0aEQ-145", output_port_name='OUT1', input_port_name='IN2')
        self.addConnection("xFvxAx3d5TRpq_XM0aEQ-129", "xFvxAx3d5TRpq_XM0aEQ-121", output_port_name='OUT1', input_port_name='IN1')
        self.addConnection("xFvxAx3d5TRpq_XM0aEQ-135", "xFvxAx3d5TRpq_XM0aEQ-121", output_port_name='OUT1', input_port_name='IN2')
        self.addConnection("xFvxAx3d5TRpq_XM0aEQ-125", "OUT", output_port_name='OUT1')
        self.addConnection("xFvxAx3d5TRpq_XM0aEQ-121", "xFvxAx3d5TRpq_XM0aEQ-125", output_port_name='OUT1', input_port_name='IN1')
        self.addConnection("xFvxAx3d5TRpq_XM0aEQ-145", "xFvxAx3d5TRpq_XM0aEQ-125", output_port_name='OUT1', input_port_name='IN2')
        self.addConnection("xFvxAx3d5TRpq_XM0aEQ-158", "xFvxAx3d5TRpq_XM0aEQ-117", output_port_name='OUT1', input_port_name='IC')
        self.addConnection("xFvxAx3d5TRpq_XM0aEQ-158", "xFvxAx3d5TRpq_XM0aEQ-140", output_port_name='OUT1', input_port_name='IC')


