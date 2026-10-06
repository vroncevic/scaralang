# -*- coding: UTF-8 -*-

'''
Module
    arc_point_calculator.py
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
    Calculates interpolated coordinates and transformed endpoints along circular arc paths.
'''

from __future__ import annotations

from collections.abc import Sequence
from typing import Final

from scaralang.core.model.dsl.ast.command_type import ScaraCommandType
from scaralang.core.model.dsl.ast.instruction import ScaraInstruction
from scaralang.core.model.dsl.ast.instruction_param import InstructionParam
from scaralang.core.model.dsl.compiler.arc_geometry import ArcGeometry
from scaralang.core.model.dsl.compiler.scara_compiler_context import ScaraCompilerContext
from scaralang.core.model.kinematics.point_2d import Point2D
from scaralang.core.model.trajectory.arc_point import ArcPoint
from scaralang.core.service.transformation.iframe_transformer import IFrameTransformer
from scaralang.core.service.compiler.motion.arc.interpolation.iarc_interpolator import IArcInterpolator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.6'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ArcPointCalculator:
    '''
        Calculates transformed endpoints and interpolated coordinates for circular arc instructions.

        It defines:

            :attributes:
                | _frame_transformer - Coordinate frame transformer collaborator.
                | _arc_interpolator - Circular arc interpolator collaborator.
            :methods:
                | __init__ - Initializes calculator with frame transformer and arc interpolator.
                | calculate_points - Computes transformed endpoints and interpolated coordinates.
                | get_version - Gets implementation version string.
    '''

    _frame_transformer: IFrameTransformer
    _arc_interpolator: IArcInterpolator

    def __init__(
        self,
        *,
        frame_transformer: IFrameTransformer,
        arc_interpolator: IArcInterpolator,
    ) -> None:
        '''
            Initializes ArcPointCalculator with injected helpers.

            :param frame_transformer: Injected IFrameTransformer instance.
            :param arc_interpolator: Injected IArcInterpolator instance.
            :exceptions: None.
        '''
        self._frame_transformer: Final[IFrameTransformer] = frame_transformer
        self._arc_interpolator: Final[IArcInterpolator] = arc_interpolator

    def calculate_points(
        self,
        *,
        instruction: ScaraInstruction,
        context: ScaraCompilerContext,
    ) -> tuple[Sequence[ArcPoint], Point2D]:
        '''
            Calculates transformed endpoints and generates interpolated arc points.

            :param instruction: Primitive AST instruction node.
            :param context: Mutable compiler execution context.
            :return: Tuple containing arc points sequence and transformed target point.
            :exceptions: None.
        '''
        params = instruction.parameters
        is_cw: bool = instruction.command_type == ScaraCommandType.ARC_CW
        target_x_raw: float = float(
            params.get(InstructionParam.X, context.pose.current_x)
        )
        target_y_raw: float = float(
            params.get(InstructionParam.Y, context.pose.current_y)
        )

        end_point: Point2D = self._frame_transformer.transform_point(
            frame=context.active_frame,
            point=Point2D(x=target_x_raw, y=target_y_raw),
        )

        geometry: ArcGeometry = ArcGeometry(
            start=Point2D(x=context.pose.current_x, y=context.pose.current_y),
            target=end_point,
            offset=Point2D(
                x=float(params.get(InstructionParam.I, 0.0)),
                y=float(params.get(InstructionParam.J, 0.0)),
            ),
            is_clockwise=is_cw,
        )
        arc_points: tuple[ArcPoint, ...] = (
            self._arc_interpolator.interpolate(geometry=geometry)
        )

        return (arc_points, end_point)

    def get_version(self) -> str:
        '''
            Gets implementation version string.

            :return: Version string.
            :exceptions: None.
        '''
        return __version__
