# -*- coding: UTF-8 -*-

'''
Module
    scara_linter.py
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
    Static analysis and diagnostic linter verifying safety, sequencing,
    and coherence in SCARA DSL programs.
'''

from __future__ import annotations

from collections.abc import Sequence
from typing import Final

from scaralang.core.model.dsl.ast.program import ScaraProgram
from scaralang.core.model.dsl.diagnostic.scara_diagnostic import ScaraDiagnostic
from scaralang.core.model.dsl.diagnostic.scara_diagnostic_code import ScaraDiagnosticCode
from scaralang.core.model.dsl.diagnostic.scara_diagnostic_severity import ScaraDiagnosticSeverity
from scaralang.core.model.dsl.linter.scara_lint_context import ScaraLintContext
from scaralang.core.service.linter.rules.iscara_lint_rule import IScaraLintRule

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.7'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ScaraLinter:
    '''
        Static analyzer orchestrating rule evaluations across SCARA DSL AST programs.

        It defines:

            :attributes:
                | _rules - Sequence of registered IScaraLintRule components.
            :methods:
                | __init__ - Initializes ScaraLinter with injected lint rules.
                | rules - Returns tuple of configured lint rules.
                | lint - Performs static analysis and returns tuple of ScaraDiagnostic findings.
    '''

    _rules: tuple[IScaraLintRule, ...]

    def __init__(self, *, rules: Sequence[IScaraLintRule]) -> None:
        '''
            Initializes ScaraLinter with injected lint rules.

            :param rules: Sequence of IScaraLintRule components.
            :exceptions: None.
        '''
        self._rules: Final[tuple[IScaraLintRule, ...]] = tuple(rules)

    @property
    def rules(self) -> tuple[IScaraLintRule, ...]:
        '''
            Returns the configured lint rules.

            :return: Tuple of IScaraLintRule instances.
            :exceptions: None.
        '''
        return self._rules

    def lint(self, *, program: ScaraProgram) -> tuple[ScaraDiagnostic, ...]:
        '''
            Performs static analysis checks on a SCARA DSL AST program.

            :param program: Parsed ScaraProgram AST root.
            :return: Tuple of ScaraDiagnostic findings.
            :exceptions: None.
        '''
        diagnostics: list[ScaraDiagnostic] = []
        instructions = program.instructions

        if not instructions:
            diagnostics.append(
                ScaraDiagnostic(
                    code=ScaraDiagnosticCode.EMPTY_PROGRAM,
                    severity=ScaraDiagnosticSeverity.ERROR,
                    message='Program contains no executable instructions.',
                    line=1,
                    command='',
                )
            )

            return tuple(diagnostics)

        context = ScaraLintContext()

        for inst in instructions:
            for rule in self._rules:
                diagnostics.extend(
                    rule.check(
                        instruction=inst,
                        context=context,
                    )
                )

        return tuple(diagnostics)
