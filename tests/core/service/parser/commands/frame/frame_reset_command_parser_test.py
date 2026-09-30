# -*- coding: UTF-8 -*-

'''
Module
    frame_reset_command_parser_test.py
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
    Unit tests for FrameResetCommandParser implementation.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.model.dsl.ast.command_type import ScaraCommandType
from scaralang.core.model.dsl.token.scara_token import ScaraToken
from scaralang.core.model.dsl.token.scara_token_type import ScaraTokenType
from scaralang.core.service.parser.commands.frame.frame_reset_command_parser import FrameResetCommandParser
from scaralang.core.service.parser.commands.icommand_parser import ICommandParser

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestFrameResetCommandParser(TestCase):
    '''
        Test cases verifying FrameResetCommandParser behavior.

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
        parser = FrameResetCommandParser()
        self.assertEqual(parser.name, 'frame_reset_command_parser')
        self.assertIsInstance(parser, ICommandParser)

    def test_can_parse(self) -> None:
        '''
            Verifies can_parse method matches FRAME_RESET.
        '''
        parser = FrameResetCommandParser()
        self.assertTrue(parser.can_parse(command_name='FRAME_RESET'))
        self.assertFalse(parser.can_parse(command_name='FRAME_SET'))

    def test_parse_success(self) -> None:
        '''
            Verifies parsing of FRAME_RESET instruction.
        '''
        parser = FrameResetCommandParser()
        tokens = (
            ScaraToken(token_type=ScaraTokenType.IDENTIFIER, value='FRAME_RESET', line=1, column=1),
        )
        instruction = parser.parse(tokens=tokens, line_num=1, raw_text='FRAME_RESET')
        self.assertEqual(instruction.command_type, ScaraCommandType.FRAME_RESET)
        self.assertEqual(instruction.line_number, 1)
        self.assertEqual(instruction.parameters, {})


if __name__ == '__main__':
    main()
