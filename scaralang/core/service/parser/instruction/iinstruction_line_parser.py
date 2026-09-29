# -*- coding: UTF-8 -*-

'''
Module
    iinstruction_line_parser.py
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
    Defines structural runtime-checkable protocol IInstructionLineParser for statement line parsing.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from scaralang.core.model.dsl.ast.instruction import ScaraInstruction
from scaralang.core.model.dsl.token.scara_token import ScaraToken
from scaralang.core.service.parser.commands.icommand_parser import ICommandParser

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IInstructionLineParser(Protocol):
    '''
        Structural protocol defining contract for statement line token parsing.

        It defines:

            :attributes:
                | name - Identifier name of the line parser.
                | handlers - Registered command parser handlers.
            :methods:
                | parse_line - Parses single statement token tuple into a ScaraInstruction.
    '''

    @property
    def name(self) -> str:
        '''
            Gets the line parser identifier name.

            :return: Line parser name string.
        '''

    @property
    def handlers(self) -> tuple[ICommandParser, ...]:
        '''
            Gets the registered command handlers.

            :return: Tuple of registered ICommandParser handlers.
        '''

    def parse_line(
        self, *, tokens: tuple[ScaraToken, ...]
    ) -> ScaraInstruction:
        '''
            Parses a statement token slice into a structured ScaraInstruction AST node.

            :param tokens: Statement token tuple including command keyword.
            :return: ScaraInstruction AST node.
            :exceptions: ValueError if no registered handler recognizes the command.
        '''
