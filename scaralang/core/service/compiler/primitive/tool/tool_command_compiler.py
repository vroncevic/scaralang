# -*- coding: UTF-8 -*-

'''
Module
    tool_command_compiler.py
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
    Compiles pneumatic tool actuation DSL instructions (pump and valve)
    into waypoints.
'''

from __future__ import annotations

from scaralang.core.model.dsl.ast.command_type import ScaraCommandType
from scaralang.core.model.dsl.ast.instruction import ScaraInstruction
from scaralang.core.model.dsl.ast.instruction_param import InstructionParam
from scaralang.core.model.dsl.ast.pneumatic_state import PneumaticState
from scaralang.core.model.dsl.compiler.scara_compiler_context import ScaraCompilerContext
from scaralang.core.model.trajectory.waypoint import Waypoint
from scaralang.core.service.compiler.primitive.tool.itool_waypoint_builder import IToolWaypointBuilder

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ToolCommandCompiler:
    '''
        Sub-compiler handling pneumatic tool actuation instructions (PUMP and VALVE).

        It defines:

            :attributes:
                | _SUPPORTED - Frozenset of handled ScaraCommandType instances.
                | _waypoint_builder - Collaborator building pneumatic tool waypoints.
            :methods:
                | __init__ - Initializes ToolCommandCompiler with injected waypoint builder.
                | can_compile - Checks if command is a tool actuation instruction.
                | compile - Appends pneumatic command waypoints to the waypoint accumulator.
    '''

    _SUPPORTED: frozenset[ScaraCommandType] = frozenset({
        ScaraCommandType.PUMP,
        ScaraCommandType.VALVE,
    })

    _waypoint_builder: IToolWaypointBuilder

    def __init__(
        self,
        *,
        waypoint_builder: IToolWaypointBuilder,
    ) -> None:
        '''
            Initializes ToolCommandCompiler with injected waypoint builder.

            :param waypoint_builder: Injected IToolWaypointBuilder instance.
            :exceptions: None.
        '''
        self._waypoint_builder = waypoint_builder

    def can_compile(self, *, instruction: ScaraInstruction) -> bool:
        '''
            Determines whether this sub-compiler handles the specified instruction.

            :param instruction: Primitive AST instruction node.
            :return: True if handled, False otherwise.
            :exceptions: None.
        '''
        return instruction.command_type in self._SUPPORTED

    def compile(
        self,
        *,
        instruction: ScaraInstruction,
        context: ScaraCompilerContext,
    ) -> tuple[Waypoint, ...]:
        '''
            Processes pneumatic instructions and returns tool command waypoints.

            :param instruction: Primitive AST instruction node.
            :param context: Mutable compiler execution context.
            :return: Tuple of compiled Waypoint instances.
            :exceptions: None.
        '''
        cmd_type = instruction.command_type

        if cmd_type not in self._SUPPORTED:
            return ()

        params = instruction.parameters
        raw_state = params.get(InstructionParam.STATE, PneumaticState.OFF)
        is_on: bool = str(raw_state).upper() == PneumaticState.ON
        state: PneumaticState = PneumaticState.ON if is_on else PneumaticState.OFF

        waypoint: Waypoint = self._waypoint_builder.build_waypoint(
            context=context,
            tool_type=cmd_type,
            state=state,
        )

        return (waypoint,)
