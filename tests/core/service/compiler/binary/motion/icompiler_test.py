# -*- coding: UTF-8 -*-

'''
Module
    icompiler_test.py
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
    Unit tests for IMotionCompiler protocol.
'''

from __future__ import annotations

from unittest import TestCase, main

from scaralang.core.model.dsl.binary.step import BinaryStep
from scaralang.core.model.kinematics.pose.angles import JointAngles
from scaralang.core.model.kinematics.pose.steps import JointStepCoordinates
from scaralang.core.model.protocol.frame import BinaryFrame
from scaralang.core.model.protocol.message import MessageId
from scaralang.core.model.trajectory.plan.waypoint import Waypoint
from scaralang.core.service.compiler.binary.motion.icompiler import IMotionCompiler

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DummyMotionCompiler:
    '''Dummy class implementing IMotionCompiler for protocol verification.'''

    def compile_motion_step(
        self,
        *,
        waypoint: Waypoint,
        seq_num: int,
        prev_angles: JointAngles,
        line_num: int
    ) -> tuple[BinaryStep, JointAngles]:
        '''Dummy implementation of compile_motion_step.'''
        _ = (waypoint, prev_angles)
        frame = BinaryFrame(
            seq_num=seq_num,
            msg_id=MessageId.CMD_MOVE_JOINT_STEPS,
            payload=b'',
            crc16=0,
        )
        step = BinaryStep(
            frame=frame,
            raw_bytes=b'',
            duration_us=1000,
            target_steps=JointStepCoordinates(j1=0, j2=0, z=0, j4=0),
            description='dummy',
            line_number=line_num,
        )
        return step, JointAngles(theta1=0.0, theta2=0.0, z=0.0, theta4=0.0)

    def get_version(self) -> str:
        '''Dummy implementation of get_version.'''
        return '1.1.0'


class TestIMotionCompiler(TestCase):
    '''
        Test cases verifying IMotionCompiler structural protocol.

        It defines:

            :methods:
                | test_structural_conformance - Verifies protocol check.
                | test_structural_rejection - Verifies incomplete dummy is rejected.
    '''

    def test_structural_conformance(self) -> None:
        '''Verifies that dummy conforming class satisfies protocol check.'''
        compiler = DummyMotionCompiler()
        self.assertIsInstance(compiler, IMotionCompiler)

    def test_structural_rejection(self) -> None:
        '''Verifies that class missing required methods fails protocol check.'''
        self.assertFalse(isinstance(object(), IMotionCompiler))


if __name__ == '__main__':
    main()
