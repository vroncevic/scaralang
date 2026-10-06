# -*- coding: UTF-8 -*-

'''
Module
    scara_source_generator.py
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
    Service providing source code unparsing and text generation from SCARA AST programs.
'''

from __future__ import annotations

from scaralang.core.model.dsl.ast.instruction import ScaraInstruction
from scaralang.core.model.dsl.ast.program import ScaraProgram

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.6'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ScaraSourceGenerator:
    '''
        Domain service for unparsing Program AST structures back into DSL source text.

        It defines:

            :methods:
                | format_instruction - Formats single ScaraInstruction AST node into text.
                | generate_source - Reconstructs .scara source code string from AST.
    '''

    @classmethod
    def format_instruction(cls, *, instruction: ScaraInstruction) -> str:
        '''
            Formats a single ScaraInstruction AST node into a DSL code line.

            :param instruction: ScaraInstruction AST node.
            :return: Formatted instruction string.
            :exceptions: None.
        '''
        if instruction.raw_text:
            return instruction.raw_text

        params_str: str = ' '.join(
            f'{k}={v}' for k, v in instruction.parameters.items()
        )

        return f'{instruction.command_type.value} {params_str}'.strip()

    @classmethod
    def generate_source(cls, *, program: ScaraProgram) -> str:
        '''
            Serializes an ScaraProgram back into standard .scara DSL source text.

            :param program: ScaraProgram AST root.
            :return: Formatted source text string.
            :exceptions: None.
        '''
        lines: list[str] = [
            cls.format_instruction(instruction=inst)
            for inst in program.instructions
        ]

        return '\n'.join(lines)
