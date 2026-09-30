# -*- coding: UTF-8 -*-

'''
Module
    repl_command_executor_test.py
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
    Unit tests for ReplCommandExecutor class.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.infrastructure.cli.repl.compiler.repl_single_command_compiler_factory import ReplSingleCommandCompilerFactory
from scaralang.infrastructure.cli.repl.dispatch.repl_command_dispatcher_factory import ReplCommandDispatcherFactory
from scaralang.infrastructure.cli.repl.input.repl_line_reader import ReplLineReader
from scaralang.infrastructure.cli.repl.input.repl_line_reader_factory import ReplLineReaderFactory
from scaralang.infrastructure.cli.repl.presentation.repl_response_presenter_factory import ReplResponsePresenterFactory
from scaralang.infrastructure.cli.repl.transmission.repl_frame_transmitter_factory import ReplFrameTransmitterFactory
from scaralang.infrastructure.command.repl.repl_command_definition import ReplCommandDefinition
from scaralang.infrastructure.command.repl.repl_command_executor import ReplCommandExecutor
from scaralang.setup.factory import ScaralangBundleFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestReplCommandExecutor(TestCase):
    '''
        Test cases verifying ReplCommandExecutor.

        It defines:

            :methods:
                | test_execute_interactive_session - Verifies complete REPL session lifecycle.
                | test_execute_with_error_and_recovery - Verifies error recovery in REPL loop.
                | test_get_definition - Verifies retrieval of command definition.
    '''

    def setUp(self) -> None:
        '''Initializes service and shared components.'''
        bundle = ScaralangBundleFactory.create_bundle()
        self.service = bundle.service
        self.definition = ReplCommandDefinition()

    def test_execute_interactive_session(self) -> None:
        '''Verifies executing REPL session with built-in commands and motion compilation.'''
        lines: list[str] = [
            'help',
            'status',
            'MOVE_L X=150.0 Y=50.0 Z=0.0 SPEED=100',
            'exit',
        ]
        line_idx: int = 0

        def scripted_input(_: str) -> str:
            nonlocal line_idx

            if line_idx < len(lines):
                val = lines[line_idx]
                line_idx += 1
                return val

            return 'exit'

        captured: list[str] = []
        reader = ReplLineReader(reader_func=scripted_input)
        dispatcher = ReplCommandDispatcherFactory.create()
        compiler = ReplSingleCommandCompilerFactory.create(service=self.service)
        transmitter = ReplFrameTransmitterFactory.create()
        presenter = ReplResponsePresenterFactory.create()

        executor = ReplCommandExecutor(
            definition=self.definition,
            reader=reader,
            dispatcher=dispatcher,
            compiler=compiler,
            transmitter=transmitter,
            presenter=presenter,
            output_func=captured.append,
        )

        result = executor.execute(params={}, service=self.service)
        self.assertEqual(result['returncode'], 0)
        self.assertTrue(len(transmitter.transmitted_frames) > 0)
        output_str = '\n'.join(captured)
        self.assertIn('SCARA Robotics Interactive Motion Console', output_str)
        self.assertIn('Built-in REPL Commands', output_str)
        self.assertIn('Executed: MOVE X=150.0 Y=50.0 Z=0.0', output_str)
        self.assertIn('Terminating SCARA REPL session', output_str)

    def test_execute_with_error_and_recovery(self) -> None:
        '''Verifies REPL catches syntax error and continues to next instruction.'''
        lines: list[str] = [
            'INVALID SYNTAX ERROR LINE',
            'PUMP ON',
            'exit',
        ]
        line_idx: int = 0

        def scripted_input(_: str) -> str:
            nonlocal line_idx
            if line_idx < len(lines):
                val = lines[line_idx]
                line_idx += 1
                return val
            return 'exit'

        captured: list[str] = []
        reader = ReplLineReader(reader_func=scripted_input)
        dispatcher = ReplCommandDispatcherFactory.create()
        compiler = ReplSingleCommandCompilerFactory.create(service=self.service)
        transmitter = ReplFrameTransmitterFactory.create()
        presenter = ReplResponsePresenterFactory.create()

        executor = ReplCommandExecutor(
            definition=self.definition,
            reader=reader,
            dispatcher=dispatcher,
            compiler=compiler,
            transmitter=transmitter,
            presenter=presenter,
            output_func=captured.append,
        )

        result = executor.execute(params={}, service=self.service)
        self.assertEqual(result['returncode'], 0)
        output_str = '\n'.join(captured)
        self.assertIn('❌ Error:', output_str)
        self.assertIn('CMD_TOOL_PUMP', output_str)

    def test_get_definition(self) -> None:
        '''Verifies get_definition returns correct command definition.'''
        reader = ReplLineReaderFactory.create_default()
        dispatcher = ReplCommandDispatcherFactory.create()
        compiler = ReplSingleCommandCompilerFactory.create(service=self.service)
        transmitter = ReplFrameTransmitterFactory.create()
        presenter = ReplResponsePresenterFactory.create()

        executor = ReplCommandExecutor(
            definition=self.definition,
            reader=reader,
            dispatcher=dispatcher,
            compiler=compiler,
            transmitter=transmitter,
            presenter=presenter,
            output_func=lambda _: None,
        )
        self.assertEqual(executor.get_definition().name, 'repl')


if __name__ == '__main__':
    main()
