# -*- coding: UTF-8 -*-

'''
Module
    builder.py
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
    Implementation of ObstacleZone builder extracting geometry from instruction parameters.
'''

from __future__ import annotations

from scaralang.core.model.dsl.ast.instruction import ScaraInstruction
from scaralang.core.model.dsl.ast.instruction_param import ScaraInstructionParam
from scaralang.core.model.kinematics.pose.point_2d import Point2D
from scaralang.core.model.trajectory.obstacle.box import BoxObstacle
from scaralang.core.model.trajectory.obstacle.circle import CircleObstacle
from scaralang.core.model.trajectory.obstacle.shape import ObstacleShape
from scaralang.core.model.trajectory.obstacle.zone import ObstacleZone

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ZoneBuilder:
    '''
        Builds ObstacleZone models from parsed ZONE_DEF instruction parameter dictionaries.

        It defines:

            :methods:
                | __init__ - Initializes ZoneBuilder instance.
                | build_zone - Constructs an ObstacleZone from a ZONE_DEF instruction.
                | get_version - Gets implementation version string.
    '''

    def __init__(self) -> None:
        '''Initializes ZoneBuilder instance.'''

    def build_zone(
        self,
        *,
        instruction: ScaraInstruction,
    ) -> ObstacleZone:
        '''
            Constructs an ObstacleZone model from parsed instruction parameters.

            :param instruction: ScaraInstruction representing ZONE_DEF command.
            :return: Fully configured ObstacleZone domain instance.
            :exceptions: None.
        '''
        params: dict[str, object] = instruction.parameters
        name: str = str(params[ScaraInstructionParam.NAME.value])
        shape = ObstacleShape(str(params[ScaraInstructionParam.SHAPE.value]))

        match shape:
            case ObstacleShape.BOX:
                geometry: BoxObstacle | CircleObstacle = BoxObstacle(
                    x_min=float(params[ScaraInstructionParam.X_MIN.value]),  # type: ignore[arg-type]
                    x_max=float(params[ScaraInstructionParam.X_MAX.value]),  # type: ignore[arg-type]
                    y_min=float(params[ScaraInstructionParam.Y_MIN.value]),  # type: ignore[arg-type]
                    y_max=float(params[ScaraInstructionParam.Y_MAX.value]),  # type: ignore[arg-type]
                )
            case ObstacleShape.CIRCLE:
                geometry = CircleObstacle(
                    center=Point2D(
                        x=float(params[ScaraInstructionParam.X.value]),  # type: ignore[arg-type]
                        y=float(params[ScaraInstructionParam.Y.value]),  # type: ignore[arg-type]
                    ),
                    radius=float(params[ScaraInstructionParam.RADIUS.value]),  # type: ignore[arg-type]
                )

        return ObstacleZone(name=name, shape=shape, geometry=geometry)

    def get_version(self) -> str:
        '''
            Gets implementation version string.

            :return: Version string.
            :exceptions: None.
        '''
        return __version__
