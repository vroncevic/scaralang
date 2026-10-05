# -*- coding: UTF-8 -*-

'''
Module
    parameter_extractor_test.py
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
    Unit tests for ParameterExtractor implementation.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.model.dsl.token.scara_token import ScaraToken
from scaralang.core.model.dsl.token.scara_token_type import ScaraTokenType
from scaralang.core.service.parser.commands.parameter.parameter_extractor import ParameterExtractor

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.5'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestParameterExtractor(TestCase):
    '''
        Test cases verifying ParameterExtractor functionality.

        It defines:

            :methods:
                | test_extract_equals_key_values - Verifies extraction of key=value syntax.
                | test_extract_spaced_key_values - Verifies extraction of key value syntax.
                | test_extract_flag_parameter - Verifies extraction of standalone flag tokens.
                | test_parse_token_value_numeric - Verifies parsing int, float, scientific notation.
                | test_parse_token_value_string - Verifies string literal parsing.
    '''

    def test_extract_equals_key_values(self) -> None:
        '''
            Verifies extraction of key=value parameter assignments.
        '''
        tokens = (
            ScaraToken(
                token_type=ScaraTokenType.IDENTIFIER,
                value='X',
                line=1,
                column=1,
            ),
            ScaraToken(
                token_type=ScaraTokenType.EQUALS,
                value='=',
                line=1,
                column=2,
            ),
            ScaraToken(
                token_type=ScaraTokenType.NUMBER,
                value='100.5',
                line=1,
                column=3,
            ),
        )
        params = ParameterExtractor.extract_key_values(tokens=tokens)
        self.assertEqual(params, {'X': 100.5})

    def test_extract_spaced_key_values(self) -> None:
        '''
            Verifies extraction of key value parameter assignments without equals.
        '''
        tokens = (
            ScaraToken(
                token_type=ScaraTokenType.IDENTIFIER,
                value='Y',
                line=1,
                column=1,
            ),
            ScaraToken(
                token_type=ScaraTokenType.NUMBER,
                value='42',
                line=1,
                column=3,
            ),
        )
        params = ParameterExtractor.extract_key_values(tokens=tokens)
        self.assertEqual(params, {'Y': 42})

    def test_extract_flag_parameter(self) -> None:
        '''
            Verifies extraction of standalone flag parameters defaults to True.
        '''
        tokens = (
            ScaraToken(
                token_type=ScaraTokenType.IDENTIFIER,
                value='FORCE',
                line=1,
                column=1,
            ),
        )
        params = ParameterExtractor.extract_key_values(tokens=tokens)
        self.assertEqual(params, {'FORCE': True})

    def test_parse_token_value_numeric(self) -> None:
        '''
            Verifies parsing int, float, and scientific notation numbers.
        '''
        tok_int = ScaraToken(
            token_type=ScaraTokenType.NUMBER, value='10', line=1, column=1
        )
        tok_float = ScaraToken(
            token_type=ScaraTokenType.NUMBER, value='3.14', line=1, column=1
        )
        tok_sci = ScaraToken(
            token_type=ScaraTokenType.NUMBER, value='1e-3', line=1, column=1
        )
        self.assertEqual(
            ParameterExtractor.parse_token_value(token=tok_int), 10
        )
        self.assertEqual(
            ParameterExtractor.parse_token_value(token=tok_float), 3.14
        )
        self.assertEqual(
            ParameterExtractor.parse_token_value(token=tok_sci), 0.001
        )

    def test_parse_token_value_string(self) -> None:
        '''
            Verifies parsing string token values.
        '''
        tok_str = ScaraToken(
            token_type=ScaraTokenType.STRING, value='test_str', line=1, column=1
        )
        self.assertEqual(
            ParameterExtractor.parse_token_value(token=tok_str), 'test_str'
        )


if __name__ == '__main__':
    main()
