# -*- coding: UTF-8 -*-

'''
Module
    compiler.py
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
    Compiles Cartesian linear and joint motion DSL instructions (MOVE_L, MOVE_J) into waypoints.
'''

from __future__ import annotations

from typing import ClassVar, Final

from scaralang.core.model.dsl.ast.command_type import ScaraCommandType
from scaralang.core.model.dsl.ast.instruction import ScaraInstruction
from scaralang.core.model.dsl.ast.instruction_param import ScaraInstructionParam
from scaralang.core.model.dsl.ast.tool_orient_mode import ToolOrientMode
from scaralang.core.model.dsl.compiler.context import CompilerContext
from scaralang.core.model.kinematics.pose.point_2d import Point2D
from scaralang.core.model.kinematics.pose.point_3d import Point3D
from scaralang.core.model.trajectory.plan.waypoint import Waypoint
from scaralang.core.service.compiler.primitive.motion.cartesian.itangent_heading_calculator import ITangentHeadingCalculator
from scaralang.core.service.transformation.itransformer import ITransformer

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class CartesianMoveCompiler:
    '''
        Sub-compiler handling Cartesian linear and joint motion instructions (MOVE_L, MOVE_J).

        It defines:

            :attributes:
                | _PERCENT_DIVISOR - Scale factor converting percentage values to unit ratios.
                | _SUPPORTED - Frozenset of handled ScaraCommandType instances.
                | _tangent_calculator - Tangent heading angle calculator helper.
                | _frame_transformer - Coordinate frame transformer service.
            :methods:
                | __init__ - Initializes Cartesian move compiler with injected helpers.
                | can_compile - Checks if command is a Cartesian motion instruction.
                | compile - Transforms coordinate frames and appends motion waypoints.
                | get_version - Gets implementation version string.
    '''

    _PERCENT_DIVISOR: ClassVar[float] = 100.0

    _SUPPORTED: frozenset[ScaraCommandType] = frozenset({
        ScaraCommandType.MOVE_L,
        ScaraCommandType.MOVE_J,
    })

    _tangent_calculator: ITangentHeadingCalculator
    _frame_transformer: ITransformer

    def __init__(
        self,
        *,
        tangent_calculator: ITangentHeadingCalculator,
        frame_transformer: ITransformer,
    ) -> None:
        '''
            Initializes CartesianMoveCompiler with injected tangent calculator and frame transformer.

            :param tangent_calculator: Injected ITangentHeadingCalculator helper for heading calculation.
            :param frame_transformer: Injected ITransformer instance.
            :exceptions: None.
        '''
        self._tangent_calculator: Final[ITangentHeadingCalculator] = (
            tangent_calculator
        )
        self._frame_transformer: Final[ITransformer] = frame_transformer

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
        context: CompilerContext,
    ) -> tuple[Waypoint, ...]:
        '''
            Processes Cartesian linear and joint motion instructions and returns computed waypoints.

            :param instruction: Primitive AST instruction node.
            :param context: Mutable compiler execution context.
            :return: Tuple containing compiled Waypoint instance.
            :exceptions: None.
        '''
        params = instruction.parameters
        raw_x: float = float(
            params.get(ScaraInstructionParam.X, context.pose.current_x)
        )
        raw_y: float = float(
            params.get(ScaraInstructionParam.Y, context.pose.current_y)
        )
        raw_z: float = (
            float(params[ScaraInstructionParam.Z])
            if ScaraInstructionParam.Z in params
            else context.pose.current_z - context.active_frame.origin.z
        )
        target_spd: float = float(
            params.get(ScaraInstructionParam.SPEED, context.speed.current_speed)
        )

        target_point: Point3D = self._frame_transformer.transform_point(
            frame=context.active_frame,
            point=Point3D(x=raw_x, y=raw_y, z=raw_z),
        )

        if context.tool_orient_mode == ToolOrientMode.TANGENTIAL:
            target_phi: float = (
                self._tangent_calculator.calculate_tangent_angle(
                    source=Point2D(
                        x=context.pose.current_x, y=context.pose.current_y
                    ),
                    target=Point2D(x=target_point.x, y=target_point.y),
                    fallback_phi=context.pose.current_phi,
                )
            )
        else:
            target_phi = float(
                params.get(ScaraInstructionParam.PHI, context.pose.current_phi)
            )

        effective_spd: float = target_spd * (
            context.speed.speed_override_pct / self._PERCENT_DIVISOR
        )

        waypoint = Waypoint(
            x=target_point.x,
            y=target_point.y,
            z=target_point.z,
            phi=target_phi,
            speed=effective_spd,
            name='',
            command='',
        )

        context.pose.current_x = target_point.x
        context.pose.current_y = target_point.y
        context.pose.current_z = target_point.z
        context.pose.current_phi = target_phi

        return (waypoint,)

    def get_version(self) -> str:
        '''
            Gets implementation version string.

            :return: Version string.
            :exceptions: None.
        '''
        return __version__
