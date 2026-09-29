# -*- coding: UTF-8 -*-

'''
Module
    motion_command_compiler_test.py
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
    Unit tests for MotionCommandCompiler coordinator component.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main
from unittest.mock import MagicMock

from scaralang.core.model.dsl.ast.command_type import ScaraCommandType
from scaralang.core.model.dsl.ast.instruction import ScaraInstruction
from scaralang.core.model.dsl.compiler.scara_compiler_context import ScaraCompilerContext
from scaralang.core.model.trajectory.waypoint import Waypoint
from scaralang.core.service.compiler.motion.imotion_sub_compiler import IMotionSubCompiler
from scaralang.core.service.compiler.motion.motion_command_compiler import MotionCommandCompiler
from scaralang.core.service.compiler.primitive.iprimitive_compiler import IPrimitiveCompiler

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestMotionCommandCompiler(TestCase):
    '''
        Test cases verifying MotionCommandCompiler coordinator functionality.

        It defines:

            :methods:
                | setUp - Prepares test fixture with mock sub-compilers.
                | test_protocol_conformance - Verifies IPrimitiveCompiler conformance.
                | test_can_compile - Verifies handled motion command types.
                | test_compile_delegates_to_cartesian - Verifies delegation to cartesian compiler.
                | test_compile_delegates_to_vertical - Verifies delegation to vertical compiler.
                | test_compile_delegates_to_arc - Verifies delegation to arc compiler.
                | test_compile_unhandled_no_op - Verifies unhandled instructions do not delegate.
    '''

    def setUp(self) -> None:
        '''
            Sets up test fixture with mock sub-compilers.
        '''
        self.mock_cartesian = MagicMock(spec=IMotionSubCompiler)
        self.mock_vertical = MagicMock(spec=IMotionSubCompiler)
        self.mock_arc = MagicMock(spec=IMotionSubCompiler)

        self.mock_cartesian.can_compile.return_value = False
        self.mock_vertical.can_compile.return_value = False
        self.mock_arc.can_compile.return_value = False

        self.compiler = MotionCommandCompiler(
            cartesian_compiler=self.mock_cartesian,
            vertical_compiler=self.mock_vertical,
            arc_compiler=self.mock_arc,
        )

    def test_protocol_conformance(self) -> None:
        '''
            Verifies structural conformance to IPrimitiveCompiler protocol.
        '''
        self.assertIsInstance(self.compiler, IPrimitiveCompiler)

    def test_can_compile(self) -> None:
        '''
            Verifies can_compile identifies all supported motion commands.
        '''
        supported_types = (
            ScaraCommandType.MOVE_L,
            ScaraCommandType.MOVE_J,
            ScaraCommandType.APPROACH,
            ScaraCommandType.RETRACT,
            ScaraCommandType.ARC_CW,
            ScaraCommandType.ARC_CCW,
        )
        for cmd_type in supported_types:
            inst = ScaraInstruction(
                command_type=cmd_type,
                parameters={},
                line_number=1,
                raw_text=str(cmd_type.value),
            )
            self.assertTrue(
                self.compiler.can_compile(instruction=inst),
                f'Expected {cmd_type} to be compilable',
            )

        other_inst = ScaraInstruction(
            command_type=ScaraCommandType.WAIT,
            parameters={},
            line_number=2,
            raw_text='WAIT 1.0',
        )
        self.assertFalse(self.compiler.can_compile(instruction=other_inst))

    def test_compile_delegates_to_cartesian(self) -> None:
        '''
            Verifies compile delegates to cartesian compiler when it matches.
        '''
        inst = ScaraInstruction(
            command_type=ScaraCommandType.MOVE_L,
            parameters={},
            line_number=1,
            raw_text='MOVE_L',
        )
        context = ScaraCompilerContext()
        expected_wp = MagicMock(spec=Waypoint)

        self.mock_cartesian.can_compile.return_value = True
        self.mock_cartesian.compile.return_value = (expected_wp,)

        result = self.compiler.compile(instruction=inst, context=context)
        self.assertEqual(result, (expected_wp,))
        self.mock_cartesian.compile.assert_called_once_with(
            instruction=inst, context=context
        )
        self.mock_vertical.compile.assert_not_called()
        self.mock_arc.compile.assert_not_called()

    def test_compile_delegates_to_vertical(self) -> None:
        '''
            Verifies compile delegates to vertical compiler when it matches.
        '''
        inst = ScaraInstruction(
            command_type=ScaraCommandType.APPROACH,
            parameters={},
            line_number=1,
            raw_text='APPROACH 10',
        )
        context = ScaraCompilerContext()
        expected_wp = MagicMock(spec=Waypoint)

        self.mock_vertical.can_compile.return_value = True
        self.mock_vertical.compile.return_value = (expected_wp,)

        result = self.compiler.compile(instruction=inst, context=context)
        self.assertEqual(result, (expected_wp,))
        self.mock_cartesian.compile.assert_not_called()
        self.mock_vertical.compile.assert_called_once_with(
            instruction=inst, context=context
        )
        self.mock_arc.compile.assert_not_called()

    def test_compile_delegates_to_arc(self) -> None:
        '''
            Verifies compile delegates to arc compiler when it matches.
        '''
        inst = ScaraInstruction(
            command_type=ScaraCommandType.ARC_CW,
            parameters={},
            line_number=1,
            raw_text='ARC_CW',
        )
        context = ScaraCompilerContext()
        expected_wp = MagicMock(spec=Waypoint)

        self.mock_arc.can_compile.return_value = True
        self.mock_arc.compile.return_value = (expected_wp,)

        result = self.compiler.compile(instruction=inst, context=context)
        self.assertEqual(result, (expected_wp,))
        self.mock_cartesian.compile.assert_not_called()
        self.mock_vertical.compile.assert_not_called()
        self.mock_arc.compile.assert_called_once_with(
            instruction=inst, context=context
        )

    def test_compile_unhandled_no_op(self) -> None:
        '''
            Verifies compile does not delegate when no sub-compiler matches.
        '''
        inst = ScaraInstruction(
            command_type=ScaraCommandType.WAIT,
            parameters={},
            line_number=1,
            raw_text='WAIT 1.0',
        )
        context = ScaraCompilerContext()

        result = self.compiler.compile(instruction=inst, context=context)
        self.assertEqual(result, ())
        self.mock_cartesian.compile.assert_not_called()
        self.mock_vertical.compile.assert_not_called()
        self.mock_arc.compile.assert_not_called()


if __name__ == '__main__':
    main()
