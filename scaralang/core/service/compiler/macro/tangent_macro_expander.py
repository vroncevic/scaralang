# -*- coding: UTF-8 -*-

'''
Module
    tangent_macro_expander.py
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
    Implementation of IMacroExpander adjusting 4th-axis tool orientation to follow path tangent.
'''

from __future__ import annotations

from math import atan2, degrees, hypot

from scaralang.core.model.dsl.ast.command_type import ScaraCommandType
from scaralang.core.model.dsl.ast.instruction import ScaraInstruction
from scaralang.core.model.dsl.ast.instruction_param import InstructionParam
from scaralang.core.model.dsl.ast.tool_orient_mode import ToolOrientMode
from scaralang.core.model.dsl.compiler.scara_compiler_context import ScaraCompilerContext
from scaralang.core.model.kinematics.point_2d import Point2D

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TangentMacroExpander:
    '''
        Macro expander computing tangential orientation for the 4th wrist roll axis along path.

        It defines:

            :attributes:
                | None.
            :methods:
                | can_expand - Checks if instruction requires tangential Phi or orientation.
                | expand - Updates tool orientation mode and heading in compiler context.
                | calculate_tangent_angle - Computes tangent heading angle between two 2D points.
    '''

    def can_expand(self, *, instruction: ScaraInstruction) -> bool:
        '''
            Checks whether this expander handles TOOL_ORIENT instructions.

            :param instruction: ScaraInstruction node to check.
            :return: True if TOOL_ORIENT, False otherwise.
        '''
        return instruction.command_type == ScaraCommandType.TOOL_ORIENT

    def expand(
        self,
        *,
        instruction: ScaraInstruction,
        context: ScaraCompilerContext,
    ) -> tuple[ScaraInstruction, ...]:
        '''
            Configures tool orientation mode in compiler context.

            :param instruction: TOOL_ORIENT instruction node.
            :param context: Active compiler context.
            :return: Empty tuple since orientation configuration mutates context only.
        '''
        params = instruction.parameters
        raw_mode = str(
            params.get(InstructionParam.MODE, ToolOrientMode.FIXED)
        ).upper()
        context.tool_orient_mode = (
            ToolOrientMode(raw_mode)
            if raw_mode in (
                ToolOrientMode.FIXED,
                ToolOrientMode.TANGENTIAL,
                ToolOrientMode.JOINT_LOCKED,
            )
            else ToolOrientMode.FIXED
        )

        if InstructionParam.PHI in params:
            context.pose.current_phi = float(params[InstructionParam.PHI])

        return ()

    @classmethod
    def calculate_tangent_angle(
        cls,
        *,
        source: Point2D,
        target: Point2D,
        fallback_phi: float,
    ) -> float:
        '''
            Computes tangent heading angle in degrees between two 2D points.

            :param source: Source 2D point coordinates.
            :param target: Destination 2D point coordinates.
            :param fallback_phi: Heading to return if travel distance is zero.
            :return: Heading angle in degrees [-180, +180].
        '''
        dx = target.x - source.x
        dy = target.y - source.y
        dist = hypot(dx, dy)

        if dist < 1e-4:
            return fallback_phi

        return degrees(atan2(dy, dx))
