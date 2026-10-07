# -*- coding: UTF-8 -*-

'''
Module
    scara_lexer.py
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
    Implementation of IScaraLexer converting SCARA DSL source text into atomic tokens.
'''

from __future__ import annotations

from collections.abc import Mapping
from re import compile as re_compile, Pattern
from typing import ClassVar

from scaralang.core.model.dsl.token.lexer_pattern_kind import LexerPatternKind
from scaralang.core.model.dsl.token.scara_token import ScaraToken
from scaralang.core.model.dsl.token.scara_token_type import ScaraTokenType
from scaralang.core.model.exceptions.scara_syntax_error import ScaraSyntaxError

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.7'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ScaraLexer:
    '''
        Concrete lexer implementation converting SCARA DSL text into stream of tokens.

        It defines:

            :attributes:
                | _TOKEN_REGEX - Compiled regular expression matching DSL lexical entities.
                | _PATTERN_TO_TOKEN_TYPE - Mapping of pattern kinds to token types.
                | name - Identifier name of the lexer.
            :methods:
                | tokenize - Tokenizes raw source code into an immutable tuple of lexical tokens.
    '''

    _TOKEN_REGEX: ClassVar[Pattern[str]] = re_compile(
        rf'(?P<{LexerPatternKind.COMMENT.value}>[#;].*$)|'
        rf'(?P<{LexerPatternKind.NUMBER.value}>[-+]?(?:\d*\.\d+|\d+)(?:[eE][-+]?\d+)?)|'
        rf'(?P<{LexerPatternKind.STRING.value}>"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\')|'
        rf'(?P<{LexerPatternKind.EQUALS.value}>=)|'
        rf'(?P<{LexerPatternKind.COMMA.value}>,)|'
        rf'(?P<{LexerPatternKind.LPAREN.value}>\()|'
        rf'(?P<{LexerPatternKind.RPAREN.value}>\))|'
        rf'(?P<{LexerPatternKind.IDENTIFIER.value}>[A-Za-z_][A-Za-z0-9_]*)|'
        rf'(?P<{LexerPatternKind.WHITESPACE.value}>[^\S\n\r]+)|'
        rf'(?P<{LexerPatternKind.MISMATCH.value}>.)'
    )

    _PATTERN_TO_TOKEN_TYPE: ClassVar[Mapping[LexerPatternKind, ScaraTokenType]] = {
        LexerPatternKind.NUMBER: ScaraTokenType.NUMBER,
        LexerPatternKind.STRING: ScaraTokenType.STRING,
        LexerPatternKind.EQUALS: ScaraTokenType.EQUALS,
        LexerPatternKind.COMMA: ScaraTokenType.COMMA,
        LexerPatternKind.LPAREN: ScaraTokenType.LPAREN,
        LexerPatternKind.RPAREN: ScaraTokenType.RPAREN,
        LexerPatternKind.IDENTIFIER: ScaraTokenType.IDENTIFIER,
    }

    @property
    def name(self) -> str:
        '''
            Gets the lexer identifier name.

            :return: Lexer name string.
        '''
        return 'scara_lexer'

    def tokenize(self, *, source: str) -> tuple[ScaraToken, ...]:
        '''
            Tokenizes source text into a tuple of ScaraToken instances.

            :param source: Raw source code string.
            :return: Immutable tuple of ScaraToken tokens.
            :exceptions: ScaraSyntaxError if an illegal/unrecognized character is encountered.
        '''
        tokens: list[ScaraToken] = []
        lines: list[str] = source.splitlines()

        for line_idx, line in enumerate(lines, start=1):
            line_has_tokens = False

            for match in self._TOKEN_REGEX.finditer(line):
                kind_str = match.lastgroup

                if kind_str is None:
                    continue

                pattern_kind = LexerPatternKind(kind_str)
                val = match.group()
                col = match.start() + 1

                if pattern_kind in (LexerPatternKind.WHITESPACE, LexerPatternKind.COMMENT):
                    continue

                if pattern_kind is LexerPatternKind.MISMATCH:
                    raise ScaraSyntaxError(
                        f'Syntax error: Unexpected character {val!r} '
                        f'at line {line_idx}, column {col}'
                    )

                token_type = self._PATTERN_TO_TOKEN_TYPE.get(
                    pattern_kind, ScaraTokenType.IDENTIFIER
                )

                tokens.append(
                    ScaraToken(
                        token_type=token_type,
                        value=val,
                        line=line_idx,
                        column=col,
                    )
                )
                line_has_tokens = True

            if line_has_tokens:
                tokens.append(
                    ScaraToken(
                        token_type=ScaraTokenType.NEWLINE,
                        value='\n',
                        line=line_idx,
                        column=len(line) + 1,
                    )
                )

        tokens.append(
            ScaraToken(
                token_type=ScaraTokenType.EOF,
                value='',
                line=len(lines) + 1,
                column=1,
            )
        )

        return tuple(tokens)
