# -*- coding: UTF-8 -*-

'''
Module
    scara_lexer_test.py
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
    Unit tests for ScaraLexer implementation.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main
from unittest.mock import MagicMock, patch

from scaralang.core.model.dsl.token.scara_token_type import ScaraTokenType
from scaralang.core.model.exceptions.scara_syntax_error import ScaraSyntaxError
from scaralang.core.service.parser.lexer.scara_lexer import ScaraLexer

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.6'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestScaraLexer(TestCase):
    '''
        Test cases verifying ScaraLexer tokenization behavior.

        It defines:

            :methods:
                | test_tokenize_empty_source - Verifies tokenization of empty source.
                | test_tokenize_identifiers_and_numbers - Verifies identifiers and numbers.
                | test_tokenize_strings - Verifies double and single quoted strings.
                | test_tokenize_delimiters - Verifies equals, comma, and parentheses.
                | test_tokenize_comments - Verifies comments are ignored.
                | test_tokenize_multiline - Verifies newline handling across lines.
                | test_tokenize_mismatch_error - Verifies ValueError on invalid characters.
                | test_name_property - Verifies name property returns lexer identifier.
                | test_tokenize_match_without_lastgroup_skipped - Verifies match without lastgroup is skipped.
    '''

    def test_tokenize_empty_source(self) -> None:
        '''
            Verifies tokenization of empty source string.
        '''
        lexer = ScaraLexer()
        tokens = lexer.tokenize(source='')
        self.assertEqual(len(tokens), 1)
        self.assertEqual(tokens[0].token_type, ScaraTokenType.EOF)

    def test_tokenize_identifiers_and_numbers(self) -> None:
        '''
            Verifies identifiers and numbers tokenization.
        '''
        lexer = ScaraLexer()
        tokens = lexer.tokenize(source='MOVE_JOINT J1=90 J2=-45.5 J3=1e-3\n')
        token_types = [tok.token_type for tok in tokens]
        self.assertEqual(
            token_types,
            [
                ScaraTokenType.IDENTIFIER,
                ScaraTokenType.IDENTIFIER,
                ScaraTokenType.EQUALS,
                ScaraTokenType.NUMBER,
                ScaraTokenType.IDENTIFIER,
                ScaraTokenType.EQUALS,
                ScaraTokenType.NUMBER,
                ScaraTokenType.IDENTIFIER,
                ScaraTokenType.EQUALS,
                ScaraTokenType.NUMBER,
                ScaraTokenType.NEWLINE,
                ScaraTokenType.EOF,
            ],
        )

    def test_tokenize_strings(self) -> None:
        '''
            Verifies double and single quoted strings tokenization.
        '''
        lexer = ScaraLexer()
        tokens = lexer.tokenize(source='MSG "hello world" \'single quoted\'\n')
        token_types = [tok.token_type for tok in tokens]
        self.assertEqual(
            token_types,
            [
                ScaraTokenType.IDENTIFIER,
                ScaraTokenType.STRING,
                ScaraTokenType.STRING,
                ScaraTokenType.NEWLINE,
                ScaraTokenType.EOF,
            ],
        )

    def test_tokenize_delimiters(self) -> None:
        '''
            Verifies equals, comma, and parentheses tokenization.
        '''
        lexer = ScaraLexer()
        tokens = lexer.tokenize(source='POINT(10, 20)\n')
        token_types = [tok.token_type for tok in tokens]
        self.assertEqual(
            token_types,
            [
                ScaraTokenType.IDENTIFIER,
                ScaraTokenType.LPAREN,
                ScaraTokenType.NUMBER,
                ScaraTokenType.COMMA,
                ScaraTokenType.NUMBER,
                ScaraTokenType.RPAREN,
                ScaraTokenType.NEWLINE,
                ScaraTokenType.EOF,
            ],
        )

    def test_tokenize_comments(self) -> None:
        '''
            Verifies comments with # and ; are ignored.
        '''
        lexer = ScaraLexer()
        tokens = lexer.tokenize(source='# comment line\nMOVE ; inline comment\n')
        token_types = [tok.token_type for tok in tokens]
        self.assertEqual(
            token_types,
            [
                ScaraTokenType.IDENTIFIER,
                ScaraTokenType.NEWLINE,
                ScaraTokenType.EOF,
            ],
        )

    def test_tokenize_multiline(self) -> None:
        '''
            Verifies newline handling across multiple lines.
        '''
        lexer = ScaraLexer()
        source = 'LINE1\nLINE2\n'
        tokens = lexer.tokenize(source=source)
        self.assertEqual(len(tokens), 5)
        self.assertEqual(tokens[0].value, 'LINE1')
        self.assertEqual(tokens[1].token_type, ScaraTokenType.NEWLINE)
        self.assertEqual(tokens[2].value, 'LINE2')
        self.assertEqual(tokens[3].token_type, ScaraTokenType.NEWLINE)
        self.assertEqual(tokens[4].token_type, ScaraTokenType.EOF)

    def test_tokenize_mismatch_error(self) -> None:
        '''
            Verifies ScaraSyntaxError on invalid/unexpected character.
        '''
        lexer = ScaraLexer()
        with self.assertRaises(ScaraSyntaxError):
            lexer.tokenize(source='MOVE @INVALID\n')

    def test_name_property(self) -> None:
        '''
            Verifies name property returns lexer identifier.
        '''
        lexer = ScaraLexer()
        self.assertEqual(lexer.name, 'scara_lexer')

    def test_tokenize_match_without_lastgroup_skipped(self) -> None:
        '''
            Verifies regex match without lastgroup is skipped safely.
        '''
        mock_match = MagicMock()
        mock_match.lastgroup = None
        mock_regex = MagicMock()
        mock_regex.finditer.return_value = [mock_match]

        with patch.object(ScaraLexer, '_TOKEN_REGEX', mock_regex):
            lexer = ScaraLexer()
            tokens = lexer.tokenize(source='TEST')
            self.assertEqual(len(tokens), 1)
            self.assertEqual(tokens[0].token_type, ScaraTokenType.EOF)


if __name__ == '__main__':
    main()
