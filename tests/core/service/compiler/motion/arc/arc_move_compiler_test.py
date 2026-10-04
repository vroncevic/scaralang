# -*- coding: UTF-8 -*-

'''
Module
    arc_move_compiler_test.py
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
    Unit tests for ArcMoveCompiler.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.model.dsl.ast.command_type import ScaraCommandType
from scaralang.core.model.dsl.ast.instruction import ScaraInstruction
from scaralang.core.model.dsl.compiler.compiler_pose_state import CompilerPoseState
from scaralang.core.model.dsl.compiler.compiler_speed_state import CompilerSpeedState
from scaralang.core.model.dsl.compiler.scara_compiler_context import ScaraCompilerContext
from scaralang.core.service.compiler.motion.arc.arc_move_compiler import ArcMoveCompiler
from scaralang.core.service.compiler.motion.arc.arc_move_compiler_factory import ArcMoveCompilerFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestArcMoveCompiler(TestCase):
    '''
        Test cases verifying ArcMoveCompiler execution.

        It defines:

            :methods:
                | setUp - Initializes compiler and context.
                | test_can_compile - Verifies command type detection.
                | test_compile - Verifies arc instruction compilation and context update.
    '''

    def setUp(self) -> None:
        '''
            Prepares ArcMoveCompiler and initial compiler context.
        '''
        self.compiler: ArcMoveCompiler = ArcMoveCompilerFactory.create()
        self.context = ScaraCompilerContext(
            pose=CompilerPoseState(
                current_x=100.0,
                current_y=0.0,
                current_z=10.0,
                current_phi=0.0,
            ),
            speed=CompilerSpeedState(
                current_speed=50.0,
            ),
        )

    def test_can_compile(self) -> None:
        '''
            Verifies instruction compatibility detection.
        '''
        arc_cw = ScaraInstruction(
            command_type=ScaraCommandType.ARC_CW,
            parameters={'X': 0.0, 'Y': 100.0, 'I': -100.0, 'J': 0.0},
            line_number=1,
            raw_text='ARC_CW',
        )
        move_j = ScaraInstruction(
            command_type=ScaraCommandType.MOVE_J,
            parameters={'X': 100.0, 'Y': 100.0},
            line_number=2,
            raw_text='MOVE_J',
        )
        self.assertTrue(self.compiler.can_compile(instruction=arc_cw))
        self.assertFalse(self.compiler.can_compile(instruction=move_j))

    def test_compile(self) -> None:
        '''
            Verifies compilation of arc command into waypoints and context update.
        '''
        instruction = ScaraInstruction(
            command_type=ScaraCommandType.ARC_CW,
            parameters={'X': 0.0, 'Y': 100.0, 'I': -100.0, 'J': 0.0, 'Z': 15.0, 'SPEED': 40.0},
            line_number=1,
            raw_text='ARC_CW X=0 Y=100 I=-100 J=0 Z=15 SPEED=40',
        )
        waypoints = self.compiler.compile(
            instruction=instruction,
            context=self.context,
        )
        self.assertGreater(len(waypoints), 0)
        self.assertAlmostEqual(self.context.pose.current_x, 0.0)
        self.assertAlmostEqual(self.context.pose.current_y, 100.0)
        self.assertAlmostEqual(self.context.pose.current_z, 15.0)


if __name__ == '__main__':
    main()
