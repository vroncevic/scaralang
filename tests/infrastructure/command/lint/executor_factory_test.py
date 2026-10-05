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
    Unit tests for LintCommandExecutorFactory class.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.service.linter.diagnostic.scara_diagnostic_formatter_factory import ScaraDiagnosticFormatterFactory
from scaralang.core.service.linter.script.scara_script_validator_factory import ScaraScriptValidatorFactory
from scaralang.infrastructure.command.lint.definition import LintCommandDefinition
from scaralang.infrastructure.command.lint.error.lint_error_handler_factory import LintErrorHandlerFactory
from scaralang.infrastructure.command.lint.executor import LintCommandExecutor
from scaralang.infrastructure.command.lint.executor_factory import LintCommandExecutorFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestLintCommandExecutorFactory(TestCase):
    '''
        Test cases verifying LintCommandExecutorFactory.

        It defines:

            :methods:
                | test_create_default - Verifies factory returns default LintCommandExecutor.
                | test_create_with_collaborators - Verifies factory builds with injected collaborators.
                | test_get_version - Verifies factory version string.
    '''

    def test_create_default(self) -> None:
        '''Verifies factory returns default LintCommandExecutor instance.'''
        executor = LintCommandExecutorFactory.create_default()
        self.assertIsInstance(executor, LintCommandExecutor)

    def test_create_with_collaborators(self) -> None:
        '''Verifies factory builds LintCommandExecutor with explicit collaborators.'''
        definition = LintCommandDefinition()
        formatter = ScaraDiagnosticFormatterFactory.create()
        service = ScaraScriptValidatorFactory.create_default()
        error_handler = LintErrorHandlerFactory.create()
        executor = LintCommandExecutorFactory.create(
            definition=definition,
            service=service,
            diagnostic_formatter=formatter,
            error_handler=error_handler,
        )
        self.assertIsInstance(executor, LintCommandExecutor)
        self.assertEqual(executor.get_definition().name, definition.name)

    def test_get_version(self) -> None:
        '''Verifies factory version returns valid string.'''
        self.assertEqual(
            LintCommandExecutorFactory.get_version(), '1.0.4'
        )


if __name__ == '__main__':
    main()
