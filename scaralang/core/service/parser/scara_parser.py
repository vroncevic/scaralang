# -*- coding: UTF-8 -*-

'''
Module
    scara_parser.py
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
    Implementation of IScaraParser orchestrating modular command
    parser handlers into an AST program.
'''

from __future__ import annotations

from collections.abc import Sequence
from typing import Final

from scaralang.core.model.dsl.ast.program import ScaraProgram
from scaralang.core.model.dsl.token.scara_token import ScaraToken
from scaralang.core.service.parser.instruction.iinstruction_line_parser import IInstructionLineParser
from scaralang.core.service.parser.splitter.itoken_line_splitter import ITokenLineSplitter
from scaralang.core.service.parser.lexer.iscara_lexer import IScaraLexer

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.7'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ScaraParser:
    '''
        Orchestrator parser coordinating tokenizer, line splitter, and instruction line parser.

        It defines:

            :attributes:
                | name - Identifier name of the parser.
            :methods:
                | __init__ - Initializes ScaraParser with injected components.
                | parse - Parses raw DSL source string into an ScaraProgram.
                | parse_tokens - Parses a sequence of lexical tokens into an ScaraProgram.
    '''

    _lexer: IScaraLexer
    _line_splitter: ITokenLineSplitter
    _line_parser: IInstructionLineParser

    def __init__(
        self,
        *,
        lexer: IScaraLexer,
        line_splitter: ITokenLineSplitter,
        line_parser: IInstructionLineParser,
    ) -> None:
        '''
            Initializes ScaraParser constructor with injected components.

            :param lexer: Injected IScaraLexer tokenizer component.
            :param line_splitter: Injected ITokenLineSplitter line segmenter.
            :param line_parser: Injected IInstructionLineParser line parser.
            :exceptions: None.
        '''
        self._lexer: Final[IScaraLexer] = lexer
        self._line_splitter: Final[ITokenLineSplitter] = line_splitter
        self._line_parser: Final[IInstructionLineParser] = line_parser

    @property
    def name(self) -> str:
        '''
            Gets the parser identifier name.

            :return: Parser name string.
        '''
        return 'scara_parser'

    def parse(self, *, source: str) -> ScaraProgram:
        '''
            Parses raw SCARA DSL code string into an immutable AST program representation.

            :param source: Raw source code text.
            :return: ScaraProgram instance.
            :exceptions: ValueError on syntactic parse error.
        '''
        tokens: tuple[ScaraToken, ...] = self._lexer.tokenize(source=source)

        return self.parse_tokens(tokens=tokens)

    def parse_tokens(self, *, tokens: Sequence[ScaraToken]) -> ScaraProgram:
        '''
            Parses a sequence of lexical tokens into an immutable AST program representation.

            :param tokens: Sequence of ScaraToken instances.
            :return: ScaraProgram instance.
            :exceptions: ValueError on syntactic parse error.
        '''
        lines = self._line_splitter.split_lines(tokens=tokens)
        instructions = tuple(
            self._line_parser.parse_line(tokens=line) for line in lines
        )

        return ScaraProgram(instructions=instructions)
