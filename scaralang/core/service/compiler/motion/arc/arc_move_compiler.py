# -*- coding: UTF-8 -*-

'''
Module
    arc_move_compiler.py
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
    Compiles circular arc DSL instructions (ARC_CW, ARC_CCW) using
    point calculator and waypoint builder.
'''

from __future__ import annotations

from collections.abc import Sequence
from typing import Final

from scaralang.core.model.dsl.ast.command_type import ScaraCommandType
from scaralang.core.model.dsl.ast.instruction import ScaraInstruction
from scaralang.core.model.dsl.ast.instruction_param import InstructionParam
from scaralang.core.model.dsl.compiler.scara_compiler_context import ScaraCompilerContext
from scaralang.core.model.kinematics.point_2d import Point2D
from scaralang.core.model.trajectory.arc_point import ArcPoint
from scaralang.core.model.trajectory.waypoint import Waypoint
from scaralang.core.service.compiler.motion.arc.builder.iarc_waypoint_builder import IArcWaypointBuilder
from scaralang.core.service.compiler.motion.arc.calculator.iarc_point_calculator import IArcPointCalculator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ArcMoveCompiler:
    '''
        Sub-compiler handling circular arc motion instructions (ARC_CW, ARC_CCW).

        It defines:

            :attributes:
                | _SUPPORTED - Frozenset of handled ScaraCommandType instances.
                | _point_calculator - Collaborator calculating interpolated arc endpoints.
                | _waypoint_builder - Collaborator building domain waypoints.
            :methods:
                | __init__ - Initializes ArcMoveCompiler with injected helpers.
                | can_compile - Checks if command is an arc motion instruction.
                | compile - Interpolates circular arc and appends interpolated waypoints.
    '''

    _SUPPORTED: frozenset[ScaraCommandType] = frozenset({
        ScaraCommandType.ARC_CW,
        ScaraCommandType.ARC_CCW,
    })

    _point_calculator: IArcPointCalculator
    _waypoint_builder: IArcWaypointBuilder

    def __init__(
        self,
        *,
        point_calculator: IArcPointCalculator,
        waypoint_builder: IArcWaypointBuilder,
    ) -> None:
        '''
            Initializes ArcMoveCompiler with point calculator and waypoint builder.

            :param point_calculator: Injected IArcPointCalculator component.
            :param waypoint_builder: Injected IArcWaypointBuilder component.
            :exceptions: None.
        '''
        self._point_calculator: Final[IArcPointCalculator] = point_calculator
        self._waypoint_builder: Final[IArcWaypointBuilder] = waypoint_builder

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
            Processes circular arc motion instructions and returns interpolated waypoints.

            :param instruction: Primitive AST instruction node.
            :param context: Mutable compiler execution context.
            :return: Tuple of compiled Waypoint instances.
            :exceptions: None.
        '''
        arc_points: Sequence[ArcPoint]
        end_point: Point2D
        arc_points, end_point = self._point_calculator.calculate_points(
            instruction=instruction, context=context,
        )
        params = instruction.parameters
        target_z: float = float(
            params.get(InstructionParam.Z, context.pose.current_z)
        )
        spd: float = float(
            params.get(InstructionParam.SPEED, context.speed.current_speed)
        )
        effective_spd: float = spd * (context.speed.speed_override_pct / 100.0)

        compiled: tuple[Waypoint, ...] = (
            self._waypoint_builder.build_waypoints(
                arc_points=arc_points,
                target_z=target_z,
                speed=effective_spd,
                context=context,
            )
        )

        context.pose.current_x = end_point.x
        context.pose.current_y = end_point.y
        context.pose.current_z = target_z

        return compiled
