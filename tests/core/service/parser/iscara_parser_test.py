# -*- coding: UTF-8 -*-

'''
Module
    iscara_parser_test.py
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
    Unit tests for IScaraParser protocol compliance.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.service.parser.instruction.instruction_line_parser_factory import InstructionLineParserFactory
from scaralang.core.service.parser.iscara_parser import IScaraParser
from scaralang.core.service.parser.lexer.scara_lexer_factory import ScaraLexerFactory
from scaralang.core.service.parser.scara_parser import ScaraParser
from scaralang.core.service.parser.splitter.token_line_splitter_factory import TokenLineSplitterFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.0'
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
            lexer=ScaraLexerFactory.create(),
            line_splitter=TokenLineSplitterFactory.create(),
            line_parser=InstructionLineParserFactory.create(),
        )
        self.assertIsInstance(parser, IScaraParser)

    def test_name_property(self) -> None:
        '''
            Verifies that name property returns expected identifier.
        '''
        parser = ScaraParser(
            lexer=ScaraLexerFactory.create(),
            line_splitter=TokenLineSplitterFactory.create(),
            line_parser=InstructionLineParserFactory.create(),
        )
        self.assertEqual(parser.name, 'scara_parser')


if __name__ == '__main__':
    main()
