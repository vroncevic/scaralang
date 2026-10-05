# -*- coding: UTF-8 -*-

'''
Module
    iscara_parser.py
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
    Defines structural runtime-checkable protocol IScaraParser for parsing SCARA DSL tokens.
'''

from __future__ import annotations

from collections.abc import Sequence
from typing import Protocol, runtime_checkable

from scaralang.core.model.dsl.ast.program import ScaraProgram
from scaralang.core.model.dsl.token.scara_token import ScaraToken

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IScaraParser(Protocol):
    '''
        Structural protocol defining contract for SCARA DSL syntactic parsing.

        It defines:

            :attributes:
                | name - Identifier name of the parser.
            :methods:
                | parse - Parses raw DSL source string into a Program AST.
                | parse_tokens - Parses a sequence of lexical tokens into a Program AST.
    '''

    @property
    def name(self) -> str:
        '''
            Gets the parser identifier name.

            :return: Parser name string.
        '''

    def parse(self, *, source: str) -> ScaraProgram:
        '''
            Parses raw SCARA DSL code string into an immutable AST program representation.

            :param source: Raw source code text.
            :return: Program instance.
        '''

    def parse_tokens(self, *, tokens: Sequence[ScaraToken]) -> ScaraProgram:
        '''
            Parses a sequence of lexical tokens into an immutable AST program representation.

            :param tokens: Sequence of ScaraToken instances.
            :return: Program instance.
        '''
