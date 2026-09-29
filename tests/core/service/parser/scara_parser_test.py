# -*- coding: UTF-8 -*-

'''
Module
    scara_parser_test.py
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
    Unit tests for ScaraParser implementation.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.model.dsl.ast.command_type import ScaraCommandType
from scaralang.core.model.dsl.ast.program import ScaraProgram
from scaralang.core.service.parser.instruction.instruction_line_parser_factory import InstructionLineParserFactory
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


class TestScaraParser(TestCase):
    '''
        Test cases verifying ScaraParser orchestration and AST generation.

        It defines:

            :methods:
                | setUp - Sets up test fixture with wired ScaraParser instance.
                | test_parse_program_success - Verifies parsing complete DSL program string.
                | test_parse_empty_source - Verifies parsing empty DSL string.
                | test_parse_tokens_direct - Verifies parsing token sequence directly.
                | test_parse_unknown_command_raises - Verifies ValueError on unknown command.
                | test_name_property - Verifies name property.
    '''

    def setUp(self) -> None:
        '''
            Sets up test fixture with wired ScaraParser instance.
        '''
        self.parser = ScaraParser(
            lexer=ScaraLexerFactory.create(),
            line_splitter=TokenLineSplitterFactory.create(),
            line_parser=InstructionLineParserFactory.create(),
        )

    def test_parse_program_success(self) -> None:
        '''
            Verifies parsing complete DSL program string into ScaraProgram.
        '''
        source = 'MOVE_J J1=90 J2=45\nMOVE_L X=100 Y=200 Z=50\n'
        program = self.parser.parse(source=source)
        self.assertIsInstance(program, ScaraProgram)
        self.assertEqual(len(program.instructions), 2)
        self.assertEqual(program.instructions[0].command_type, ScaraCommandType.MOVE_J)
        self.assertEqual(program.instructions[1].command_type, ScaraCommandType.MOVE_L)

    def test_parse_empty_source(self) -> None:
        '''
            Verifies parsing empty DSL string into ScaraProgram with no instructions.
        '''
        program = self.parser.parse(source='')
        self.assertIsInstance(program, ScaraProgram)
        self.assertEqual(len(program.instructions), 0)

    def test_parse_tokens_direct(self) -> None:
        '''
            Verifies parsing token sequence directly.
        '''
        lexer = ScaraLexerFactory.create()
        tokens = lexer.tokenize(source='MOVE_J J1=0\n')
        program = self.parser.parse_tokens(tokens=tokens)
        self.assertIsInstance(program, ScaraProgram)
        self.assertEqual(len(program.instructions), 1)

    def test_parse_unknown_command_raises(self) -> None:
        '''
            Verifies ValueError on unknown command.
        '''
        with self.assertRaises(ValueError):
            self.parser.parse(source='INVALID_COMMAND X=10\n')

    def test_name_property(self) -> None:
        '''
            Verifies name property returns expected identifier.
        '''
        self.assertEqual(self.parser.name, 'scara_parser')


if __name__ == '__main__':
    main()
