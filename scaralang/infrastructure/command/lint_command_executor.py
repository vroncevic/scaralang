# -*- coding: UTF-8 -*-

'''
Module
    lint_command_executor.py
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
    Command executor for linting SCARA DSL scripts.
'''

from __future__ import annotations

from collections.abc import Mapping, Sequence
from os.path import exists

from scaralang.core.model.dsl.diagnostic.diagnostic import Diagnostic
from scaralang.core.model.dsl.diagnostic.diagnostic_severity import DiagnosticSeverity
from scaralang.core.service.dsl.diagnostic.scara_diagnostic_formatter import ScaraDiagnosticFormatter
from scaralang.core.service.dsl.iscara_dsl_service import IScaraDslService
from scaralang.infrastructure.command.icommand_definition import ICommandDefinition

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class LintCommandExecutor:
    '''
        Command executor strategy for validating .scara scripts against syntax and lint rules.

        It defines:

            :attributes:
                | definition - The command CLI metadata definition.
            :methods:
                | execute - Executes the lint command.
                | get_definition - Returns the command definition metadata.
    '''

    definition: ICommandDefinition

    def __init__(self, definition: ICommandDefinition) -> None:
        '''
            Initializes the lint command executor.

            :param definition: The command definition metadata.
            :exceptions: None.
        '''
        self.definition = definition

    def execute(
        self,
        *,
        params: Mapping[str, object],
        service: IScaraDslService
    ) -> Mapping[str, object]:
        '''
            Executes the lint subcommand.

            :param params: Subcommand parameters from CLI parser.
            :param service: SCARA DSL service instance.
            :return: The result of the subcommand execution.
            :exceptions: None.
        '''
        try:
            script_path: str | None = params.get('script')  # type: ignore[assignment]
            if not script_path or not isinstance(script_path, str) or not exists(script_path):
                return {
                    'returncode': 1,
                    'stdout': '',
                    'stderr': f'lint_command_executor: script file does not exist: {script_path}'
                }

            with open(script_path, 'r', encoding='utf-8') as f:
                source_code: str = f.read()

            diagnostics: Sequence[Diagnostic] = service.lint_script(source=source_code)
            reports = [
                ScaraDiagnosticFormatter.format_report(diagnostic=d)
                for d in diagnostics
            ]
            has_errors = any(d.severity == DiagnosticSeverity.ERROR for d in diagnostics)

            output_text = '\n'.join(reports) if reports else 'No issues found. Script is clean.'
            return {
                'returncode': 1 if has_errors else 0,
                'stdout': output_text,
                'stderr': ''
            }

        except Exception as exc:
            return {'returncode': 1, 'stdout': '', 'stderr': f'lint error: {exc}'}

    def get_definition(self) -> ICommandDefinition:
        '''
            Returns the command definition metadata.

            :return: The command definition metadata.
            :exceptions: None.
        '''
        return self.definition
