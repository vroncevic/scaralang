# -*- coding: UTF-8 -*-

'''
Module
    motion_compiler_test.py
Copyright
    Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>
    scaralang is free software: you can redistribute it and/or modify it
    under the terms of the GNU General Public License as published by the
    Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    scaralang is distributed in the hope that it will be useful, but
    WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
    See the GNU General Public License for more details.
    You should have received a copy of the GNU General Public License along
    with this program. If not, see <http://www.gnu.org/licenses/>.
Info
    Unit tests for MotionCompiler class.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.model.protocol.message_id import MessageId
from scaralang.core.model.dsl.binary.step import Step
from scaralang.core.model.trajectory.waypoint import Waypoint
from scaralang.core.service.compiler.binary.motion.imotion_compiler import IMotionCompiler
from scaralang.core.service.compiler.binary.motion.motion_compiler_factory import MotionCompilerFactory
from scaralang.core.service.compiler.binary.step.istep_discretizer import IStepDiscretizer
from scaralang.core.service.compiler.binary.step.step_discretizer_factory import StepDiscretizerFactory
from scaralang.core.service.kinematics.default_scara_profile import DefaultScaraProfile
from scaralang.core.service.kinematics.kinematics_service_factory import KinematicsServiceFactory
from scaralang.core.service.kinematics.transmission.joint_step_transmission_converter_factory import JointStepTransmissionConverterFactory
from scaralang.core.service.protocol.ibinary_frame_builder import IBinaryFrameBuilder
from scaralang.infrastructure.communication.protocol.binary.builder.binary_frame_builder_factory import BinaryFrameBuilderFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestMotionCompiler(TestCase):
    '''
        Test cases verifying MotionCompiler step generation.

        It defines:

            :methods:
                | setUp - Initializes MotionCompiler fixture.
                | test_structural_conformance - Verifies IMotionCompiler protocol satisfaction.
                | test_compile_motion_step - Verifies compiling a motion waypoint to binary step.
    '''

    def setUp(self) -> None:
        '''
            Sets up test fixtures.
        '''
        bounds = DefaultScaraProfile.create_bounds()
        kinematics = KinematicsServiceFactory.create(bounds=bounds)
        transmission = JointStepTransmissionConverterFactory.create_default()
        discretizer: IStepDiscretizer = StepDiscretizerFactory.create(
            kinematics=kinematics,
            transmission=transmission,
        )
        frame_builder: IBinaryFrameBuilder = BinaryFrameBuilderFactory.create()
        self.compiler: IMotionCompiler = MotionCompilerFactory.create(
            discretizer=discretizer,
            frame_builder=frame_builder,
        )

    def test_structural_conformance(self) -> None:
        '''
            Verifies that MotionCompiler satisfies IMotionCompiler.
        '''
        self.assertIsInstance(self.compiler, IMotionCompiler)

    def test_compile_motion_step(self) -> None:
        '''
            Verifies compiling a Cartesian waypoint to a binary move step.
        '''
        waypoint = Waypoint(
            x=150.0,
            y=50.0,
            z=10.0,
            phi=0.0,
            speed=50.0,
        )
        step, new_angles = self.compiler.compile_motion_step(
            waypoint=waypoint,
            seq_num=1,
            prev_angles=(0.0, 0.0, 0.0, 0.0),
            line_num=5,
        )
        self.assertIsInstance(step, Step)
        self.assertEqual(step.frame.msg_id, MessageId.CMD_MOVE_JOINT_STEPS)
        self.assertEqual(step.frame.seq_num, 1)
        self.assertEqual(step.line_number, 5)
        self.assertGreater(len(step.raw_bytes), 0)
        self.assertEqual(len(new_angles), 4)


if __name__ == '__main__':
    main()
