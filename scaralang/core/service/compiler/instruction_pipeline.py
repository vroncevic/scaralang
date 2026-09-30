# -*- coding: UTF-8 -*-

'''
Module
    instruction_pipeline.py
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
    Implementation of IInstructionPipeline managing macro expansion and primitive compilation loops.
'''

from __future__ import annotations

from collections.abc import Sequence
from typing import Final

from scaralang.core.model.dsl.ast.instruction import ScaraInstruction
from scaralang.core.model.dsl.compiler.scara_compiler_context import ScaraCompilerContext
from scaralang.core.model.trajectory.waypoint import Waypoint
from scaralang.core.service.compiler.iprimitive_instruction_processor import IPrimitiveInstructionProcessor
from scaralang.core.service.compiler.macro.imacro_expander import IMacroExpander

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class InstructionPipeline:
    '''
        Compiler execution pipeline expanding macros and compiling primitive instructions.

        It defines:

            :attributes:
                | _macro_expanders - Registered IMacroExpander components.
                | _processor - Injected IPrimitiveInstructionProcessor component.
            :methods:
                | __init__ - Initializes pipeline with expanders and processor.
                | compile_instructions - Expands and compiles AST instructions into Waypoints.
    '''

    _macro_expanders: tuple[IMacroExpander, ...]
    _processor: IPrimitiveInstructionProcessor

    def __init__(
        self,
        *,
        macro_expanders: Sequence[IMacroExpander],
        processor: IPrimitiveInstructionProcessor,
    ) -> None:
        '''
            Initializes InstructionPipeline with injected expanders and processor.

            :param macro_expanders: Sequence of IMacroExpander components.
            :param processor: Injected IPrimitiveInstructionProcessor component.
            :exceptions: None.
        '''
        self._macro_expanders: Final[tuple[IMacroExpander, ...]] = tuple(macro_expanders)
        self._processor: Final[IPrimitiveInstructionProcessor] = processor

    def compile_instructions(
        self,
        *,
        instructions: Sequence[ScaraInstruction],
    ) -> list[Waypoint]:
        '''
            Expands and compiles AST instructions into Waypoint list.

            :param instructions: Sequence of AST ScaraInstruction nodes.
            :return: Mutable list of compiled Waypoint instances.
            :exceptions: ValueError if instruction is unsupported.
        '''
        context = ScaraCompilerContext()
        waypoints: list[Waypoint] = []

        for inst in instructions:
            expanded = False

            for expander in self._macro_expanders:
                if expander.can_expand(instruction=inst):
                    for new_inst in expander.expand(
                        instruction=inst, context=context
                    ):
                        waypoints.extend(
                            self._processor.process_primitive(
                                instruction=new_inst,
                                context=context,
                            )
                        )
                    expanded = True
                    break

            if not expanded:
                waypoints.extend(
                    self._processor.process_primitive(
                        instruction=inst,
                        context=context,
                    )
                )

        return waypoints
