# -*- coding: UTF-8 -*-

'''
Module
    pipeline.py
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
from scaralang.core.model.kinematics.solver.elbow import ElbowConfig
from scaralang.core.model.trajectory.plan.waypoint import Waypoint
from scaralang.core.service.compiler.context.factory import CompilerContextFactory
from scaralang.core.service.compiler.instruction.processor.iprocessor import IPrimitiveInstructionProcessor
from scaralang.core.service.compiler.macro.iexpander import IMacroExpander
from scaralang.core.service.compiler.macro.repeat.iexpander import IRepeatExpander
from scaralang.core.service.compiler.macro.subroutine.iexpander import ISubroutineExpander

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class InstructionPipeline:
    '''
        Compiler execution pipeline expanding macros and compiling primitive instructions.

        It defines:

            :attributes:
                | _subroutine_expander - Injected ISubroutineExpander component.
                | _repeat_expander - Injected IRepeatExpander component.
                | _macro_expanders - Registered IMacroExpander components.
                | _processor - Injected IPrimitiveInstructionProcessor component.
                | _elbow_configs - Recorded active elbow configuration for each compiled waypoint.
            :methods:
                | __init__ - Initializes pipeline with expanders and processor.
                | compile_instructions - Expands and compiles AST instructions into Waypoints.
                | get_elbow_configs - Returns the active elbow configuration sequence.
                | get_version - Returns the pipeline version string.
    '''

    _subroutine_expander: ISubroutineExpander
    _repeat_expander: IRepeatExpander
    _macro_expanders: tuple[IMacroExpander, ...]
    _processor: IPrimitiveInstructionProcessor
    _elbow_configs: tuple[ElbowConfig, ...]

    def __init__(
        self,
        *,
        subroutine_expander: ISubroutineExpander,
        repeat_expander: IRepeatExpander,
        macro_expanders: Sequence[IMacroExpander],
        processor: IPrimitiveInstructionProcessor,
    ) -> None:
        '''
            Initializes InstructionPipeline with injected expanders and processor.

            :param subroutine_expander: Injected ISubroutineExpander component.
            :param repeat_expander: Injected IRepeatExpander component.
            :param macro_expanders: Sequence of IMacroExpander components.
            :param processor: Injected IPrimitiveInstructionProcessor component.
            :exceptions: None.
        '''
        self._subroutine_expander: Final[ISubroutineExpander] = (
            subroutine_expander
        )
        self._repeat_expander: Final[IRepeatExpander] = repeat_expander
        self._macro_expanders: Final[tuple[IMacroExpander, ...]] = tuple(
            macro_expanders
        )
        self._processor: Final[IPrimitiveInstructionProcessor] = processor
        self._elbow_configs = ()

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
        context = CompilerContextFactory.create()
        waypoints: list[Waypoint] = []
        configs: list[ElbowConfig] = []
        sub_expanded: tuple[ScaraInstruction, ...] = (
            self._subroutine_expander.expand_subroutines(
                instructions=instructions
            )
        )
        linear_instructions: tuple[ScaraInstruction, ...] = (
            self._repeat_expander.expand_repeats(instructions=sub_expanded)
        )

        for inst in linear_instructions:
            expanded = False

            for expander in self._macro_expanders:
                if expander.can_expand(instruction=inst):
                    for new_inst in expander.expand(
                        instruction=inst, context=context
                    ):
                        pts = self._processor.process_primitive(
                            instruction=new_inst, context=context
                        )
                        waypoints.extend(pts)
                        configs.extend([context.pose.elbow_config] * len(pts))
                    expanded = True
                    break

            if not expanded:
                pts = self._processor.process_primitive(
                    instruction=inst, context=context
                )
                waypoints.extend(pts)
                configs.extend([context.pose.elbow_config] * len(pts))

        self._elbow_configs = tuple(configs)

        return waypoints

    def get_elbow_configs(self) -> tuple[ElbowConfig, ...]:
        '''
            Returns the active elbow configuration sequence for each compiled waypoint.

            :return: Tuple of ElbowConfig instances matching waypoints 1:1.
            :exceptions: None.
        '''
        return self._elbow_configs

    def get_version(self) -> str:
        '''
            Returns the pipeline version string representation.

            :return: Version string representation.
            :exceptions: None.
        '''
        return __version__
