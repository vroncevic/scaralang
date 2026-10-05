# -*- coding: UTF-8 -*-

'''
Module
    vertical_move_compiler.py
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
    Compiles vertical approach and retract motion DSL instructions
    (APPROACH, RETRACT) into waypoints.
'''

from __future__ import annotations

from scaralang.core.model.dsl.ast.command_type import ScaraCommandType
from scaralang.core.model.dsl.ast.instruction import ScaraInstruction
from scaralang.core.model.dsl.ast.instruction_param import InstructionParam
from scaralang.core.model.dsl.compiler.scara_compiler_context import ScaraCompilerContext
from scaralang.core.model.trajectory.waypoint import Waypoint

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class VerticalMoveCompiler:
    '''
        Sub-compiler handling vertical motion instructions (APPROACH, RETRACT).

        It defines:

            :attributes:
                | _SUPPORTED - Frozenset of handled ScaraCommandType instances.
            :methods:
                | can_compile - Checks if command is an APPROACH or RETRACT instruction.
                | compile - Adjusts height coordinates and appends vertical motion waypoints.
    '''

    _SUPPORTED: frozenset[ScaraCommandType] = frozenset({
        ScaraCommandType.APPROACH,
        ScaraCommandType.RETRACT,
    })

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
            Processes APPROACH and RETRACT instructions and returns computed waypoints.

            :param instruction: Primitive AST instruction node.
            :param context: Mutable compiler execution context.
            :return: Tuple containing compiled Waypoint instance.
            :exceptions: None.
        '''
        params = instruction.parameters
        cmd_type: ScaraCommandType = instruction.command_type
        dist: float = float(params.get(InstructionParam.DIST, 10.0))

        if cmd_type == ScaraCommandType.APPROACH:
            spd: float = float(
                params.get(InstructionParam.SPEED, context.speed.speed_work)
            )
            target_z: float = max(0.0, context.pose.current_z - dist)
            name: str = ScaraCommandType.APPROACH.value
        else:
            spd = float(
                params.get(InstructionParam.SPEED, context.speed.speed_rapid)
            )
            target_z = context.pose.current_z + dist
            name = ScaraCommandType.RETRACT.value

        context.pose.current_z = target_z
        waypoint = Waypoint(
            x=context.pose.current_x,
            y=context.pose.current_y,
            z=target_z,
            phi=context.pose.current_phi,
            speed=spd,
            name=name,
            command='',
        )

        return (waypoint,)
