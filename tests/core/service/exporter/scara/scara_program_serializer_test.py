# -*- coding: UTF-8 -*-

'''
Module
    scara_program_serializer_test.py
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
    Unit tests for ScaraProgramSerializer class.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.model.dsl.ast.command_type import ScaraCommandType
from scaralang.core.model.dsl.ast.instruction import ScaraInstruction
from scaralang.core.model.dsl.ast.program import ScaraProgram
from scaralang.core.service.exporter.scara.scara_program_serializer import ScaraProgramSerializer

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestScaraProgramSerializer(TestCase):
    '''
        Unit tests validating serialization of AST instructions and programs.

        It defines:

            :methods:
                | test_serialize_instruction - Verifies single instruction serialization.
                | test_serialize_program - Verifies complete program serialization.
    '''

    def test_serialize_instruction(self) -> None:
        '''Verify serializing a single instruction to dictionary representation.'''
        inst = ScaraInstruction(
            command_type=ScaraCommandType.MOVE_L,
            line_number=10,
            raw_text='MOVE_L X=15.0 Y=25.0',
            parameters={'X': 15.0, 'Y': 25.0},
        )
        serialized = ScaraProgramSerializer.serialize_instruction(
            instruction=inst
        )
        self.assertEqual(
            serialized,
            {
                'command_type': 'MOVE_L',
                'line_number': 10,
                'raw_text': 'MOVE_L X=15.0 Y=25.0',
                'parameters': {'X': 15.0, 'Y': 25.0},
            },
        )

    def test_serialize_program(self) -> None:
        '''Verify serializing a complete program to dictionary representation.'''
        inst = ScaraInstruction(
            command_type=ScaraCommandType.HOME,
            line_number=1,
            raw_text='HOME',
            parameters={},
        )
        program = ScaraProgram(instructions=(inst,))
        serialized = ScaraProgramSerializer.serialize_program(program=program)
        self.assertEqual(serialized['instruction_count'], 1)
        self.assertEqual(len(serialized['instructions']), 1)
        self.assertEqual(
            serialized['instructions'][0]['command_type'], 'HOME'
        )


if __name__ == '__main__':
    main()
