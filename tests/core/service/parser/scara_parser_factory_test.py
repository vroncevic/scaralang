# -*- coding: UTF-8 -*-

'''
Module
    scara_parser_factory_test.py
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
    Unit tests for ScaraParserFactory.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.service.parser.commands.motion.linear_move_command_parser import LinearMoveCommandParser
from scaralang.core.service.parser.instruction.instruction_line_parser_factory import InstructionLineParserFactory
from scaralang.core.service.parser.iscara_parser import IScaraParser
from scaralang.core.service.parser.lexer.scara_lexer_factory import ScaraLexerFactory
from scaralang.core.service.parser.scara_parser_factory import ScaraParserFactory
from scaralang.core.service.parser.splitter.token_line_splitter_factory import TokenLineSplitterFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.5'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestScaraParserFactory(TestCase):
    '''
        Test cases verifying ScaraParserFactory instance creation.

        It defines:

            :methods:
                | test_create - Verifies factory returns IScaraParser instance.
                | test_create_with_handlers - Verifies factory returns custom configured parser.
                | test_create_with_collaborators - Verifies factory with explicit collaborators.
                | test_get_version - Verifies factory version string.
    '''

    def test_create(self) -> None:
        '''
            Verifies that factory returns an IScaraParser instance.
        '''
        lexer = ScaraLexerFactory.create()
        parser = ScaraParserFactory.create(lexer=lexer)
        self.assertIsInstance(parser, IScaraParser)

    def test_create_with_handlers(self) -> None:
        '''
            Verifies that factory returns parser with custom handlers.
        '''
        lexer = ScaraLexerFactory.create()
        handler = LinearMoveCommandParser()
        parser = ScaraParserFactory.create_with_handlers(
            lexer=lexer, handlers=(handler,)
        )
        self.assertIsInstance(parser, IScaraParser)

    def test_create_with_collaborators(self) -> None:
        '''
            Verifies that factory returns parser with explicit collaborators.
        '''
        lexer = ScaraLexerFactory.create()
        splitter = TokenLineSplitterFactory.create()
        line_parser = InstructionLineParserFactory.create()
        parser = ScaraParserFactory.create_with_collaborators(
            lexer=lexer,
            line_splitter=splitter,
            line_parser=line_parser,
        )
        self.assertIsInstance(parser, IScaraParser)

    def test_get_version(self) -> None:
        '''
            Verifies that get_version returns a valid version string.
        '''
        version = ScaraParserFactory.get_version()
        self.assertIsInstance(version, str)
        self.assertTrue(len(version) > 0)


if __name__ == '__main__':
    main()
