# -*- coding: UTF-8 -*-

'''
Module
    planner.py
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
    Implementation of shape contour planner with automated obstacle detour routing.
'''

from __future__ import annotations

from typing import Final, Sequence

from scaralang.core.model.kinematics.point_2d import Point2D
from scaralang.core.model.trajectory.waypoint import Waypoint
from scaralang.core.service.trajectory.avoidance.bypass.planner.iplanner import IDeadZoneBypassPlanner
from scaralang.core.service.trajectory.avoidance.shape.dependencies import ShapeDependencies
from scaralang.core.service.trajectory.avoidance.validation.ivalidator import IDeadZoneValidator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.8'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class AvoidanceShapePlanner:
    '''
        Service planning geometric contours with automated dead zone detour routing.

        It defines:

            :attributes:
                | _validator - Injected dead zone validation port.
                | _bypass_planner - Injected dead zone bypass planner port.
            :methods:
                | __init__ - Initializes AvoidanceShapePlanner with dependencies bundle.
                | plan_contour - Plans geometric contour with dead zone avoidance detours.
                | get_version - Returns planner component version string.
    '''

    _validator: IDeadZoneValidator
    _bypass_planner: IDeadZoneBypassPlanner

    def __init__(self, dependencies: ShapeDependencies) -> None:
        '''
            Initializes AvoidanceShapePlanner with required avoidance collaborators.

            :param dependencies: Injected ShapeDependencies container bundle.
            :exceptions: None.
        '''
        self._validator: Final[IDeadZoneValidator] = dependencies.validator
        self._bypass_planner: Final[IDeadZoneBypassPlanner] = (
            dependencies.bypass_planner
        )

    def plan_contour(
        self,
        points: Sequence[Point2D],
        *,
        z: float,
        speed: float,
        closed: bool = True,
    ) -> list[Waypoint]:
        '''
            Plans sequence of coordinates with automated dead zone avoidance detours.

            :param points: Sequence of Point2D vertices defining the shape contour.
            :param z: Z vertical height coordinate in mm.
            :param speed: Feedrate speed in mm/s.
            :param closed: Whether to close the contour by connecting back to the start.
            :return: List of Waypoint instances with detours inserted where needed.
            :exceptions: None.
        '''
        if not points:
            return []

        if len(points) == 1:
            return [Waypoint(x=points[0].x, y=points[0].y, z=z, speed=speed)]

        vertices: list[Point2D] = list(points)

        if closed and (
            vertices[0].x != vertices[-1].x or vertices[0].y != vertices[-1].y
        ):
            vertices.append(vertices[0])

        result: list[Waypoint] = [
            Waypoint(x=vertices[0].x, y=vertices[0].y, z=z, speed=speed)
        ]

        for i in range(len(vertices) - 1):
            p_start: Point2D = vertices[i]
            p_end: Point2D = vertices[i + 1]

            if self._validator.is_segment_crossing_dead_zone(p_start, p_end):
                detour: list[Waypoint] = self._bypass_planner.plan_bypass(
                    p_start,
                    p_end,
                    z=z,
                    speed=speed,
                )
                result.extend(detour)
            else:
                result.append(
                    Waypoint(x=p_end.x, y=p_end.y, z=z, speed=speed)
                )

        return result

    def get_version(self) -> str:
        '''
            Returns planner component version string representation.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return __version__
