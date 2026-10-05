# -*- coding: UTF-8 -*-

'''
Module
    frame_set_command_parser_test.py
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
    Unit tests for FrameSetCommandParser implementation.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.model.dsl.ast.command_type import ScaraCommandType
from scaralang.core.model.dsl.token.scara_token import ScaraToken
from scaralang.core.model.dsl.token.scara_token_type import ScaraTokenType
from scaralang.core.service.parser.commands.frame.frame_set_command_parser import FrameSetCommandParser
from scaralang.core.service.parser.commands.icommand_parser import ICommandParser

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.5'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestFrameSetCommandParser(TestCase):
    '''
        Test cases verifying FrameSetCommandParser behavior.

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
        parser = FrameSetCommandParser()
        self.assertEqual(parser.name, 'frame_set_command_parser')
        self.assertIsInstance(parser, ICommandParser)

    def test_can_parse(self) -> None:
        '''
            Verifies can_parse method matches FRAME_SET.
        '''
        parser = FrameSetCommandParser()
        self.assertTrue(parser.can_parse(command_name='FRAME_SET'))
        self.assertFalse(parser.can_parse(command_name='FRAME_RESET'))

    def test_parse_success(self) -> None:
        '''
            Verifies parsing of FRAME_SET instruction.
        '''
        parser = FrameSetCommandParser()
        tokens = (
            ScaraToken(token_type=ScaraTokenType.IDENTIFIER, value='FRAME_SET', line=1, column=1),
            ScaraToken(token_type=ScaraTokenType.IDENTIFIER, value='X', line=1, column=11),
            ScaraToken(token_type=ScaraTokenType.EQUALS, value='=', line=1, column=12),
            ScaraToken(token_type=ScaraTokenType.NUMBER, value='50', line=1, column=13),
            ScaraToken(token_type=ScaraTokenType.IDENTIFIER, value='Y', line=1, column=16),
            ScaraToken(token_type=ScaraTokenType.EQUALS, value='=', line=1, column=17),
            ScaraToken(token_type=ScaraTokenType.NUMBER, value='50', line=1, column=18),
        )
        instruction = parser.parse(tokens=tokens, line_num=1, raw_text='FRAME_SET X=50 Y=50')
        self.assertEqual(instruction.command_type, ScaraCommandType.FRAME_SET)
        self.assertEqual(instruction.line_number, 1)
        self.assertEqual(instruction.parameters.get('X'), 50)
        self.assertEqual(instruction.parameters.get('Y'), 50)


if __name__ == '__main__':
    main()
