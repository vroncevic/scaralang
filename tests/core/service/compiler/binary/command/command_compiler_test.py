# -*- coding: UTF-8 -*-

'''
Module
    command_compiler_test.py
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
    Unit tests for CommandCompiler.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.model.dsl.binary.step import Step
from scaralang.core.model.exceptions.scara_semantic_error import ScaraSemanticError
from scaralang.core.model.protocol.message_id import MessageId
from scaralang.core.service.compiler.binary.command.command_compiler_factory import CommandCompilerFactory
from scaralang.core.service.compiler.binary.command.icommand_compiler import ICommandCompiler
from scaralang.core.service.protocol.ibinary_frame_builder import IBinaryFrameBuilder
from scaralang.infrastructure.communication.protocol.binary.builder.binary_frame_builder_factory import BinaryFrameBuilderFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.7'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestCommandCompiler(TestCase):
    '''
        Test cases verifying CommandCompiler execution and step generation.

        It defines:

            :methods:
                | setUp - Initializes compiler fixture.
                | test_structural_conformance - Verifies protocol check.
                | test_get_version - Verifies get_version returns valid version string.
                | test_compile_pump_command - Tests compiling PUMP command.
                | test_compile_valve_command - Tests compiling VALVE command.
                | test_compile_wait_command - Tests compiling WAIT command.
                | test_compile_system_command - Tests compiling HOME system command.
                | test_compile_unknown_command - Tests ScaraSemanticError on unknown command.
    '''

    def setUp(self) -> None:
        '''
            Sets up CommandCompiler fixture.
        '''
        frame_builder: IBinaryFrameBuilder = BinaryFrameBuilderFactory.create()
        self.compiler: ICommandCompiler = CommandCompilerFactory.create(
            frame_builder=frame_builder
        )

    def test_structural_conformance(self) -> None:
        '''
            Verifies structural conformance to ICommandCompiler.
        '''
        self.assertIsInstance(self.compiler, ICommandCompiler)

    def test_get_version(self) -> None:
        '''
            Verifies get_version returns valid version string.
        '''
        self.assertEqual(self.compiler.get_version(), '1.0.7')


    def test_compile_pump_command(self) -> None:
        '''
            Verifies compiling PUMP ON command.
        '''
        step: Step = self.compiler.compile_command_step(
            command='PUMP ON',
            seq_num=1,
            line_num=10,
        )
        self.assertEqual(step.frame.msg_id, MessageId.CMD_TOOL_PUMP)
        self.assertEqual(step.frame.seq_num, 1)
        self.assertEqual(step.line_number, 10)

    def test_compile_valve_command(self) -> None:
        '''
            Verifies compiling VALVE 0 command.
        '''
        step: Step = self.compiler.compile_command_step(
            command='VALVE 0',
            seq_num=2,
            line_num=11,
        )
        self.assertEqual(step.frame.msg_id, MessageId.CMD_TOOL_VALVE)
        self.assertEqual(step.frame.seq_num, 2)
        self.assertEqual(step.line_number, 11)

    def test_compile_wait_command(self) -> None:
        '''
            Verifies compiling WAIT 500 command.
        '''
        step: Step = self.compiler.compile_command_step(
            command='<CMD:WAIT#500>',
            seq_num=3,
            line_num=12,
        )
        self.assertEqual(step.frame.msg_id, MessageId.CMD_WAIT)
        self.assertEqual(step.frame.seq_num, 3)
        self.assertEqual(step.line_number, 12)

    def test_compile_system_command(self) -> None:
        '''
            Verifies compiling HOME system command.
        '''
        step: Step = self.compiler.compile_command_step(
            command='<CMD:HOME>',
            seq_num=4,
            line_num=13,
        )
        self.assertEqual(step.frame.msg_id, MessageId.CMD_HOME)
        self.assertEqual(step.frame.seq_num, 4)

    def test_compile_motor_config_command(self) -> None:
        '''
            Verifies compiling CONFIG_MOTOR command generates CMD_CONFIG_MOTOR frame.
        '''
        step: Step = self.compiler.compile_command_step(
            command='<CMD:CONFIG_MOTOR#CLOSED_LOOP>',
            seq_num=5,
            line_num=14,
        )
        self.assertEqual(step.frame.msg_id, MessageId.CMD_CONFIG_MOTOR)
        self.assertEqual(step.frame.seq_num, 5)
        self.assertEqual(step.line_number, 14)

    def test_compile_unknown_command(self) -> None:
        '''
            Verifies unknown command raises ScaraSemanticError.
        '''
        with self.assertRaises(ScaraSemanticError):
            self.compiler.compile_command_step(
                command='<CMD:UNKNOWN>',
                seq_num=6,
                line_num=15,
            )


if __name__ == '__main__':
    main()
