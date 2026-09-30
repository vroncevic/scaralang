# -*- coding: UTF-8 -*-

'''
Module
    iscara_lint_rule.py
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
    Defines structural runtime-checkable protocol IScaraLintRule for static analysis checks.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from scaralang.core.model.dsl.ast.instruction import ScaraInstruction
from scaralang.core.model.dsl.diagnostic.scara_diagnostic import ScaraDiagnostic
from scaralang.core.model.dsl.linter.scara_lint_context import ScaraLintContext

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IScaraLintRule(Protocol):
    '''
        Structural protocol defining contracts for discrete DSL lint rules.

        It defines:

            :attributes:
                | name - Unique identifier name of the lint rule.
            :methods:
                | check - Evaluates rule for an instruction, updating context or diagnostics.
    '''

    @property
    def name(self) -> str:
        '''
            Returns the unique identifier name of the lint rule.

            :return: String identifier of the rule.
        '''

    def check(
        self,
        *,
        instruction: ScaraInstruction,
        context: ScaraLintContext,
    ) -> tuple[ScaraDiagnostic, ...]:
        '''
            Evaluates rule against the instruction node and updates simulation context.

            :param instruction: Primitive AST instruction node.
            :param context: Mutable simulation state context.
            :return: Tuple of detected ScaraDiagnostic findings.
        '''
