# -*- coding: UTF-8 -*-

'''
Module
    dependencies_test.py
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
    Unit tests for ParserDependencies parameter bundle dataclass.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.service.parser.dependencies import ParserDependencies
from scaralang.core.service.parser.instruction.iparser import IInstructionLineParser
from scaralang.core.service.parser.lexer.factory import LexerFactory
from scaralang.core.service.parser.lexer.ilexer import IScaraLexer
from scaralang.core.service.parser.splitter.factory import SplitterFactory
from scaralang.core.service.parser.splitter.isplitter import ITokenLineSplitter
from scaralang.infrastructure.parser.instruction.factory import DefaultInstructionParserFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestParserDependencies(TestCase):
    '''
        Test cases verifying ParserDependencies parameter encapsulation.

        It defines:

            :methods:
                | test_dependencies_encapsulation - Verifies storage and typing of dependencies.
    '''

    def test_dependencies_encapsulation(self) -> None:
        '''
            Verifies that ParserDependencies stores collaborators properly.
        '''
        lexer = LexerFactory.create().lexer
        line_splitter = SplitterFactory.create().splitter
        line_parser = DefaultInstructionParserFactory.create().parser
        deps = ParserDependencies(
            lexer=lexer,
            line_splitter=line_splitter,
            line_parser=line_parser,
        )
        self.assertIs(deps.lexer, lexer)
        self.assertIsInstance(deps.lexer, IScaraLexer)
        self.assertIs(deps.line_splitter, line_splitter)
        self.assertIsInstance(deps.line_splitter, ITokenLineSplitter)
        self.assertIs(deps.line_parser, line_parser)
        self.assertIsInstance(deps.line_parser, IInstructionLineParser)


if __name__ == '__main__':
    main()
