# -*- coding: UTF-8 -*-

'''
Module
    expander.py
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
    Implementation of repeat loop macro expander unrolling loops.
'''

from __future__ import annotations

from collections.abc import Sequence
from typing import Final

from scaralang.core.model.dsl.ast.command_type import ScaraCommandType
from scaralang.core.model.dsl.ast.instruction import ScaraInstruction
from scaralang.core.model.dsl.ast.instruction_param import ScaraInstructionParam
from scaralang.core.model.exceptions.syntax import ScaraSyntaxError
from scaralang.core.service.compiler.macro.segmenter.isegmenter import ISegmenter

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class RepeatExpander:
    '''
        Expander component unrolling repeat loops into linear instruction sequences.

        It defines:

            :attributes:
                | _segmenter - Injected ISegmenter component.
            :methods:
                | __init__ - Initializes RepeatExpander with segmenter.
                | expand_repeats - Unrolls repeat loops into linear stream.
                | get_version - Returns expander component version string.
    '''

    _segmenter: ISegmenter

    def __init__(
        self,
        *,
        segmenter: ISegmenter,
    ) -> None:
        '''
            Initializes RepeatExpander with injected segmenter.

            :param segmenter: Injected ISegmenter component.
            :exceptions: None.
        '''
        self._segmenter: Final[ISegmenter] = segmenter

    def expand_repeats(
        self,
        *,
        instructions: Sequence[ScaraInstruction],
    ) -> tuple[ScaraInstruction, ...]:
        '''
            Unrolls repeat loops into a linear stream.

            :param instructions: Input sequence of parsed AST instructions.
            :return: Linear sequence of fully expanded instructions.
            :exceptions:
                | ScaraSyntaxError: On block syntax errors or orphaned END statements.
        '''
        result: list[ScaraInstruction] = []
        curr_idx: int = 0
        total_len: int = len(instructions)

        while curr_idx < total_len:
            inst: ScaraInstruction = instructions[curr_idx]

            if inst.command_type == ScaraCommandType.REPEAT:
                end_idx, body = self._segmenter.segment_block(
                    instructions=instructions, start_index=curr_idx
                )
                count_obj: object = inst.parameters[ScaraInstructionParam.COUNT]
                count: int = int(count_obj)  # type: ignore[arg-type]
                expanded_body = self.expand_repeats(instructions=body)
                for _ in range(count):
                    result.extend(expanded_body)
                curr_idx = end_idx + 1

            elif inst.command_type == ScaraCommandType.END:
                raise ScaraSyntaxError(
                    f'Unexpected END statement without matching DEF or REPEAT at line {inst.line_number}'
                )

            else:
                result.append(inst)
                curr_idx += 1

        return tuple(result)

    def get_version(self) -> str:
        '''
            Returns component version string representation.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return __version__
