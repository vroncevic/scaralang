# -*- coding: UTF-8 -*-

'''
Module
    zone_command_parser_test.py
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
    Unit tests for ZoneCommandParser implementation.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.model.dsl.ast.command_type import ScaraCommandType
from scaralang.core.model.dsl.ast.zone_mode import ZoneMode
from scaralang.core.model.dsl.token.scara_token import ScaraToken
from scaralang.core.model.dsl.token.scara_token_type import ScaraTokenType
from scaralang.core.service.parser.commands.config.zone_command_parser import ZoneCommandParser
from scaralang.core.service.parser.commands.icommand_parser import ICommandParser

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestZoneCommandParser(TestCase):
    '''
        Test cases verifying ZoneCommandParser behavior.

        It defines:

            :methods:
                | test_properties_and_protocol - Verifies name and protocol conformance.
                | test_can_parse - Verifies command matching.
                | test_parse_fine_success - Verifies ZONE FINE statement parsing.
                | test_parse_blend_success - Verifies ZONE BLEND statement parsing.
                | test_parse_missing_mode - Verifies ValueError on missing zone mode.
    '''

    def test_properties_and_protocol(self) -> None:
        '''
            Verifies name property and structural protocol conformance.
        '''
        parser = ZoneCommandParser()
        self.assertEqual(parser.name, 'zone_command_parser')
        self.assertIsInstance(parser, ICommandParser)

    def test_can_parse(self) -> None:
        '''
            Verifies can_parse method matches ZONE.
        '''
        parser = ZoneCommandParser()
        self.assertTrue(parser.can_parse(command_name='ZONE'))
        self.assertFalse(parser.can_parse(command_name='SPEED'))

    def test_parse_fine_success(self) -> None:
        '''
            Verifies parsing of ZONE FINE instruction.
        '''
        parser = ZoneCommandParser()
        tokens = (
            ScaraToken(token_type=ScaraTokenType.IDENTIFIER, value='ZONE', line=1, column=1),
            ScaraToken(token_type=ScaraTokenType.IDENTIFIER, value='FINE', line=1, column=6),
        )
        instruction = parser.parse(tokens=tokens, line_num=1, raw_text='ZONE FINE')
        self.assertEqual(instruction.command_type, ScaraCommandType.ZONE)
        self.assertEqual(instruction.parameters.get('mode'), ZoneMode.FINE)

    def test_parse_blend_success(self) -> None:
        '''
            Verifies parsing of ZONE BLEND instruction.
        '''
        parser = ZoneCommandParser()
        tokens = (
            ScaraToken(token_type=ScaraTokenType.IDENTIFIER, value='ZONE', line=1, column=1),
            ScaraToken(token_type=ScaraTokenType.IDENTIFIER, value='BLEND', line=1, column=6),
            ScaraToken(token_type=ScaraTokenType.IDENTIFIER, value='R', line=1, column=12),
            ScaraToken(token_type=ScaraTokenType.EQUALS, value='=', line=1, column=13),
            ScaraToken(token_type=ScaraTokenType.NUMBER, value='10', line=1, column=14),
        )
        instruction = parser.parse(tokens=tokens, line_num=1, raw_text='ZONE BLEND R=10')
        self.assertEqual(instruction.command_type, ScaraCommandType.ZONE)
        self.assertEqual(instruction.parameters.get('mode'), ZoneMode.BLEND)
        self.assertEqual(instruction.parameters.get('radius'), 10.0)

    def test_parse_missing_mode(self) -> None:
        '''
            Verifies ValueError on missing zone mode.
        '''
        parser = ZoneCommandParser()
        tokens = (
            ScaraToken(token_type=ScaraTokenType.IDENTIFIER, value='ZONE', line=1, column=1),
        )
        with self.assertRaises(ValueError):
            parser.parse(tokens=tokens, line_num=1, raw_text='ZONE')


if __name__ == '__main__':
    main()
