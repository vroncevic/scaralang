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
    Implementation of subroutine macro expander inlining subroutine calls.
'''

from __future__ import annotations

from collections.abc import Sequence
from typing import ClassVar, Final

from scaralang.core.model.dsl.ast.command_type import ScaraCommandType
from scaralang.core.model.dsl.ast.instruction import ScaraInstruction
from scaralang.core.model.dsl.ast.instruction_param import ScaraInstructionParam
from scaralang.core.model.dsl.macro.subroutine import SubroutineDefinition
from scaralang.core.model.exceptions.semantic import ScaraSemanticError
from scaralang.core.model.exceptions.syntax import ScaraSyntaxError
from scaralang.core.service.compiler.macro.segmenter.isegmenter import ISegmenter
from scaralang.core.service.compiler.macro.subroutine.iregistry import ISubroutineRegistry

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class SubroutineExpander:
    '''
        Expander component resolving and inlining subroutines.

        It defines:

            :attributes:
                | MAX_RECURSION_DEPTH - Maximum allowed call stack nesting depth.
                | _registry - Injected ISubroutineRegistry component.
                | _segmenter - Injected ISegmenter component.
            :methods:
                | __init__ - Initializes SubroutineExpander with registry and segmenter.
                | expand_subroutines - Inlines subroutines into linear stream.
                | expand_with_depth - Recursively expands subroutines with nesting tracking.
                | get_version - Returns expander component version string.
    '''

    MAX_RECURSION_DEPTH: ClassVar[int] = 16

    _registry: ISubroutineRegistry
    _segmenter: ISegmenter

    def __init__(
        self,
        *,
        registry: ISubroutineRegistry,
        segmenter: ISegmenter,
    ) -> None:
        '''
            Initializes SubroutineExpander with injected collaborators.

            :param registry: Injected ISubroutineRegistry component.
            :param segmenter: Injected ISegmenter component.
            :exceptions: None.
        '''
        self._registry: Final[ISubroutineRegistry] = registry
        self._segmenter: Final[ISegmenter] = segmenter

    def expand_subroutines(
        self,
        *,
        instructions: Sequence[ScaraInstruction],
    ) -> tuple[ScaraInstruction, ...]:
        '''
            Registers subroutine definitions and inlines called subroutines.

            :param instructions: Input sequence of parsed AST instructions.
            :return: Linear sequence of fully expanded instructions.
            :exceptions:
                | ScaraSyntaxError: On block syntax errors or orphaned END statements.
                | ScaraSemanticError: On unknown subroutine or recursion overflow.
        '''
        return self.expand_with_depth(instructions=instructions, depth=0)

    def expand_with_depth(
        self,
        *,
        instructions: Sequence[ScaraInstruction],
        depth: int,
    ) -> tuple[ScaraInstruction, ...]:
        '''
            Recursively expands subroutines with call stack depth tracking.

            :param instructions: Input sequence of instructions to expand.
            :param depth: Current recursion nesting depth level.
            :return: Expanded tuple of linear ScaraInstruction instances.
            :exceptions:
                | ScaraSyntaxError: On block syntax errors or orphaned END statements.
                | ScaraSemanticError: On unknown subroutine or recursion overflow.
        '''
        result: list[ScaraInstruction] = []
        curr_idx: int = 0
        total_len: int = len(instructions)

        while curr_idx < total_len:
            inst: ScaraInstruction = instructions[curr_idx]

            if inst.command_type == ScaraCommandType.DEF:
                end_idx, body = self._segmenter.segment_block(
                    instructions=instructions, start_index=curr_idx
                )
                name_obj: object = inst.parameters[ScaraInstructionParam.NAME]
                sub_def = SubroutineDefinition(
                    name=str(name_obj),
                    instructions=body,
                    line_number=inst.line_number,
                )
                self._registry.register(definition=sub_def)
                curr_idx = end_idx + 1

            elif inst.command_type == ScaraCommandType.CALL:
                if depth >= self.MAX_RECURSION_DEPTH:
                    name_obj = inst.parameters[ScaraInstructionParam.NAME]
                    raise ScaraSemanticError(
                        f'Maximum subroutine recursion depth ({self.MAX_RECURSION_DEPTH}) '
                        f'exceeded calling {name_obj!r} at line {inst.line_number}'
                    )
                name_obj = inst.parameters[ScaraInstructionParam.NAME]
                sub_def = self._registry.lookup(name=str(name_obj))
                expanded_sub = self.expand_with_depth(
                    instructions=sub_def.instructions, depth=depth + 1
                )
                result.extend(expanded_sub)
                curr_idx += 1

            elif inst.command_type == ScaraCommandType.REPEAT:
                end_idx, body = self._segmenter.segment_block(
                    instructions=instructions, start_index=curr_idx
                )
                expanded_body = self.expand_with_depth(
                    instructions=body, depth=depth
                )
                result.append(inst)
                result.extend(expanded_body)
                result.append(instructions[end_idx])
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
