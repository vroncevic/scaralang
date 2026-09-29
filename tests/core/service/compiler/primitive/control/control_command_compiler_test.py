# -*- coding: UTF-8 -*-

'''
Module
    control_command_compiler_test.py
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
    Unit tests for ControlCommandCompiler.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.model.dsl.ast.command_type import ScaraCommandType
from scaralang.core.model.dsl.ast.instruction import ScaraInstruction
from scaralang.core.model.dsl.ast.instruction_param import InstructionParam
from scaralang.core.model.dsl.compiler.scara_compiler_context import ScaraCompilerContext
from scaralang.core.model.motor.motor_drive_mode import MotorDriveMode
from scaralang.core.service.compiler.primitive.control.control_command_compiler import ControlCommandCompiler
from scaralang.core.service.compiler.primitive.control.control_waypoint_builder_factory import ControlWaypointBuilderFactory
from scaralang.core.service.compiler.primitive.iprimitive_compiler import IPrimitiveCompiler

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestControlCommandCompiler(TestCase):
    '''
        Test cases verifying ControlCommandCompiler functionality.

        It defines:

            :methods:
                | setUp - Prepares test fixtures.
                | test_protocol_conformance - Verifies IPrimitiveCompiler conformance.
                | test_can_compile - Verifies supported command identification.
                | test_compile_home - Verifies compilation of HOME instruction.
                | test_compile_wait_ms - Verifies compilation of WAIT_MS instruction.
                | test_compile_control_states - Verifies compilation of safety & control states.
                | test_compile_unsupported_no_op - Verifies unhandled commands are ignored.
    '''

    def setUp(self) -> None:
        '''
            Sets up test fixture with compiler and context.
        '''
        builder = ControlWaypointBuilderFactory.create()
        self.compiler = ControlCommandCompiler(waypoint_builder=builder)
        self.context = ScaraCompilerContext()

    def test_protocol_conformance(self) -> None:
        '''
            Verifies structural protocol conformance to IPrimitiveCompiler.
        '''
        self.assertIsInstance(self.compiler, IPrimitiveCompiler)

    def test_can_compile(self) -> None:
        '''
            Verifies can_compile identifies execution control commands.
        '''
        supported = (
            ScaraCommandType.HOME,
            ScaraCommandType.WAIT_MS,
            ScaraCommandType.HOLD,
            ScaraCommandType.RESUME,
            ScaraCommandType.ESTOP,
            ScaraCommandType.ENABLE,
            ScaraCommandType.DISABLE,
            ScaraCommandType.CONFIG_MOTOR,
        )
        for cmd in supported:
            inst = ScaraInstruction(command_type=cmd, parameters={}, line_number=1, raw_text='')
            self.assertTrue(self.compiler.can_compile(instruction=inst))

        unsupported_inst = ScaraInstruction(
            command_type=ScaraCommandType.MOVE_L,
            parameters={},
            line_number=1,
            raw_text='',
        )
        self.assertFalse(self.compiler.can_compile(instruction=unsupported_inst))

    def test_compile_home(self) -> None:
        '''
            Verifies compilation of HOME command.
        '''
        inst = ScaraInstruction(
            command_type=ScaraCommandType.HOME,
            parameters={},
            line_number=1,
            raw_text='HOME',
        )
        result = self.compiler.compile(
            instruction=inst,
            context=self.context,
        )
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].name, 'HOME')
        self.assertEqual(result[0].command, '<CMD:HOME>')

    def test_compile_wait_ms(self) -> None:
        '''
            Verifies compilation of WAIT_MS command.
        '''
        inst = ScaraInstruction(
            command_type=ScaraCommandType.WAIT_MS,
            parameters={InstructionParam.MS: 500.0},
            line_number=2,
            raw_text='WAIT_MS 500',
        )
        result = self.compiler.compile(
            instruction=inst,
            context=self.context,
        )
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].name, 'WAIT_500MS')
        self.assertEqual(result[0].command, '<CMD:WAIT#500>')

    def test_compile_control_states(self) -> None:
        '''
            Verifies compilation of safety and control state commands.
        '''
        commands = (
            (ScaraCommandType.HOLD, 'HOLD', '<CMD:HOLD>'),
            (ScaraCommandType.RESUME, 'RESUME', '<CMD:RESUME>'),
            (ScaraCommandType.ESTOP, 'ESTOP', '<CMD:ESTOP>'),
            (ScaraCommandType.ENABLE, 'ENABLE', '<CMD:ENABLE>'),
            (ScaraCommandType.DISABLE, 'DISABLE', '<CMD:DISABLE>'),
        )
        for cmd_type, expected_name, expected_cmd in commands:
            inst = ScaraInstruction(
                command_type=cmd_type,
                parameters={},
                line_number=1,
                raw_text=cmd_type.value,
            )
            result = self.compiler.compile(
                instruction=inst,
                context=self.context,
            )
            self.assertEqual(len(result), 1)
            self.assertEqual(result[0].name, expected_name)
            self.assertEqual(result[0].command, expected_cmd)

    def test_compile_config_motor(self) -> None:
        '''
            Verifies compilation of CONFIG_MOTOR updates context and emits waypoint.
        '''
        inst = ScaraInstruction(
            command_type=ScaraCommandType.CONFIG_MOTOR,
            parameters={InstructionParam.MODE: 'CLOSED_LOOP'},
            line_number=3,
            raw_text='CONFIG MOTOR CLOSED_LOOP',
        )
        result = self.compiler.compile(
            instruction=inst,
            context=self.context,
        )
        self.assertEqual(self.context.motor_drive_mode, MotorDriveMode.CLOSED_LOOP)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].name, 'CONFIG_MOTOR_CLOSED_LOOP')
        self.assertEqual(result[0].command, '<CMD:CONFIG_MOTOR#CLOSED_LOOP>')

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
