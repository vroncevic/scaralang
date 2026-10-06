# -*- coding: UTF-8 -*-

'''
Module
    token_line_splitter_test.py
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
    Unit tests for TokenLineSplitter implementation.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.model.dsl.token.scara_token import ScaraToken
from scaralang.core.model.dsl.token.scara_token_type import ScaraTokenType
from scaralang.core.service.parser.splitter.token_line_splitter import TokenLineSplitter

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.6'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestTokenLineSplitter(TestCase):
    '''
        Test cases verifying TokenLineSplitter line segmentation.

        It defines:

            :methods:
                | test_split_empty_tokens - Verifies empty tokens sequence.
                | test_split_single_line - Verifies single line splitting.
                | test_split_multiple_lines - Verifies multiline splitting by NEWLINE.
                | test_split_without_trailing_delimiter - Verifies line without trailing delimiter.
                | test_name_property - Verifies name property.
    '''

    def test_split_empty_tokens(self) -> None:
        '''
            Verifies that empty token sequence produces empty lines tuple.
        '''
        splitter = TokenLineSplitter()
        lines = splitter.split_lines(tokens=())
        self.assertEqual(lines, ())

    def test_split_single_line(self) -> None:
        '''
            Verifies single line terminated by NEWLINE and EOF.
        '''
        splitter = TokenLineSplitter()
        tok1 = ScaraToken(
            token_type=ScaraTokenType.IDENTIFIER, value='MOVE', line=1, column=1
        )
        tok_nl = ScaraToken(
            token_type=ScaraTokenType.NEWLINE, value='\n', line=1, column=5
        )
        tok_eof = ScaraToken(
            token_type=ScaraTokenType.EOF, value='', line=2, column=1
        )
        lines = splitter.split_lines(tokens=(tok1, tok_nl, tok_eof))
        self.assertEqual(len(lines), 1)
        self.assertEqual(lines[0], (tok1,))

    def test_split_multiple_lines(self) -> None:
        '''
            Verifies multiple lines segmented by NEWLINE tokens.
        '''
        splitter = TokenLineSplitter()
        tok1 = ScaraToken(
            token_type=ScaraTokenType.IDENTIFIER, value='LINE1', line=1, column=1
        )
        tok_nl1 = ScaraToken(
            token_type=ScaraTokenType.NEWLINE, value='\n', line=1, column=6
        )
        tok2 = ScaraToken(
            token_type=ScaraTokenType.IDENTIFIER, value='LINE2', line=2, column=1
        )
        tok_nl2 = ScaraToken(
            token_type=ScaraTokenType.NEWLINE, value='\n', line=2, column=6
        )
        tok_eof = ScaraToken(
            token_type=ScaraTokenType.EOF, value='', line=3, column=1
        )
        lines = splitter.split_lines(
            tokens=(tok1, tok_nl1, tok2, tok_nl2, tok_eof)
        )
        self.assertEqual(len(lines), 2)
        self.assertEqual(lines[0], (tok1,))
        self.assertEqual(lines[1], (tok2,))

    def test_split_without_trailing_delimiter(self) -> None:
        '''
            Verifies tokens without trailing delimiter are captured as a line.
        '''
        splitter = TokenLineSplitter()
        tok1 = ScaraToken(
            token_type=ScaraTokenType.IDENTIFIER, value='TEST', line=1, column=1
        )
        lines = splitter.split_lines(tokens=(tok1,))
        self.assertEqual(len(lines), 1)
        self.assertEqual(lines[0], (tok1,))

    def test_name_property(self) -> None:
        '''
            Verifies name property returns expected identifier.
        '''
        splitter = TokenLineSplitter()
        self.assertEqual(splitter.name, 'token_line_splitter')


if __name__ == '__main__':
    main()
