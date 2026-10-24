# -*- coding: UTF-8 -*-

'''
Module
    segmenter.py
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
    Implementation of block boundary segmenter locating matching END instructions.
'''

from __future__ import annotations

from collections.abc import Sequence

from scaralang.core.model.dsl.ast.command_type import ScaraCommandType
from scaralang.core.model.dsl.ast.instruction import ScaraInstruction
from scaralang.core.model.exceptions.syntax import ScaraSyntaxError

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class BlockSegmenter:
    '''
        Scans instruction sequences to identify nested block boundaries and matching END statements.

        It defines:

            :methods:
                | __init__ - Initializes BlockSegmenter constructor.
                | segment_block - Locates matching END index and extracts body instruction slice.
                | get_version - Returns segmenter component version string.
    '''

    def __init__(self) -> None:
        '''
            Initializes BlockSegmenter constructor.

            :exceptions: None.
        '''

    def segment_block(
        self,
        *,
        instructions: Sequence[ScaraInstruction],
        start_index: int,
    ) -> tuple[int, tuple[ScaraInstruction, ...]]:
        '''
            Scans instruction sequence from start_index to locate matching END token.

            :param instructions: Complete sequence of AST instructions.
            :param start_index: Index of block opening instruction (DEF or REPEAT).
            :return: Tuple of index of matching END instruction and extracted body instructions.
            :exceptions:
                | ScaraSyntaxError: If block is not closed with a matching END.
        '''
        start_inst: ScaraInstruction = instructions[start_index]
        nesting: int = 1
        curr_index: int = start_index + 1
        total_instructions: int = len(instructions)

        while curr_index < total_instructions:
            inst: ScaraInstruction = instructions[curr_index]

            if inst.command_type in (
                ScaraCommandType.DEF,
                ScaraCommandType.REPEAT,
            ):
                nesting += 1

            elif inst.command_type == ScaraCommandType.END:
                nesting -= 1
                if nesting == 0:
                    body: tuple[ScaraInstruction, ...] = tuple(
                        instructions[start_index + 1 : curr_index]
                    )
                    return curr_index, body

            curr_index += 1

        raise ScaraSyntaxError(
            f'Unterminated block {start_inst.command_type} opened at line {start_inst.line_number}'
        )

    def get_version(self) -> str:
        '''
            Returns component version string representation.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return __version__
