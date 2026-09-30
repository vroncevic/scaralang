# -*- coding: UTF-8 -*-

'''
Module
    command_token_parser_test.py
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
    Unit tests for CommandTokenParser.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.service.compiler.binary.command.tokens.command_token_parser import CommandTokenParser
from scaralang.core.service.compiler.binary.command.tokens.icommand_token_parser import ICommandTokenParser

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestCommandTokenParser(TestCase):
    '''
        Test cases verifying CommandTokenParser parsing and protocol conformance.

        It defines:

            :methods:
                | setUp - Initializes CommandTokenParser instance.
                | test_structural_conformance - Verifies protocol adherence.
                | test_name_property - Verifies name property value.
                | test_parse_simple_command - Verifies command without arguments.
                | test_parse_hash_argument - Verifies command with hash-separated argument.
                | test_parse_empty_command - Verifies empty string command handling.
    '''

    def setUp(self) -> None:
        '''
            Prepares CommandTokenParser instance for testing.
        '''
        self.parser = CommandTokenParser()

    def test_structural_conformance(self) -> None:
        '''
            Verifies structural conformance to ICommandTokenParser.
        '''
        self.assertIsInstance(self.parser, ICommandTokenParser)

    def test_name_property(self) -> None:
        '''
            Verifies component name property.
        '''
        self.assertEqual(self.parser.name, 'command_token_parser')

    def test_parse_simple_command(self) -> None:
        '''
            Verifies parsing simple command token.
        '''
        token = self.parser.parse(command='<CMD:HOME>')
        self.assertEqual(token.cmd_name, 'HOME')
        self.assertEqual(token.arg, '')
        self.assertEqual(token.clean, '<CMD:HOME>')
        self.assertEqual(token.parts, ('HOME',))

    def test_parse_hash_argument(self) -> None:
        '''
            Verifies parsing command token with hash argument.
        '''
        token = self.parser.parse(command='<CMD:WAIT#250>')
        self.assertEqual(token.cmd_name, 'WAIT')
        self.assertEqual(token.arg, '250')
        self.assertEqual(token.clean, '<CMD:WAIT#250>')
        self.assertEqual(token.parts, ('WAIT', '250'))

    def test_parse_empty_command(self) -> None:
        '''
            Verifies parsing empty command string.
        '''
        token = self.parser.parse(command='')
        self.assertEqual(token.cmd_name, '')
        self.assertEqual(token.arg, '')
        self.assertEqual(token.parts, ())


if __name__ == '__main__':
    main()
