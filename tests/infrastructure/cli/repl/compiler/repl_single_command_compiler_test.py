# -*- coding: UTF-8 -*-

'''
Module
    repl_single_command_compiler_test.py
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
    Unit tests for ReplSingleCommandCompiler and factory.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.model.protocol.message_id import MessageId
from scaralang.core.model.repl.repl_session_context import ReplSessionContext
from scaralang.infrastructure.cli.repl.compiler.irepl_single_command_compiler import IReplSingleCommandCompiler
from scaralang.infrastructure.cli.repl.compiler.repl_single_command_compiler import ReplSingleCommandCompiler
from scaralang.infrastructure.cli.repl.compiler.repl_single_command_compiler_factory import ReplSingleCommandCompilerFactory
from scaralang.setup.factory import ScaralangBundleFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestReplSingleCommandCompiler(TestCase):
    '''
        Test cases verifying ReplSingleCommandCompiler.

        It defines:

            :methods:
                | test_compile_move_instruction - Verifies compiling Cartesian move.
                | test_compile_tool_pump_instruction - Verifies compiling pump command.
                | test_compile_home_instruction - Verifies compiling home command.
                | test_compile_invalid_instruction - Verifies error raised on syntax error.
                | test_factory_and_protocol_conformance - Verifies factory and protocol check.
    '''

    def setUp(self) -> None:
        '''Initializes service and compiler under test.'''
        bundle = ScaralangBundleFactory.create_bundle()
        self.service = bundle.service
        self.compiler = ReplSingleCommandCompiler(service=self.service)

    def test_compile_move_instruction(self) -> None:
        '''Verifies compiling Cartesian linear move instruction.'''
        context = ReplSessionContext()
        frame, step, new_ctx = self.compiler.compile_instruction(
            line='MOVE_L X=150.0 Y=50.0 Z=0.0 SPEED=100', context=context
        )
        self.assertIsNotNone(step)
        self.assertEqual(frame.msg_id, MessageId.CMD_MOVE_JOINT_STEPS)
        self.assertEqual(new_ctx.current_x, 150.0)
        self.assertEqual(new_ctx.current_y, 50.0)
        self.assertEqual(new_ctx.current_z, 0.0)

    def test_compile_tool_pump_instruction(self) -> None:
        '''Verifies compiling pneumatic tool suction command.'''
        context = ReplSessionContext(pump_active=False)
        frame, step, new_ctx = self.compiler.compile_instruction(
            line='PUMP ON', context=context
        )
        self.assertIsNotNone(step)
        self.assertEqual(frame.msg_id, MessageId.CMD_TOOL_PUMP)
        self.assertTrue(new_ctx.pump_active)

    def test_compile_home_instruction(self) -> None:
        '''Verifies compiling homing sequence resets coordinates.'''
        context = ReplSessionContext(current_x=100.0, current_y=100.0)
        frame, step, new_ctx = self.compiler.compile_instruction(
            line='HOME', context=context
        )
        self.assertIsNotNone(step)
        self.assertEqual(frame.msg_id, MessageId.CMD_HOME)
        self.assertEqual(new_ctx.current_x, 150.0)
        self.assertEqual(new_ctx.current_y, 0.0)
        self.assertEqual(new_ctx.current_z, 20.0)

    def test_compile_invalid_instruction(self) -> None:
        '''Verifies exception raised on invalid DSL instruction.'''
        context = ReplSessionContext()
        with self.assertRaises(ValueError):
            self.compiler.compile_instruction(
                line='INVALID_OPCODE FOO BAR', context=context
            )

    def test_factory_and_protocol_conformance(self) -> None:
        '''Verifies factory instantiation and protocol check.'''
        compiler = ReplSingleCommandCompilerFactory.create(service=self.service)
        self.assertTrue(isinstance(compiler, IReplSingleCommandCompiler))
        self.assertEqual(ReplSingleCommandCompilerFactory.get_version(), '1.0.1')


if __name__ == '__main__':
    main()
