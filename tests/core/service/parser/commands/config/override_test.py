# -*- coding: UTF-8 -*-

'''
Module
    override_test.py
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
    Unit tests for OverrideParser implementation.
'''

from __future__ import annotations

from unittest import TestCase, main

from scaralang.core.model.dsl.ast.command_type import ScaraCommandType
from scaralang.core.model.dsl.ast.instruction_param import ScaraInstructionParam
from scaralang.core.model.dsl.token.token import ScaraToken
from scaralang.core.model.dsl.token.token_type import ScaraTokenType
from scaralang.core.model.exceptions.syntax import ScaraSyntaxError
from scaralang.core.service.parser.commands.config.override import OverrideParser
from scaralang.core.service.parser.commands.iparser import ICommandParser

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestOverrideParser(TestCase):
    '''
        Test cases verifying OverrideParser behavior.

        It defines:

            :methods:
                | test_properties_and_protocol - Verifies name and protocol conformance.
                | test_can_parse - Verifies command matching.
                | test_parse_success - Verifies statement parsing into instruction.
                | test_parse_missing_arg - Verifies ScaraSyntaxError on missing percentage.
                | test_parse_invalid_percent - Verifies ScaraSyntaxError on non-numeric percentage.
    '''

    def test_properties_and_protocol(self) -> None:
        '''
            Verifies name property and structural protocol conformance.
        '''
        parser = OverrideParser()
        self.assertEqual(parser.name, 'override_parser')
        self.assertIsInstance(parser, ICommandParser)

    def test_can_parse(self) -> None:
        '''
            Verifies can_parse method matches OVERRIDE.
        '''
        parser = OverrideParser()
        self.assertTrue(parser.can_parse(command_name='OVERRIDE'))
        self.assertFalse(parser.can_parse(command_name='SPEED'))

    def test_parse_success(self) -> None:
        '''
            Verifies parsing of OVERRIDE instruction.
        '''
        parser = OverrideParser()
        tokens = (
            ScaraToken(
                token_type=ScaraTokenType.IDENTIFIER,
                value='OVERRIDE',
                line=1,
                column=1,
            ),
            ScaraToken(
                token_type=ScaraTokenType.NUMBER,
                value='80',
                line=1,
                column=10,
            ),
        )
        instruction = parser.parse(tokens=tokens, line_num=1, raw_text='OVERRIDE 80')
        self.assertEqual(instruction.command_type, ScaraCommandType.OVERRIDE)
        self.assertEqual(instruction.parameters.get(ScaraInstructionParam.PERCENT), 80.0)

    def test_parse_missing_arg(self) -> None:
        '''
            Verifies ScaraSyntaxError on missing override argument.
        '''
        parser = OverrideParser()
        tokens = (
            ScaraToken(
                token_type=ScaraTokenType.IDENTIFIER,
                value='OVERRIDE',
                line=1,
                column=1,
            ),
        )
        with self.assertRaises(ScaraSyntaxError):
            parser.parse(tokens=tokens, line_num=1, raw_text='OVERRIDE')

    def test_parse_invalid_percent(self) -> None:
        '''
            Verifies ScaraSyntaxError on non-numeric override percentage.
        '''
        parser = OverrideParser()
        tokens = (
            ScaraToken(
                token_type=ScaraTokenType.IDENTIFIER,
                value='OVERRIDE',
                line=1,
                column=1,
            ),
            ScaraToken(
                token_type=ScaraTokenType.IDENTIFIER,
                value='BAD_PERCENT',
                line=1,
                column=10,
            ),
        )
        with self.assertRaises(ScaraSyntaxError):
            parser.parse(tokens=tokens, line_num=1, raw_text='OVERRIDE BAD_PERCENT')


if __name__ == '__main__':
    main()
