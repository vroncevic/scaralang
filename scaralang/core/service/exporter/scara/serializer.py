# -*- coding: UTF-8 -*-

'''
Module
    serializer.py
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
    Service providing dictionary serialization for SCARA DSL AST programs and instructions.
'''

from __future__ import annotations

from scaralang.core.model.dsl.ast.instruction import ScaraInstruction
from scaralang.core.model.dsl.ast.program import ScaraProgram

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ProgramSerializer:
    '''
        Domain service for serializing SCARA AST trees to dictionary representations.

        It defines:

            :methods:
                | serialize_instruction - Serializes single instruction node to dictionary.
                | serialize_program - Serializes entire program AST root to dictionary.
                | get_version - Returns the serializer version string.
    '''

    @classmethod
    def serialize_instruction(
        cls,
        *,
        instruction: ScaraInstruction,
    ) -> dict[str, object]:
        '''
            Serializes a ScaraInstruction node to dictionary format.

            :param instruction: ScaraInstruction instance to serialize.
            :return: Dictionary representation of the instruction.
            :exceptions: None.
        '''
        return {
            'command_type': instruction.command_type.value,
            'line_number': instruction.line_number,
            'raw_text': instruction.raw_text,
            'parameters': dict(instruction.parameters),
        }

    @classmethod
    def serialize_program(
        cls,
        *,
        program: ScaraProgram,
    ) -> dict[str, object]:
        '''
            Serializes an ScaraProgram root to dictionary format.

            :param program: ScaraProgram instance to serialize.
            :return: Dictionary representation of the program.
            :exceptions: None.
        '''
        return {
            'instruction_count': len(program.instructions),
            'instructions': [
                cls.serialize_instruction(instruction=inst)
                for inst in program.instructions
            ],
        }

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the serializer version string.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return __version__
