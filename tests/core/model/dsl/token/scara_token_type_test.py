# -*- coding: UTF-8 -*-

'''
Module
    scara_token_type_test.py
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
    Unit tests for ScaraTokenType enumeration model.
'''

from __future__ import annotations

from unittest import TestCase, main

from scaralang.core.model.dsl.token.scara_token_type import ScaraTokenType

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ScaraTokenTypeTest(TestCase):
    '''Unit tests validating ScaraTokenType enumeration members and values.'''

    def test_enumeration_members_count(self) -> None:
        '''Verify total number of defined DSL token types.'''
        self.assertEqual(len(ScaraTokenType), 11)

    def test_string_representation(self) -> None:
        '''Verify that token type members match expected string representations.'''
        self.assertEqual(ScaraTokenType.KEYWORD, 'KEYWORD')
        self.assertEqual(ScaraTokenType.IDENTIFIER, 'IDENTIFIER')
        self.assertEqual(ScaraTokenType.NUMBER, 'NUMBER')
        self.assertEqual(ScaraTokenType.STRING, 'STRING')
        self.assertEqual(ScaraTokenType.EQUALS, 'EQUALS')
        self.assertEqual(ScaraTokenType.COMMA, 'COMMA')
        self.assertEqual(ScaraTokenType.LPAREN, 'LPAREN')
        self.assertEqual(ScaraTokenType.RPAREN, 'RPAREN')
        self.assertEqual(ScaraTokenType.COMMENT, 'COMMENT')
        self.assertEqual(ScaraTokenType.NEWLINE, 'NEWLINE')
        self.assertEqual(ScaraTokenType.EOF, 'EOF')

    def test_lookup_by_value(self) -> None:
        '''Verify member lookup from string values.'''
        self.assertIs(ScaraTokenType('KEYWORD'), ScaraTokenType.KEYWORD)
        self.assertIs(ScaraTokenType('EOF'), ScaraTokenType.EOF)

    def test_invalid_token_type_raises_value_error(self) -> None:
        '''Verify that invalid token type raises ValueError.'''
        with self.assertRaises(ValueError):
            ScaraTokenType('UNKNOWN')


if __name__ == '__main__':
    main()
