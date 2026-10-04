# -*- coding: UTF-8 -*-

'''
Module
    retract_command_parser_test.py
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
    Unit tests for RetractCommandParser implementation.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.model.dsl.ast.command_type import ScaraCommandType
from scaralang.core.model.dsl.token.scara_token import ScaraToken
from scaralang.core.model.dsl.token.scara_token_type import ScaraTokenType
from scaralang.core.service.parser.commands.icommand_parser import ICommandParser
from scaralang.core.service.parser.commands.motion.retract_command_parser import RetractCommandParser

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestRetractCommandParser(TestCase):
    '''
        Test cases verifying RetractCommandParser behavior.

        It defines:

            :methods:
                | test_properties_and_protocol - Verifies name and protocol conformance.
                | test_can_parse - Verifies command matching.
                | test_parse_success - Verifies statement parsing into instruction.
    '''

    def test_properties_and_protocol(self) -> None:
        '''
            Verifies name property and structural protocol conformance.
        '''
        parser = RetractCommandParser()
        self.assertEqual(parser.name, 'retract_command_parser')
        self.assertIsInstance(parser, ICommandParser)

    def test_can_parse(self) -> None:
        '''
            Verifies can_parse method matches RETRACT.
        '''
        parser = RetractCommandParser()
        self.assertTrue(parser.can_parse(command_name='RETRACT'))
        self.assertFalse(parser.can_parse(command_name='APPROACH'))

    def test_parse_success(self) -> None:
        '''
            Verifies parsing of RETRACT instruction.
        '''
        parser = RetractCommandParser()
        tokens = (
            ScaraToken(token_type=ScaraTokenType.IDENTIFIER, value='RETRACT', line=1, column=1),
            ScaraToken(token_type=ScaraTokenType.IDENTIFIER, value='DZ', line=1, column=9),
            ScaraToken(token_type=ScaraTokenType.EQUALS, value='=', line=1, column=11),
            ScaraToken(token_type=ScaraTokenType.NUMBER, value='20', line=1, column=12),
        )
        instruction = parser.parse(tokens=tokens, line_num=1, raw_text='RETRACT DZ=20')
        self.assertEqual(instruction.command_type, ScaraCommandType.RETRACT)
        self.assertEqual(instruction.line_number, 1)
        self.assertEqual(instruction.parameters.get('DZ'), 20)


if __name__ == '__main__':
    main()
