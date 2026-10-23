# -*- coding: UTF-8 -*-

'''
Module
    iparser_test.py
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
    Unit tests for IScaraParser structural protocol compliance.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.service.parser.iparser import IScaraParser
from scaralang.core.service.parser.lexer.factory import LexerFactory
from scaralang.core.service.parser.parser import ScaraParser
from scaralang.core.service.parser.splitter.factory import SplitterFactory
from scaralang.infrastructure.parser.instruction.factory import DefaultInstructionParserFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestIScaraParser(TestCase):
    '''
        Test cases verifying IScaraParser structural subtyping.

        It defines:

            :methods:
                | test_structural_compliance - Verifies ScaraParser satisfies protocol.
                | test_name_property - Verifies name property returns expected identifier.
    '''

    def test_structural_compliance(self) -> None:
        '''
            Verifies that ScaraParser satisfies IScaraParser.
        '''
        parser = ScaraParser(
            lexer=LexerFactory.create().lexer,
            line_splitter=SplitterFactory.create().splitter,
            line_parser=DefaultInstructionParserFactory.create().parser,
        )
        self.assertIsInstance(parser, IScaraParser)

    def test_name_property(self) -> None:
        '''
            Verifies that name property returns expected identifier.
        '''
        parser = ScaraParser(
            lexer=LexerFactory.create().lexer,
            line_splitter=SplitterFactory.create().splitter,
            line_parser=DefaultInstructionParserFactory.create().parser,
        )
        self.assertEqual(parser.name, 'scara_parser')


if __name__ == '__main__':
    main()
