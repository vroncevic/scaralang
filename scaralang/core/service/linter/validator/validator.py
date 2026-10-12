# -*- coding: UTF-8 -*-

'''
Module
    validator.py
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
    Validates syntax, static analysis safety rules, and kinematics of SCARA scripts.
'''

from __future__ import annotations

from typing import Final

from scaralang.core.model.dsl.diagnostic.scara_diagnostic_severity import ScaraDiagnosticSeverity
from scaralang.core.model.exceptions.scara_error import ScaraError
from scaralang.core.service.compiler.plan.ast.icompiler import IAstPlanCompiler
from scaralang.core.service.linter.ilinter import ILinter
from scaralang.core.service.linter.validator.dependencies import ValidatorDependencies
from scaralang.core.service.parser.iparser import IScaraParser

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.8'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ScriptValidator:
    '''
        Validates syntax, static analysis rules, and kinematics of SCARA scripts.

        It defines:

            :attributes:
                | _parser - Injected AST parser protocol instance.
                | _compiler - Injected plan compiler protocol instance.
                | _linter - Injected static analysis linter protocol instance.
            :methods:
                | __init__ - Initializes validator with dependency bundle.
                | validate_script - Validates syntax and kinematics of a DSL script.
                | get_version - Returns the validator version string.
    '''

    _parser: IScaraParser
    _linter: ILinter
    _compiler: IAstPlanCompiler

    def __init__(self, *, dependencies: ValidatorDependencies) -> None:
        '''
            Initializes ScriptValidator with injected dependency bundle.

            :param dependencies: Injected ValidatorDependencies bundle.
            :exceptions: None.
        '''
        self._parser: Final[IScaraParser] = dependencies.parser
        self._linter: Final[ILinter] = dependencies.linter
        self._compiler: Final[IAstPlanCompiler] = dependencies.compiler

    def validate_script(self, *, source: str) -> tuple[bool, list[str]]:
        '''
            Checks syntax, static analysis rules, and kinematics of a DSL script.

            :param source: Raw .scara script text.
            :return: Tuple of (is_valid boolean, list of error message strings).
            :exceptions: None.
        '''
        messages: list[str] = []

        try:
            program = self._parser.parse(source=source)
            diagnostics = self._linter.lint(program=program)

            for diag in diagnostics:
                location: str = (
                    f'Line {diag.line}: ' if diag.line > 0 else ''
                )
                messages.append(
                    f'[{diag.severity.name}] {location}[{diag.code}] {diag.message}'
                )

            has_errors: bool = any(
                d.severity == ScaraDiagnosticSeverity.ERROR
                for d in diagnostics
            )

            if has_errors:
                return False, messages

            plan = self._compiler.compile(program=program)
            messages.append(
                f'Validation PASSED: {len(program.instructions)} instructions, '
                f'{plan.count} waypoints generated.'
            )

            return True, messages

        except (ScaraError, ValueError, TypeError, KeyError) as exc:
            messages.append(f'Validation failed: {exc}')
            return False, messages

    def get_version(self) -> str:
        '''
            Returns the validator version string representation.

            :return: Version string representation.
            :exceptions: None.
        '''
        return __version__
