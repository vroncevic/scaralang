# -*- coding: UTF-8 -*-

'''
Module
    instruction_line_parser.py
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
    Implementation of IInstructionLineParser dispatching and parsing statement lines.
'''

from __future__ import annotations

from collections.abc import Sequence

from scaralang.core.model.dsl.ast.instruction import ScaraInstruction
from scaralang.core.model.dsl.token.scara_token import ScaraToken
from scaralang.core.service.parser.commands.icommand_parser import ICommandParser

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class InstructionLineParser:
    '''
        Dispatches statement line tokens to registered command handlers.

        It defines:

            :attributes:
                | name - Identifier name of the line parser.
                | handlers - Registered command parser handlers.
            :methods:
                | __init__ - Initializes InstructionLineParser with registered command handlers.
                | parse_line - Parses single statement token tuple into a ScaraInstruction.
    '''

    def __init__(self, *, handlers: Sequence[ICommandParser]) -> None:
        '''
            Initializes InstructionLineParser constructor with injected command handlers.

            :param handlers: Sequence of custom ICommandParser handlers.
            :exceptions: None.
        '''
        self._handlers: tuple[ICommandParser, ...] = tuple(handlers)
        self._registry: dict[str, ICommandParser] = {}

    @property
    def name(self) -> str:
        '''
            Gets the line parser identifier name.

            :return: Line parser name string.
        '''
        return 'instruction_line_parser'

    @property
    def handlers(self) -> tuple[ICommandParser, ...]:
        '''
            Gets the registered command handlers.

            :return: Tuple of registered ICommandParser handlers.
        '''
        return self._handlers

    def parse_line(
        self, *, tokens: tuple[ScaraToken, ...]
    ) -> ScaraInstruction:
        '''
            Parses a statement token slice into a structured ScaraInstruction AST node.

            :param tokens: Statement token tuple including command keyword.
            :return: ScaraInstruction AST node.
            :exceptions: ValueError if empty tokens or no handler recognizes command.
        '''
        if not tokens:
            raise ValueError('Cannot parse empty statement token sequence')

        first_tok = tokens[0]
        cmd_name = first_tok.value.upper()
        line_num = first_tok.line
        raw_text = ' '.join(t.value for t in tokens)

        handler = None

        if cmd_name == 'CONFIG' and len(tokens) > 1:
            compound_name = f'CONFIG_{tokens[1].value.upper()}'
            handler = self._registry.get(compound_name)

            if handler is None:
                for candidate in self._handlers:
                    if candidate.can_parse(command_name=compound_name):
                        handler = candidate
                        self._registry[compound_name] = handler
                        break

        if handler is None:
            handler = self._registry.get(cmd_name)

        if handler is None:
            for candidate in self._handlers:
                if candidate.can_parse(command_name=cmd_name):
                    handler = candidate
                    self._registry[cmd_name] = handler
                    break

        if handler is None:
            raise ValueError(
                f'Unknown SCARA DSL command {cmd_name!r} at line {line_num}'
            )

        return handler.parse(
            tokens=tokens, line_num=line_num, raw_text=raw_text
        )
