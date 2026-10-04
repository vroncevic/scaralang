# -*- coding: UTF-8 -*-

'''
Module
    instruction_line_parser_factory_test.py
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
    Unit tests for InstructionLineParserFactory.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.service.parser.commands.motion.linear_move_command_parser import LinearMoveCommandParser
from scaralang.core.service.parser.instruction.iinstruction_line_parser import IInstructionLineParser
from scaralang.core.service.parser.instruction.instruction_line_parser_factory import InstructionLineParserFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestInstructionLineParserFactory(TestCase):
    '''
        Test cases verifying InstructionLineParserFactory instance creation.

        It defines:

            :methods:
                | test_create - Verifies factory returns default configured line parser.
                | test_create_with_handlers - Verifies factory returns custom configured line parser.
                | test_get_version - Verifies factory version string.
    '''

    def test_create(self) -> None:
        '''
            Verifies that factory returns default configured line parser.
        '''
        parser = InstructionLineParserFactory.create()
        self.assertIsInstance(parser, IInstructionLineParser)
        self.assertEqual(len(parser.handlers), 30)

    def test_create_with_handlers(self) -> None:
        '''
            Verifies that factory returns custom configured line parser.
        '''
        handler = LinearMoveCommandParser()
        parser = InstructionLineParserFactory.create_with_handlers(
            handlers=(handler,)
        )
        self.assertIsInstance(parser, IInstructionLineParser)
        self.assertEqual(parser.handlers, (handler,))

    def test_default_domains(self) -> None:
        '''
            Verifies that default_domains returns the 6 registered domain providers.
        '''
        domains = InstructionLineParserFactory.default_domains()
        self.assertEqual(len(domains), 6)

    def test_get_version(self) -> None:
        '''
            Verifies that get_version returns a valid version string.
        '''
        version = InstructionLineParserFactory.get_version()
        self.assertIsInstance(version, str)
        self.assertTrue(len(version) > 0)


if __name__ == '__main__':
    main()
