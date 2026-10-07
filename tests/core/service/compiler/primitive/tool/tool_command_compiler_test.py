# -*- coding: UTF-8 -*-

'''
Module
    tool_command_compiler_test.py
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
    Unit tests for ToolCommandCompiler.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.model.dsl.ast.command_type import ScaraCommandType
from scaralang.core.model.dsl.ast.instruction import ScaraInstruction
from scaralang.core.model.dsl.ast.instruction_param import InstructionParam
from scaralang.core.model.dsl.ast.pneumatic_state import PneumaticState
from scaralang.core.model.dsl.compiler.scara_compiler_context import ScaraCompilerContext
from scaralang.core.service.compiler.primitive.iprimitive_compiler import IPrimitiveCompiler
from scaralang.core.service.compiler.primitive.tool.tool_command_compiler import ToolCommandCompiler
from scaralang.core.service.compiler.primitive.tool.tool_waypoint_builder_factory import ToolWaypointBuilderFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.7'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestToolCommandCompiler(TestCase):
    '''
        Test cases verifying ToolCommandCompiler functionality.

        It defines:

            :methods:
                | setUp - Prepares test fixtures.
                | test_protocol_conformance - Verifies IPrimitiveCompiler conformance.
                | test_can_compile - Verifies supported command identification.
                | test_compile_pump - Verifies compilation of PUMP instructions.
                | test_compile_valve - Verifies compilation of VALVE instructions.
                | test_compile_unsupported_no_op - Verifies unhandled commands are ignored.
    '''

    def setUp(self) -> None:
        '''
            Sets up test fixture with compiler and context.
        '''
        builder = ToolWaypointBuilderFactory.create()
        self.compiler = ToolCommandCompiler(waypoint_builder=builder)
        self.context = ScaraCompilerContext()

    def test_protocol_conformance(self) -> None:
        '''
            Verifies structural protocol conformance to IPrimitiveCompiler.
        '''
        self.assertIsInstance(self.compiler, IPrimitiveCompiler)

    def test_can_compile(self) -> None:
        '''
            Verifies can_compile identifies PUMP and VALVE commands.
        '''
        pump_inst = ScaraInstruction(
            command_type=ScaraCommandType.PUMP,
            parameters={InstructionParam.STATE: PneumaticState.ON},
            line_number=1,
            raw_text='PUMP ON',
        )
        valve_inst = ScaraInstruction(
            command_type=ScaraCommandType.VALVE,
            parameters={InstructionParam.STATE: PneumaticState.OFF},
            line_number=2,
            raw_text='VALVE OFF',
        )
        move_inst = ScaraInstruction(
            command_type=ScaraCommandType.MOVE_L,
            parameters={},
            line_number=3,
            raw_text='MOVE_L',
        )
        self.assertTrue(self.compiler.can_compile(instruction=pump_inst))
        self.assertTrue(self.compiler.can_compile(instruction=valve_inst))
        self.assertFalse(self.compiler.can_compile(instruction=move_inst))

    def test_compile_pump(self) -> None:
        '''
            Verifies compilation of PUMP commands into waypoints.
        '''
        inst = ScaraInstruction(
            command_type=ScaraCommandType.PUMP,
            parameters={InstructionParam.STATE: PneumaticState.ON},
            line_number=1,
            raw_text='PUMP ON',
        )
        result = self.compiler.compile(
            instruction=inst,
            context=self.context,
        )
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].name, 'PUMP_ON')
        self.assertEqual(result[0].command, '<CMD:PUMP#1>')

    def test_compile_valve(self) -> None:
        '''
            Verifies compilation of VALVE commands into waypoints.
        '''
        inst = ScaraInstruction(
            command_type=ScaraCommandType.VALVE,
            parameters={InstructionParam.STATE: PneumaticState.OFF},
            line_number=1,
            raw_text='VALVE OFF',
        )
        result = self.compiler.compile(
            instruction=inst,
            context=self.context,
        )
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].name, 'VALVE_OFF')
        self.assertEqual(result[0].command, '<CMD:VALVE#0>')

    def test_compile_unsupported_no_op(self) -> None:
        '''
            Verifies unsupported commands do not append waypoints.
        '''
        inst = ScaraInstruction(
            command_type=ScaraCommandType.MOVE_L,
            parameters={},
            line_number=1,
            raw_text='MOVE_L',
        )
        result = self.compiler.compile(
            instruction=inst,
            context=self.context,
        )
        self.assertEqual(result, ())


if __name__ == '__main__':
    main()
