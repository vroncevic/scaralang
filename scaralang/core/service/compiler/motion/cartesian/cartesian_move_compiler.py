# -*- coding: UTF-8 -*-

'''
Module
    cartesian_move_compiler.py
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

from scaralang.core.model.dsl.ast.command_type import ScaraCommandType
from scaralang.core.model.dsl.ast.instruction import ScaraInstruction
from scaralang.core.model.dsl.ast.instruction_param import InstructionParam
from scaralang.core.model.dsl.ast.tool_orient_mode import ToolOrientMode
from scaralang.core.model.dsl.compiler.scara_compiler_context import ScaraCompilerContext
from scaralang.core.model.kinematics.point_2d import Point2D
from scaralang.core.model.trajectory.waypoint import Waypoint
from scaralang.core.service.compiler.frame.iframe_transformer import IFrameTransformer
from scaralang.core.service.compiler.macro.tangent_macro_expander import TangentMacroExpander

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class CartesianMoveCompiler:
    '''
        Sub-compiler handling Cartesian linear and joint motion instructions (MOVE_L, MOVE_J).

        It defines:

            :attributes:
                | _SUPPORTED - Frozenset of handled ScaraCommandType instances.
                | _tangent_helper - Tangent heading angle calculator helper.
                | _frame_transformer - Coordinate frame transformer service.
            :methods:
                | __init__ - Initializes Cartesian move compiler with injected helpers.
                | can_compile - Checks if command is a Cartesian motion instruction.
                | compile - Transforms coordinate frames and appends motion waypoints.
    '''

    _SUPPORTED: frozenset[ScaraCommandType] = frozenset({
        ScaraCommandType.MOVE_L,
        ScaraCommandType.MOVE_J,
    })

    _tangent_helper: TangentMacroExpander
    _frame_transformer: IFrameTransformer

    def __init__(
        self,
        *,
        tangent_helper: TangentMacroExpander,
        frame_transformer: IFrameTransformer,
    ) -> None:
        '''
            Initializes CartesianMoveCompiler with injected tangent helper and frame transformer.

            :param tangent_helper: Injected TangentMacroExpander helper for heading calculation.
            :param frame_transformer: Injected IFrameTransformer instance.
            :exceptions: None.
        '''
        self._tangent_helper = tangent_helper
        self._frame_transformer = frame_transformer

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
            Processes Cartesian linear and joint motion instructions and returns computed waypoints.

            :param instruction: Primitive AST instruction node.
            :param context: Mutable compiler execution context.
            :return: Tuple containing compiled Waypoint instance.
            :exceptions: None.
        '''
        params = instruction.parameters
        raw_x: float = float(params.get(InstructionParam.X, context.current_x))
        raw_y: float = float(params.get(InstructionParam.Y, context.current_y))
        target_z: float = float(params.get(InstructionParam.Z, context.current_z))
        target_spd: float = float(
            params.get(InstructionParam.SPEED, context.current_speed)
        )

        global_x, global_y = self._frame_transformer.transform_point(
            frame=context.active_frame,
            x=raw_x,
            y=raw_y,
        )

        if context.tool_orient_mode == ToolOrientMode.TANGENTIAL:
            target_phi: float = self._tangent_helper.calculate_tangent_angle(
                source=Point2D(x=context.current_x, y=context.current_y),
                target=Point2D(x=global_x, y=global_y),
                fallback_phi=context.current_phi,
            )
        else:
            target_phi = float(params.get(InstructionParam.PHI, context.current_phi))

        effective_spd: float = target_spd * (context.speed_override_pct / 100.0)

        waypoint = Waypoint(
            x=global_x,
            y=global_y,
            z=target_z,
            phi=target_phi,
            speed=effective_spd,
            name='',
            command='',
        )

        context.current_x = global_x
        context.current_y = global_y
        context.current_z = target_z
        context.current_phi = target_phi

        return (waypoint,)
