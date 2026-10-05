# -*- coding: UTF-8 -*-

'''
Module
    lexer_pattern_kind_test.py
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
    Unit tests for LexerPatternKind enumeration model.
'''

from __future__ import annotations

from unittest import TestCase, main

from scaralang.core.model.dsl.token.lexer_pattern_kind import LexerPatternKind

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class LexerPatternKindTest(TestCase):
    '''Unit tests validating LexerPatternKind enumeration members and values.'''

    def test_enumeration_members_count(self) -> None:
        '''Verify total number of defined pattern group types.'''
        self.assertEqual(len(LexerPatternKind), 10)

    def test_string_representation(self) -> None:
        '''Verify that pattern group members match expected string values.'''
        self.assertEqual(LexerPatternKind.COMMENT, 'COMMENT')
        self.assertEqual(LexerPatternKind.NUMBER, 'NUMBER')
        self.assertEqual(LexerPatternKind.STRING, 'STRING')
        self.assertEqual(LexerPatternKind.EQUALS, 'EQUALS')
        self.assertEqual(LexerPatternKind.COMMA, 'COMMA')
        self.assertEqual(LexerPatternKind.LPAREN, 'LPAREN')
        self.assertEqual(LexerPatternKind.RPAREN, 'RPAREN')
        self.assertEqual(LexerPatternKind.IDENTIFIER, 'IDENTIFIER')
        self.assertEqual(LexerPatternKind.WHITESPACE, 'WHITESPACE')
        self.assertEqual(LexerPatternKind.MISMATCH, 'MISMATCH')

    def test_lookup_by_value(self) -> None:
        '''Verify member lookup from string values.'''
        self.assertIs(LexerPatternKind('COMMENT'), LexerPatternKind.COMMENT)
        self.assertIs(LexerPatternKind('NUMBER'), LexerPatternKind.NUMBER)
        self.assertIs(LexerPatternKind('WHITESPACE'), LexerPatternKind.WHITESPACE)


if __name__ == '__main__':
    main()
