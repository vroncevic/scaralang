# -*- coding: UTF-8 -*-

'''
Module
    lexer_pattern_kind.py
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
    Defines LexerPatternKind enumeration representing regex pattern groups in the SCARA lexer.
'''

from __future__ import annotations

from enum import StrEnum, unique

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@unique
class LexerPatternKind(StrEnum):
    '''
        Regex named capture groups for the SCARA lexical scanner.

        It defines:

            :attributes:
                | COMMENT - Comment pattern group.
                | NUMBER - Numerical literal pattern group.
                | STRING - Quoted string pattern group.
                | EQUALS - Equals delimiter pattern group.
                | COMMA - Comma separator pattern group.
                | LPAREN - Left parenthesis pattern group.
                | RPAREN - Right parenthesis pattern group.
                | IDENTIFIER - Identifier pattern group.
                | WHITESPACE - Whitespace ignore group.
                | MISMATCH - Catch-all mismatch pattern group.
    '''

    COMMENT = 'COMMENT'
    NUMBER = 'NUMBER'
    STRING = 'STRING'
    EQUALS = 'EQUALS'
    COMMA = 'COMMA'
    LPAREN = 'LPAREN'
    RPAREN = 'RPAREN'
    IDENTIFIER = 'IDENTIFIER'
    WHITESPACE = 'WHITESPACE'
    MISMATCH = 'MISMATCH'
