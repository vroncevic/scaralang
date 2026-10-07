# -*- coding: UTF-8 -*-

'''
Module
    executor_test.py
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
from unittest.mock import MagicMock

from scaralang.infrastructure.cli.repl.compiler.repl_single_command_compiler_factory import ReplSingleCommandCompilerFactory
from scaralang.infrastructure.cli.repl.dispatch.repl_command_dispatcher_factory import ReplCommandDispatcherFactory
from scaralang.infrastructure.cli.repl.input.repl_line_reader_factory import ReplLineReaderFactory
from scaralang.infrastructure.cli.repl.presentation.repl_response_presenter_factory import ReplResponsePresenterFactory
from scaralang.infrastructure.cli.repl.transmission.repl_frame_transmitter_factory import ReplFrameTransmitterFactory
from scaralang.infrastructure.command.repl.bundle import ReplCommandBundle
from scaralang.infrastructure.command.repl.definition import ReplCommandDefinition
from scaralang.infrastructure.command.repl.executor import ReplCommandExecutor

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.7'
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
                | test_execute_empty_line_and_eof - Verifies empty lines and EOF exit.
                | test_get_definition - Verifies retrieval of command definition.
                | test_execute_with_endpoint_param - Verifies transmitter configuration from params.
    '''

    def setUp(self) -> None:
        '''Initializes shared components.'''
        self.definition = ReplCommandDefinition()

    def test_execute_interactive_session(self) -> None:
        '''Verifies executing REPL session with built-in commands and motion compilation.'''
        lines: list[str] = [
            'help',
            'status',
            'MOVE_L X=150.0 Y=50.0 Z=0.0 SPEED=100',
            'exit',
        ]
        captured: list[str] = []
        reader = MagicMock()
        reader.read_line.side_effect = lines
        dispatcher = ReplCommandDispatcherFactory.create_default()
        compiler = ReplSingleCommandCompilerFactory.create_default()
        transmitter = ReplFrameTransmitterFactory.create()
        presenter = ReplResponsePresenterFactory.create()

        writer = MagicMock()
        writer.write.side_effect = captured.append

        bundle = ReplCommandBundle(
            reader=reader,
            writer=writer,
            dispatcher=dispatcher,
            compiler=compiler,
            transmitter=transmitter,
            presenter=presenter,
        )
        executor = ReplCommandExecutor(
            definition=self.definition,
            bundle=bundle,
        )

        result = executor.execute(params={})
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
        captured: list[str] = []
        reader = MagicMock()
        reader.read_line.side_effect = lines
        dispatcher = ReplCommandDispatcherFactory.create_default()
        compiler = ReplSingleCommandCompilerFactory.create_default()
        transmitter = ReplFrameTransmitterFactory.create()
        presenter = ReplResponsePresenterFactory.create()
        writer = MagicMock()
        writer.write.side_effect = captured.append

        bundle = ReplCommandBundle(
            reader=reader,
            writer=writer,
            dispatcher=dispatcher,
            compiler=compiler,
            transmitter=transmitter,
            presenter=presenter,
        )
        executor = ReplCommandExecutor(
            definition=self.definition,
            bundle=bundle,
        )

        result = executor.execute(params={})
        self.assertEqual(result['returncode'], 0)
        output_str = '\n'.join(captured)
        self.assertIn('❌ Error:', output_str)
        self.assertIn('CMD_TOOL_PUMP', output_str)

    def test_get_definition(self) -> None:
        '''Verifies get_definition returns correct command definition.'''
        reader = ReplLineReaderFactory.create_default()
        dispatcher = ReplCommandDispatcherFactory.create_default()
        compiler = ReplSingleCommandCompilerFactory.create_default()
        transmitter = ReplFrameTransmitterFactory.create()
        presenter = ReplResponsePresenterFactory.create()

        bundle = ReplCommandBundle(
            reader=reader,
            writer=MagicMock(),
            dispatcher=dispatcher,
            compiler=compiler,
            transmitter=transmitter,
            presenter=presenter,
        )
        executor = ReplCommandExecutor(
            definition=self.definition,
            bundle=bundle,
        )
        self.assertEqual(executor.get_definition().name, 'repl')

    def test_execute_with_endpoint_param(self) -> None:
        '''Verifies execute configures transmitter from CLI endpoint parameter.'''
        reader = MagicMock()
        reader.read_line.return_value = 'exit'
        dispatcher = ReplCommandDispatcherFactory.create_default()
        compiler = ReplSingleCommandCompilerFactory.create_default()
        transmitter = ReplFrameTransmitterFactory.create()
        presenter = ReplResponsePresenterFactory.create()

        bundle = ReplCommandBundle(
            reader=reader,
            writer=MagicMock(),
            dispatcher=dispatcher,
            compiler=compiler,
            transmitter=transmitter,
            presenter=presenter,
        )
        executor = ReplCommandExecutor(
            definition=self.definition,
            bundle=bundle,
        )
        executor.execute(params={'endpoint': '/dev/ttyUSB1', 'dry_run': False})
        self.assertEqual(transmitter.get_endpoint(), '/dev/ttyUSB1')
        self.assertFalse(transmitter.is_dry_run())

    def test_execute_empty_line_and_eof(self) -> None:
        '''Verifies empty lines are skipped and EOF (None) terminates REPL session.'''
        lines: list[str | None] = ['', None]
        reader = MagicMock()
        reader.read_line.side_effect = lines
        bundle = ReplCommandBundle(
            reader=reader,
            writer=MagicMock(),
            dispatcher=ReplCommandDispatcherFactory.create_default(),
            compiler=ReplSingleCommandCompilerFactory.create_default(),
            transmitter=ReplFrameTransmitterFactory.create(),
            presenter=ReplResponsePresenterFactory.create(),
        )
        executor = ReplCommandExecutor(
            definition=self.definition,
            bundle=bundle,
        )
        result = executor.execute(params={})
        self.assertEqual(result['returncode'], 0)


if __name__ == '__main__':
    main()
