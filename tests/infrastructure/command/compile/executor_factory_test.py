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
    Unit tests for CompileCommandExecutorFactory class.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.service.compiler.scara_compiler_factory import ScaraCompilerFactory
from scaralang.infrastructure.command.compile.bundle import CompileCommandBundle
from scaralang.infrastructure.command.compile.definition import CompileCommandDefinition
from scaralang.infrastructure.command.compile.error.compile_error_handler_factory import CompileErrorHandlerFactory
from scaralang.infrastructure.command.compile.executor import CompileCommandExecutor
from scaralang.infrastructure.command.compile.executor_factory import CompileCommandExecutorFactory
from scaralang.infrastructure.command.compile.telemetry.compile_telemetry_formatter_factory import CompileTelemetryFormatterFactory
from scaralang.infrastructure.command.compile.inspection.presentation.program_inspection_presenter_factory import ProgramInspectionPresenterFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.7'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestCompileCommandExecutorFactory(TestCase):
    '''
        Test cases verifying CompileCommandExecutorFactory.

        It defines:

            :methods:
                | test_create_default - Verifies factory returns instance with defaults.
                | test_create_custom - Verifies factory returns instance with injected parameters.
                | test_get_version - Verifies factory version string.
    '''

    def test_create_default(self) -> None:
        '''Verifies factory returns CompileCommandExecutor instance with default dependencies.'''
        executor = CompileCommandExecutorFactory.create_default()
        self.assertIsInstance(executor, CompileCommandExecutor)

    def test_create_custom(self) -> None:
        '''Verifies factory returns CompileCommandExecutor instance with custom parameters.'''
        custom_def = CompileCommandDefinition()
        bundle = CompileCommandBundle(
            compiler=ScaraCompilerFactory.create_default(),
            inspection_presenter=ProgramInspectionPresenterFactory.create(),
            telemetry_formatter=CompileTelemetryFormatterFactory.create(),
            error_handler=CompileErrorHandlerFactory.create(),
        )
        executor = CompileCommandExecutorFactory.create(
            definition=custom_def,
            bundle=bundle,
        )
        self.assertIsInstance(executor, CompileCommandExecutor)
        self.assertIs(executor.get_definition(), custom_def)

    def test_get_version(self) -> None:
        '''Verifies factory version returns valid string.'''
        self.assertEqual(
            CompileCommandExecutorFactory.get_version(), '1.0.7'
        )


if __name__ == '__main__':
    main()
