# -*- coding: UTF-8 -*-

'''
Module
    executor_factory_test.py
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
    Unit tests for ReplCommandExecutorFactory class.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.infrastructure.cli.repl.compiler.repl_single_command_compiler_factory import ReplSingleCommandCompilerFactory
from scaralang.infrastructure.cli.repl.dispatch.repl_command_dispatcher_factory import ReplCommandDispatcherFactory
from scaralang.infrastructure.cli.repl.input.repl_line_reader_factory import ReplLineReaderFactory
from scaralang.infrastructure.cli.repl.output.repl_output_writer_factory import ReplOutputWriterFactory
from scaralang.infrastructure.cli.repl.presentation.repl_response_presenter_factory import ReplResponsePresenterFactory
from scaralang.infrastructure.cli.repl.transmission.repl_frame_transmitter_factory import ReplFrameTransmitterFactory
from scaralang.infrastructure.command.repl.bundle import ReplCommandBundle
from scaralang.infrastructure.command.repl.definition import ReplCommandDefinition
from scaralang.infrastructure.command.repl.executor import ReplCommandExecutor
from scaralang.infrastructure.command.repl.executor_factory import ReplCommandExecutorFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestReplCommandExecutorFactory(TestCase):
    '''
        Test cases verifying ReplCommandExecutorFactory.

        It defines:

            :methods:
                | test_factory_create_default - Verifies default instantiation of ReplCommandExecutor.
                | test_factory_create_with_collaborators - Verifies explicit instantiation.
                | test_factory_version - Verifies factory version string.
    '''

    def test_factory_create_default(self) -> None:
        '''Verifies factory instantiates properly configured ReplCommandExecutor.'''
        executor = ReplCommandExecutorFactory.create_default()
        self.assertIsInstance(executor, ReplCommandExecutor)
        self.assertEqual(executor.get_definition().name, 'repl')

    def test_factory_create_with_collaborators(self) -> None:
        '''Verifies factory builds ReplCommandExecutor with explicit collaborators.'''
        repl_def = ReplCommandDefinition()
        bundle = ReplCommandBundle(
            reader=ReplLineReaderFactory.create_default(),
            dispatcher=ReplCommandDispatcherFactory.create_default(),
            compiler=ReplSingleCommandCompilerFactory.create_default(),
            transmitter=ReplFrameTransmitterFactory.create(),
            presenter=ReplResponsePresenterFactory.create(),
            writer=ReplOutputWriterFactory.create_default(),
        )
        executor = ReplCommandExecutorFactory.create(
            definition=repl_def,
            bundle=bundle,
        )
        self.assertIsInstance(executor, ReplCommandExecutor)
        self.assertEqual(executor.get_definition().name, 'repl')

    def test_factory_version(self) -> None:
        '''Verifies factory version.'''
        self.assertEqual(ReplCommandExecutorFactory.get_version(), '1.0.4')


if __name__ == '__main__':
    main()
