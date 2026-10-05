# -*- coding: UTF-8 -*-

'''
Module
    executor_factory.py
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
    Factory instantiating LintCommandExecutor instances.
'''

from __future__ import annotations

from scaralang.core.service.linter.diagnostic.iscara_diagnostic_formatter import IScaraDiagnosticFormatter
from scaralang.core.service.linter.diagnostic.scara_diagnostic_formatter_factory import ScaraDiagnosticFormatterFactory
from scaralang.core.service.linter.script.iscara_dsl_linter import IScaraDslLinter
from scaralang.core.service.linter.script.scara_script_validator_factory import ScaraScriptValidatorFactory
from scaralang.infrastructure.command.icommand_definition import ICommandDefinition
from scaralang.infrastructure.command.lint.definition import LintCommandDefinition
from scaralang.infrastructure.command.lint.error.ilint_error_handler import ILintErrorHandler
from scaralang.infrastructure.command.lint.error.lint_error_handler_factory import LintErrorHandlerFactory
from scaralang.infrastructure.command.lint.executor import LintCommandExecutor

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class LintCommandExecutorFactory:
    '''
        Factory providing LintCommandExecutor instances.

        It defines:

            :methods:
                | create - Builds LintCommandExecutor with injected dependencies.
                | create_default - Builds LintCommandExecutor with default dependencies.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(
        cls,
        *,
        definition: ICommandDefinition,
        service: IScaraDslLinter,
        diagnostic_formatter: IScaraDiagnosticFormatter,
        error_handler: ILintErrorHandler,
    ) -> LintCommandExecutor:
        '''
            Builds and returns a LintCommandExecutor with strictly injected dependencies.

            :param definition: Required ICommandDefinition protocol instance.
            :param service: Required IScaraDslLinter protocol instance.
            :param diagnostic_formatter: Required IScaraDiagnosticFormatter protocol instance.
            :param error_handler: Required ILintErrorHandler protocol instance.
            :return: Fully wired LintCommandExecutor instance.
            :exceptions: None.
        '''
        return LintCommandExecutor(
            definition=definition,
            service=service,
            diagnostic_formatter=diagnostic_formatter,
            error_handler=error_handler,
        )

    @classmethod
    def create_default(cls) -> LintCommandExecutor:
        '''
            Builds and returns a LintCommandExecutor instance with default dependencies.

            :return: Fully wired LintCommandExecutor instance.
            :exceptions: None.
        '''
        return LintCommandExecutor(
            definition=LintCommandDefinition(),
            service=ScaraScriptValidatorFactory.create_default(),
            diagnostic_formatter=ScaraDiagnosticFormatterFactory.create(),
            error_handler=LintErrorHandlerFactory.create(),
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory version string.

            :return: Factory version string.
            :exceptions: None.
        '''
        return __version__
