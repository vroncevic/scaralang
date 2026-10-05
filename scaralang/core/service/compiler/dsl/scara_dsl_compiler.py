# -*- coding: UTF-8 -*-

'''
Module
    scara_dsl_compiler.py
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
    Compiles SCARA DSL source text and AST programs into validated trajectory plans.
'''

from __future__ import annotations

from typing import Final

from scaralang.core.model.dsl.ast.program import ScaraProgram
from scaralang.core.model.dsl.diagnostic.scara_diagnostic_severity import ScaraDiagnosticSeverity
from scaralang.core.model.exceptions.scara_semantic_error import ScaraSemanticError
from scaralang.core.service.compiler.plan.itrajectory_plan_compiler import ITrajectoryPlanCompiler
from scaralang.core.service.linter.iscara_linter import IScaraLinter
from scaralang.core.service.parser.iscara_parser import IScaraParser
from scaralang.core.service.trajectory.plan.itrajectory_plan import ITrajectoryPlan

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ScaraDslCompiler:
    '''
        Compiles SCARA DSL source text and AST programs into validated trajectory plans.

        It defines:

            :attributes:
                | _parser - Injected AST parser protocol instance.
                | _compiler - Injected plan compiler protocol instance.
                | _linter - Injected static analysis linter protocol instance.
            :methods:
                | __init__ - Initializes compiler with injected component protocols.
                | compile_script - Compiles DSL source text into validated ITrajectoryPlan.
                | compile_program - Compiles AST program into validated ITrajectoryPlan.
                | get_version - Returns the compiler version string.
    '''

    _parser: IScaraParser
    _compiler: ITrajectoryPlanCompiler
    _linter: IScaraLinter

    def __init__(
        self,
        *,
        parser: IScaraParser,
        compiler: ITrajectoryPlanCompiler,
        linter: IScaraLinter,
    ) -> None:
        '''
            Initializes the SCARA DSL compiler with injected subcomponents.

            :param parser: Required IScaraParser protocol instance.
            :param compiler: Required ITrajectoryPlanCompiler protocol instance.
            :param linter: Required IScaraLinter protocol instance.
            :exceptions: None.
        '''
        self._parser: Final[IScaraParser] = parser
        self._compiler: Final[ITrajectoryPlanCompiler] = compiler
        self._linter: Final[IScaraLinter] = linter

    def compile_script(self, *, source: str) -> ITrajectoryPlan:
        '''
            Compiles DSL source text into an executable and validated ITrajectoryPlan.

            :param source: Raw .scara script text.
            :return: Validated ITrajectoryPlan protocol instance.
            :exceptions: ScaraSemanticError if parsing fails or error-severity diagnostics occur.
        '''
        parsed_program = self._parser.parse(source=source)

        diagnostics = self._linter.lint(program=parsed_program)
        errors = [d for d in diagnostics if d.severity == ScaraDiagnosticSeverity.ERROR]

        if errors:
            messages = [f'Line {d.line}: {d.message}' for d in errors]
            raise ScaraSemanticError(
                f'Validation failed with {len(errors)} error(s):\n'
                + '\n'.join(messages)
            )

        return self._compiler.compile(program=parsed_program)

    def compile_program(self, *, program: ScaraProgram) -> ITrajectoryPlan:
        '''
            Compiles a parsed AST program into an executable and validated ITrajectoryPlan.

            :param program: ScaraProgram AST instance to compile.
            :return: Validated ITrajectoryPlan protocol instance.
            :exceptions: ScaraSemanticError if error-severity diagnostics occur.
        '''
        diagnostics = self._linter.lint(program=program)
        errors = [d for d in diagnostics if d.severity == ScaraDiagnosticSeverity.ERROR]

        if errors:
            messages = [f'Line {d.line}: {d.message}' for d in errors]
            raise ScaraSemanticError(
                f'Validation failed with {len(errors)} error(s):\n'
                + '\n'.join(messages)
            )

        return self._compiler.compile(program=program)

    def get_version(self) -> str:
        '''
            Returns the SCARA DSL compiler version string.

            :return: Version string.
            :exceptions: None.
        '''
        return __version__
