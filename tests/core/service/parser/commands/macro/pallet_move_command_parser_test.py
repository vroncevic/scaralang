# -*- coding: UTF-8 -*-

'''
Module
    pallet_move_command_parser_test.py
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
    Unit tests for PalletMoveCommandParser implementation.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.model.dsl.ast.command_type import ScaraCommandType
from scaralang.core.model.dsl.ast.instruction_param import InstructionParam
from scaralang.core.model.dsl.token.scara_token import ScaraToken
from scaralang.core.model.dsl.token.scara_token_type import ScaraTokenType
from scaralang.core.model.exceptions.scara_syntax_error import ScaraSyntaxError
from scaralang.core.service.parser.commands.icommand_parser import ICommandParser
from scaralang.core.service.parser.commands.macro.pallet_move_command_parser import PalletMoveCommandParser

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestPalletMoveCommandParser(TestCase):
    '''
        Test cases verifying PalletMoveCommandParser behavior.

        It defines:

            :methods:
                | test_properties_and_protocol - Verifies name and protocol conformance.
                | test_can_parse - Verifies command matching.
                | test_parse_success - Verifies statement parsing into instruction.
                | test_parse_missing_name - Verifies ValueError on missing pallet name.
    '''

    def test_properties_and_protocol(self) -> None:
        '''
            Verifies name property and structural protocol conformance.
        '''
        parser = PalletMoveCommandParser()
        self.assertEqual(parser.name, 'pallet_move_command_parser')
        self.assertIsInstance(parser, ICommandParser)

    def test_can_parse(self) -> None:
        '''
            Verifies can_parse method matches MOVE_PALLET.
        '''
        parser = PalletMoveCommandParser()
        self.assertTrue(parser.can_parse(command_name='MOVE_PALLET'))
        self.assertFalse(parser.can_parse(command_name='PALLET_DEF'))

    def test_parse_success(self) -> None:
        '''
            Verifies parsing of MOVE_PALLET instruction.
        '''
        parser = PalletMoveCommandParser()
        tokens = (
            ScaraToken(token_type=ScaraTokenType.IDENTIFIER, value='MOVE_PALLET', line=1, column=1),
            ScaraToken(token_type=ScaraTokenType.IDENTIFIER, value='PALLET1', line=1, column=13),
            ScaraToken(token_type=ScaraTokenType.IDENTIFIER, value='INDEX', line=1, column=21),
            ScaraToken(token_type=ScaraTokenType.EQUALS, value='=', line=1, column=26),
            ScaraToken(token_type=ScaraTokenType.NUMBER, value='2', line=1, column=27),
        )
        instruction = parser.parse(tokens=tokens, line_num=1, raw_text='MOVE_PALLET PALLET1 INDEX=2')
        self.assertEqual(instruction.command_type, ScaraCommandType.MOVE_PALLET)
        self.assertEqual(instruction.parameters.get(InstructionParam.NAME), 'PALLET1')
        self.assertEqual(instruction.parameters.get(InstructionParam.INDEX), 2)

    def test_parse_missing_name(self) -> None:
        '''
            Verifies ScaraSyntaxError when pallet name is missing.
        '''
        parser = PalletMoveCommandParser()
        tokens = (
            ScaraToken(token_type=ScaraTokenType.IDENTIFIER, value='MOVE_PALLET', line=1, column=1),
        )
        with self.assertRaises(ScaraSyntaxError):
            parser.parse(tokens=tokens, line_num=1, raw_text='MOVE_PALLET')


if __name__ == '__main__':
    main()
