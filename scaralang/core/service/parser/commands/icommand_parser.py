# -*- coding: UTF-8 -*-

'''
Module
    icommand_parser.py
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
    Defines structural runtime-checkable protocol ICommandParser for
    parsing individual command types.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from scaralang.core.model.dsl.ast.instruction import ScaraInstruction
from scaralang.core.model.dsl.token.scara_token import ScaraToken

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class ICommandParser(Protocol):
    '''
        Structural protocol defining contract for individual SCARA DSL command parser handlers.

        It defines:

            :attributes:
                | name - Identifier name of the command parser handler.
            :methods:
                | can_parse - Checks whether handler can parse the given command name.
                | parse - Parses tokens for statement into a ScaraInstruction node.
    '''

    @property
    def name(self) -> str:
        '''
            Gets the command parser identifier name.

            :return: Parser name string.
        '''

    def can_parse(self, *, command_name: str) -> bool:
        '''
            Checks if this parser handler can process the command keyword.

            :param command_name: Uppercase command keyword name.
            :return: True if handler can parse this command, False otherwise.
        '''

    def parse(
        self,
        *,
        tokens: tuple[ScaraToken, ...],
        line_num: int,
        raw_text: str,
    ) -> ScaraInstruction:
        '''
            Parses a statement token slice into a structured ScaraInstruction AST node.

            :param tokens: Statement token tuple including command keyword.
            :param line_num: 1-indexed source line number.
            :param raw_text: Original raw line string.
            :return: ScaraInstruction AST node.
        '''
