# -*- coding: UTF-8 -*-

'''
Module
    elbow_config_parser_test.py
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
    Unit tests for ElbowConfigParser implementation.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.model.dsl.ast.command_type import ScaraCommandType
from scaralang.core.model.dsl.token.scara_token import ScaraToken
from scaralang.core.model.dsl.token.scara_token_type import ScaraTokenType
from scaralang.core.model.kinematics.elbow_config import ElbowConfig
from scaralang.core.service.parser.commands.config.elbow_config_parser import ElbowConfigParser
from scaralang.core.service.parser.commands.icommand_parser import ICommandParser

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestElbowConfigParser(TestCase):
    '''
        Test cases verifying ElbowConfigParser behavior.

        It defines:

            :methods:
                | test_properties_and_protocol - Verifies name and protocol conformance.
                | test_can_parse - Verifies command matching.
                | test_parse_success - Verifies statement parsing into instruction.
                | test_parse_syntax_error - Verifies ValueError on insufficient tokens.
                | test_parse_unknown_property - Verifies ValueError on non-ELBOW property.
                | test_parse_invalid_value - Verifies ValueError on invalid elbow value.
    '''

    def test_properties_and_protocol(self) -> None:
        '''
            Verifies name property and structural protocol conformance.
        '''
        parser = ElbowConfigParser()
        self.assertEqual(parser.name, 'elbow_config_parser')
        self.assertIsInstance(parser, ICommandParser)

    def test_can_parse(self) -> None:
        '''
            Verifies can_parse method matches CONFIG and CONFIG_ELBOW.
        '''
        parser = ElbowConfigParser()
        self.assertTrue(parser.can_parse(command_name='CONFIG'))
        self.assertTrue(parser.can_parse(command_name='CONFIG_ELBOW'))
        self.assertFalse(parser.can_parse(command_name='SPEED'))

    def test_parse_success(self) -> None:
        '''
            Verifies parsing of CONFIG ELBOW instruction.
        '''
        parser = ElbowConfigParser()
        tokens = (
            ScaraToken(token_type=ScaraTokenType.IDENTIFIER, value='CONFIG', line=1, column=1),
            ScaraToken(token_type=ScaraTokenType.IDENTIFIER, value='ELBOW', line=1, column=8),
            ScaraToken(token_type=ScaraTokenType.IDENTIFIER, value='LEFT', line=1, column=14),
        )
        instruction = parser.parse(tokens=tokens, line_num=1, raw_text='CONFIG ELBOW LEFT')
        self.assertEqual(instruction.command_type, ScaraCommandType.CONFIG_ELBOW)
        self.assertEqual(instruction.parameters.get('elbow'), ElbowConfig.LEFT)

    def test_parse_syntax_error(self) -> None:
        '''
            Verifies ValueError on short tokens.
        '''
        parser = ElbowConfigParser()
        tokens = (
            ScaraToken(token_type=ScaraTokenType.IDENTIFIER, value='CONFIG', line=1, column=1),
        )
        with self.assertRaises(ValueError):
            parser.parse(tokens=tokens, line_num=1, raw_text='CONFIG')

    def test_parse_unknown_property(self) -> None:
        '''
            Verifies ValueError on unknown CONFIG property.
        '''
        parser = ElbowConfigParser()
        tokens = (
            ScaraToken(token_type=ScaraTokenType.IDENTIFIER, value='CONFIG', line=1, column=1),
            ScaraToken(token_type=ScaraTokenType.IDENTIFIER, value='UNKNOWN', line=1, column=8),
            ScaraToken(token_type=ScaraTokenType.IDENTIFIER, value='LEFT', line=1, column=16),
        )
        with self.assertRaises(ValueError):
            parser.parse(tokens=tokens, line_num=1, raw_text='CONFIG UNKNOWN LEFT')

    def test_parse_invalid_value(self) -> None:
        '''
            Verifies ValueError on invalid elbow value.
        '''
        parser = ElbowConfigParser()
        tokens = (
            ScaraToken(token_type=ScaraTokenType.IDENTIFIER, value='CONFIG', line=1, column=1),
            ScaraToken(token_type=ScaraTokenType.IDENTIFIER, value='ELBOW', line=1, column=8),
            ScaraToken(token_type=ScaraTokenType.IDENTIFIER, value='CENTER', line=1, column=14),
        )
        with self.assertRaises(ValueError):
            parser.parse(tokens=tokens, line_num=1, raw_text='CONFIG ELBOW CENTER')


if __name__ == '__main__':
    main()
