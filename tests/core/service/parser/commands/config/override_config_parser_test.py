# -*- coding: UTF-8 -*-

'''
Module
    override_config_parser_test.py
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
    Unit tests for OverrideConfigParser implementation.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.model.dsl.ast.command_type import ScaraCommandType
from scaralang.core.model.dsl.ast.instruction_param import InstructionParam
from scaralang.core.model.dsl.token.scara_token import ScaraToken
from scaralang.core.model.dsl.token.scara_token_type import ScaraTokenType
from scaralang.core.service.parser.commands.config.override_config_parser import OverrideConfigParser
from scaralang.core.service.parser.commands.icommand_parser import ICommandParser

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestOverrideConfigParser(TestCase):
    '''
        Test cases verifying OverrideConfigParser behavior.

        It defines:

            :methods:
                | test_properties_and_protocol - Verifies name and protocol conformance.
                | test_can_parse - Verifies command matching.
                | test_parse_success - Verifies statement parsing into instruction.
                | test_parse_missing_arg - Verifies ValueError on missing percentage.
    '''

    def test_properties_and_protocol(self) -> None:
        '''
            Verifies name property and structural protocol conformance.
        '''
        parser = OverrideConfigParser()
        self.assertEqual(parser.name, 'override_config_parser')
        self.assertIsInstance(parser, ICommandParser)

    def test_can_parse(self) -> None:
        '''
            Verifies can_parse method matches OVERRIDE.
        '''
        parser = OverrideConfigParser()
        self.assertTrue(parser.can_parse(command_name='OVERRIDE'))
        self.assertFalse(parser.can_parse(command_name='SPEED'))

    def test_parse_success(self) -> None:
        '''
            Verifies parsing of OVERRIDE instruction.
        '''
        parser = OverrideConfigParser()
        tokens = (
            ScaraToken(token_type=ScaraTokenType.IDENTIFIER, value='OVERRIDE', line=1, column=1),
            ScaraToken(token_type=ScaraTokenType.NUMBER, value='80', line=1, column=10),
        )
        instruction = parser.parse(tokens=tokens, line_num=1, raw_text='OVERRIDE 80')
        self.assertEqual(instruction.command_type, ScaraCommandType.OVERRIDE)
        self.assertEqual(instruction.parameters.get(InstructionParam.PERCENT), 80.0)

    def test_parse_missing_arg(self) -> None:
        '''
            Verifies ValueError on missing override argument.
        '''
        parser = OverrideConfigParser()
        tokens = (
            ScaraToken(token_type=ScaraTokenType.IDENTIFIER, value='OVERRIDE', line=1, column=1),
        )
        with self.assertRaises(ValueError):
            parser.parse(tokens=tokens, line_num=1, raw_text='OVERRIDE')


if __name__ == '__main__':
    main()
