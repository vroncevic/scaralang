# -*- coding: UTF-8 -*-

'''
Module
    iscara_linter.py
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
    Defines structural runtime-checkable protocol IScaraLinter for SCARA DSL static analysis.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from scaralang.core.model.dsl.ast.program import ScaraProgram
from scaralang.core.model.dsl.diagnostic.scara_diagnostic import ScaraDiagnostic
from scaralang.core.service.linter.rules.iscara_lint_rule import IScaraLintRule

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.6'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IScaraLinter(Protocol):
    '''
        Structural protocol defining contract for static analysis of SCARA DSL AST programs.

        It defines:

            :methods:
                | rules - Returns tuple of configured lint rules.
                | lint - Performs static analysis and returns tuple of ScaraDiagnostic findings.
    '''

    @property
    def rules(self) -> tuple[IScaraLintRule, ...]:
        '''
            Returns the configured lint rules.

            :return: Tuple of IScaraLintRule instances.
            :exceptions: None.
        '''

    def lint(self, *, program: ScaraProgram) -> tuple[ScaraDiagnostic, ...]:
        '''
            Performs static analysis checks on a SCARA DSL AST program.

            :param program: Parsed ScaraProgram AST root.
            :return: Tuple of ScaraDiagnostic findings.
        '''
