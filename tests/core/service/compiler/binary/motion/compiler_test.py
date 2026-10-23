# -*- coding: UTF-8 -*-

'''
Module
    compiler_test.py
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

from scaralang.core.model.dsl.binary.step import BinaryStep
from scaralang.core.model.kinematics.pose.angles import JointAngles
from scaralang.core.model.protocol.message import MessageId
from scaralang.core.model.trajectory.plan.waypoint import Waypoint
from scaralang.core.service.compiler.binary.motion.compiler import MotionCompiler
from scaralang.core.service.compiler.binary.motion.dependencies import MotionDependencies
from scaralang.core.service.compiler.binary.motion.icompiler import IMotionCompiler
from scaralang.core.service.compiler.binary.step.discretizer.dependencies import DiscretizerDependencies
from scaralang.core.service.compiler.binary.step.discretizer.factory import StepDiscretizerFactory
from scaralang.core.service.compiler.binary.step.discretizer.idiscretizer import IStepDiscretizer
from scaralang.core.service.compiler.binary.step.duration.factory import SegmentDurationCalculatorFactory
from scaralang.core.service.kinematics.profile.default_scara_profile import DefaultScaraProfile
from scaralang.core.service.kinematics.transmission.factory import TransmissionFactory
from scaralang.infrastructure.protocol.builder.factory import BuilderFactory
from scaralang.infrastructure.kinematics.factory import DefaultKinematicsFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.0'
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
                | test_get_version - Verifies get_version returns valid version string.
                | test_compile_motion_step - Verifies compiling a motion waypoint to binary step.
    '''

    def setUp(self) -> None:
        '''Sets up test fixtures.'''
        kinematics = DefaultKinematicsFactory.create()
        transmission = TransmissionFactory.create(
            transmission=DefaultScaraProfile.create_transmission()
        )
        duration_calculator = SegmentDurationCalculatorFactory.create()
        discretizer: IStepDiscretizer = StepDiscretizerFactory.create(
            dependencies=DiscretizerDependencies(
                spatial=kinematics.spatial,
                numerical_spatial=kinematics.numerical_spatial,
                transmission=transmission,
                duration_calculator=duration_calculator,
            )
        )
        builder_provides = BuilderFactory.create()
        deps = MotionDependencies(
            discretizer=discretizer,
            frame_builder=builder_provides.motion,
            frame_packer=builder_provides.packer,
        )
        self.compiler = MotionCompiler(dependencies=deps)

    def test_structural_conformance(self) -> None:
        '''Verifies that MotionCompiler satisfies IMotionCompiler.'''
        self.assertIsInstance(self.compiler, IMotionCompiler)

    def test_get_version(self) -> None:
        '''Verifies get_version returns valid version string.'''
        self.assertEqual(self.compiler.get_version(), '1.1.0')

    def test_compile_motion_step(self) -> None:
        '''Verifies compiling a Cartesian waypoint to a binary move step.'''
        waypoint = Waypoint(
            x=150.0,
            y=50.0,
            z=10.0,
            phi=0.0,
            speed=50.0,
            name='',
            command='',
        )
        step, new_angles = self.compiler.compile_motion_step(
            waypoint=waypoint,
            seq_num=1,
            prev_angles=JointAngles(theta1=0.0, theta2=0.0, z=0.0, theta4=0.0),
            line_num=5,
        )
        self.assertIsInstance(step, BinaryStep)
        self.assertEqual(step.frame.msg_id, MessageId.CMD_MOVE_JOINT_STEPS)
        self.assertEqual(step.frame.seq_num, 1)
        self.assertEqual(step.line_number, 5)
        self.assertGreater(len(step.raw_bytes), 0)
        self.assertIsInstance(new_angles, JointAngles)


if __name__ == '__main__':
    main()
