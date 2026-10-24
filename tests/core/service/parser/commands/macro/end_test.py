# -*- coding: UTF-8 -*-

'''
Module
    end_test.py
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
    Unit tests for EndParser implementation.
'''

from __future__ import annotations

from unittest import TestCase, main

from scaralang.core.model.dsl.ast.command_type import ScaraCommandType
from scaralang.core.model.dsl.token.token import ScaraToken
from scaralang.core.model.dsl.token.token_type import ScaraTokenType
from scaralang.core.model.exceptions.syntax import ScaraSyntaxError
from scaralang.core.service.parser.commands.iparser import ICommandParser
from scaralang.core.service.parser.commands.macro.end import EndParser

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestEndParser(TestCase):
    '''
        Test cases verifying EndParser behavior.

        It defines:

            :methods:
                | test_properties_and_protocol - Verifies name and protocol conformance.
                | test_can_parse - Verifies command matching.
                | test_parse_success - Verifies statement parsing into instruction.
                | test_parse_excess_tokens - Verifies ScaraSyntaxError on excess arguments.
    '''

    def test_properties_and_protocol(self) -> None:
        '''
            Verifies name property and structural protocol conformance.

            :exceptions: None.
        '''
        parser = EndParser()
        self.assertIsInstance(parser, ICommandParser)
        self.assertEqual(parser.name, 'end_parser')

    def test_can_parse(self) -> None:
        '''
            Verifies command matching logic.

            :exceptions: None.
        '''
        parser = EndParser()
        self.assertTrue(parser.can_parse(command_name='END'))
        self.assertFalse(parser.can_parse(command_name='DEF'))
        self.assertFalse(parser.can_parse(command_name='REPEAT'))

    def test_parse_success(self) -> None:
        '''
            Verifies successful parsing of END statement.

            :exceptions: None.
        '''
        parser = EndParser()
        tokens = (
            ScaraToken(
                token_type=ScaraTokenType.KEYWORD,
                value='END',
                line=5,
                column=1,
            ),
        )
        instruction = parser.parse(
            tokens=tokens,
            line_num=5,
            raw_text='END',
        )
        self.assertEqual(instruction.command_type, ScaraCommandType.END)
        self.assertEqual(instruction.line_number, 5)
        self.assertEqual(instruction.parameters, {})

    def test_parse_excess_tokens(self) -> None:
        '''
            Verifies ScaraSyntaxError on excess tokens after END.

            :exceptions: None.
        '''
        parser = EndParser()
        tokens = (
            ScaraToken(
                token_type=ScaraTokenType.KEYWORD,
                value='END',
                line=5,
                column=1,
            ),
            ScaraToken(
                token_type=ScaraTokenType.IDENTIFIER,
                value='NOW',
                line=5,
                column=5,
            ),
        )
        with self.assertRaises(ScaraSyntaxError):
            parser.parse(tokens=tokens, line_num=5, raw_text='END NOW')


if __name__ == '__main__':
    main()
