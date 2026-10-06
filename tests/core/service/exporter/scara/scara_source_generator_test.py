# -*- coding: UTF-8 -*-

'''
Module
    scara_source_generator_test.py
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
    Unit tests for ScaraSourceGenerator class.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.model.dsl.ast.command_type import ScaraCommandType
from scaralang.core.model.dsl.ast.instruction import ScaraInstruction
from scaralang.core.model.dsl.ast.program import ScaraProgram
from scaralang.core.service.exporter.scara.scara_source_generator import ScaraSourceGenerator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.6'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestScaraSourceGenerator(TestCase):
    '''
        Unit tests validating ScaraSourceGenerator DSL source code unparsing.

        It defines:

            :methods:
                | test_generate_source_empty - Verifies empty program produces empty string.
                | test_generate_source_multiple_instructions - Verifies source text unparsing.
                | test_format_instruction_raw - Verifies formatting instruction with raw text.
                | test_format_instruction_params - Verifies formatting instruction from parameters.
    '''

    def test_format_instruction_raw(self) -> None:
        '''Verify format_instruction returns raw_text when present.'''
        inst = ScaraInstruction(
            command_type=ScaraCommandType.HOME,
            line_number=1,
            raw_text='HOME',
            parameters={},
        )
        self.assertEqual(
            ScaraSourceGenerator.format_instruction(instruction=inst),
            'HOME',
        )

    def test_format_instruction_params(self) -> None:
        '''Verify format_instruction formats command and parameters when raw_text is empty.'''
        inst = ScaraInstruction(
            command_type=ScaraCommandType.MOVE_L,
            line_number=2,
            raw_text='',
            parameters={'X': 10.0, 'Y': 20.0},
        )
        self.assertEqual(
            ScaraSourceGenerator.format_instruction(instruction=inst),
            'MOVE_L X=10.0 Y=20.0',
        )

    def test_generate_source_empty(self) -> None:
        '''Verify that an empty program produces an empty string.'''
        program = ScaraProgram(instructions=())
        source = ScaraSourceGenerator.generate_source(program=program)
        self.assertEqual(source, '')

    def test_generate_source_multiple_instructions(self) -> None:
        '''Verify source text unparsing with newline termination.'''
        inst1 = ScaraInstruction(
            command_type=ScaraCommandType.HOME,
            line_number=1,
            raw_text='HOME',
            parameters={},
        )
        inst2 = ScaraInstruction(
            command_type=ScaraCommandType.MOVE_L,
            line_number=2,
            raw_text='MOVE_L X=100.0 Y=150.0',
            parameters={'X': 100.0, 'Y': 150.0},
        )
        program = ScaraProgram(instructions=(inst1, inst2))
        source = ScaraSourceGenerator.generate_source(program=program)
        self.assertEqual(source, 'HOME\nMOVE_L X=100.0 Y=150.0')


if __name__ == '__main__':
    main()
