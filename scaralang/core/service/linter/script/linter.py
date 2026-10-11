# -*- coding: UTF-8 -*-

'''
Module
    linter.py
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
    Performs static analysis checks on SCARA DSL script text.
'''

from __future__ import annotations

from typing import Final

from scaralang.core.model.dsl.diagnostic.scara_diagnostic import ScaraDiagnostic
from scaralang.core.model.dsl.diagnostic.scara_diagnostic_severity import ScaraDiagnosticSeverity
from scaralang.core.model.exceptions.scara_error import ScaraError
from scaralang.core.model.exceptions.scara_kinematics_error import ScaraKinematicsError
from scaralang.core.model.exceptions.scara_semantic_error import ScaraSemanticError
from scaralang.core.service.linter.ilinter import ILinter
from scaralang.core.service.linter.script.dependencies import ScriptDependencies
from scaralang.core.service.parser.iparser import IScaraParser

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.8'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ScriptLinter:
    '''
        Performs static analysis checks on SCARA DSL script text.

        It defines:

            :attributes:
                | _parser - Injected AST parser protocol instance.
                | _linter - Injected AST linter protocol instance.
            :methods:
                | __init__ - Initializes linter with dependency bundle.
                | lint_script - Performs static analysis checks on DSL script.
                | get_version - Returns the linter version string.
    '''

    _parser: IScaraParser
    _linter: ILinter

    def __init__(self, *, dependencies: ScriptDependencies) -> None:
        '''
            Initializes ScriptLinter with injected dependency bundle.

            :param dependencies: Injected ScriptDependencies bundle.
            :exceptions: None.
        '''
        self._parser: Final[IScaraParser] = dependencies.parser
        self._linter: Final[ILinter] = dependencies.linter

    def lint_script(self, *, source: str) -> tuple[ScaraDiagnostic, ...]:
        '''
            Performs static analysis checks on a DSL script string.

            :param source: Raw .scara script text.
            :return: Tuple of ScaraDiagnostic findings.
            :exceptions: None.
        '''
        try:
            program = self._parser.parse(source=source)
            return self._linter.lint(program=program)

        except (ScaraError, ValueError, TypeError, KeyError) as exc:
            code: str = 'SYNTAX_ERROR'
            if isinstance(exc, ScaraSemanticError):
                code = 'SEMANTIC_ERROR'
            elif isinstance(exc, ScaraKinematicsError):
                code = 'KINEMATICS_ERROR'

            return (
                ScaraDiagnostic(
                    code=code,
                    severity=ScaraDiagnosticSeverity.ERROR,
                    message=str(exc),
                    line=1,
                    command='',
                ),
            )

    def get_version(self) -> str:
        '''
            Returns the linter version string representation.

            :return: Version string representation.
            :exceptions: None.
        '''
        return __version__
