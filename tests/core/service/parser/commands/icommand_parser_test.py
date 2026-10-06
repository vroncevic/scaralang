# -*- coding: UTF-8 -*-

'''
Module
    icommand_parser_test.py
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
    Unit tests for ICommandParser structural protocol interface.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.model.dsl.ast.command_type import ScaraCommandType
from scaralang.core.model.dsl.ast.instruction import ScaraInstruction
from scaralang.core.model.dsl.token.scara_token import ScaraToken
from scaralang.core.service.parser.commands.icommand_parser import ICommandParser

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.6'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class MockCommandParser:
    '''
        Mock command parser implementation verifying protocol conformance.

        It defines:

            :attributes:
                | _name - Component identification name.
            :methods:
                | name - Property returning component name.
                | can_parse - Checks whether command can be parsed.
                | parse - Parses tokens into ScaraInstruction.
    '''

    def __init__(self) -> None:
        '''Initializes MockCommandParser.'''
        self._name: str = 'mock_command_parser'

    @property
    def name(self) -> str:
        '''
            Gets component identification name.

            :return: Component name string.
        '''
        return self._name

    def can_parse(self, *, command_name: str) -> bool:
        '''
            Checks if command is supported.

            :param command_name: Command keyword.
            :return: True if supported.
        '''
        return command_name == 'TEST'

    def parse(
        self,
        *,
        tokens: tuple[ScaraToken, ...],
        line_num: int,
        raw_text: str,
    ) -> ScaraInstruction:
        '''
            Parses mock command statement.

            :param tokens: Tokens tuple.
            :param line_num: Line number.
            :param raw_text: Raw statement.
            :return: ScaraInstruction node.
        '''
        _ = tokens
        return ScaraInstruction(
            command_type=ScaraCommandType.HOME,
            line_number=line_num,
            raw_text=raw_text,
            parameters={},
        )


class TestICommandParser(TestCase):
    '''
        Test cases verifying ICommandParser structural subtyping.

        It defines:

            :methods:
                | test_protocol_conformance - Verifies Mock satisfies ICommandParser.
    '''

    def test_protocol_conformance(self) -> None:
        '''
            Verifies that MockCommandParser conforms to ICommandParser via isinstance.
        '''
        parser = MockCommandParser()
        self.assertIsInstance(parser, ICommandParser)
        self.assertEqual(parser.name, 'mock_command_parser')
        self.assertTrue(parser.can_parse(command_name='TEST'))
        self.assertFalse(parser.can_parse(command_name='OTHER'))


if __name__ == '__main__':
    main()
