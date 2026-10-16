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

from collections.abc import Sequence
from typing import ClassVar, Final

from scaralang.core.model.kinematics.point_2d import Point2D
from scaralang.core.model.trajectory.waypoint import Waypoint
from scaralang.core.service.trajectory.avoidance.bypass.planner.iplanner import IDeadZoneBypassPlanner
from scaralang.core.service.trajectory.avoidance.shape.dependencies import ShapeDependencies
from scaralang.core.service.trajectory.avoidance.validation.ivalidator import IDeadZoneValidator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.9'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class AvoidanceShapePlanner:
    '''
        Service planning geometric contours with automated dead zone detour routing.

        It defines:

            :attributes:
                | DEFAULT_COMMAND - Default waypoint command string.
                | DEFAULT_NAME - Default waypoint identifier label.
                | DEFAULT_PHI - Default orientation angle in degrees.
                | FIRST_POINT_INDEX - Index of the first point in a sequence.
                | LAST_POINT_INDEX - Negative index of the last point in a sequence.
                | LOOP_OFFSET - Loop boundary offset for vertex segments.
                | NEXT_POINT_OFFSET - Index offset to next vertex point.
                | SINGLE_POINT_COUNT - Threshold count for single-point contour.
                | _validator - Injected dead zone validation port.
                | _bypass_planner - Injected dead zone bypass planner port.
            :methods:
                | __init__ - Initializes AvoidanceShapePlanner with dependencies bundle.
                | plan_contour - Plans geometric contour with dead zone avoidance detours.
                | get_version - Returns planner component version string.
    '''

    DEFAULT_COMMAND: ClassVar[str] = ''
    DEFAULT_NAME: ClassVar[str] = ''
    DEFAULT_PHI: ClassVar[float] = 0.0
    FIRST_POINT_INDEX: ClassVar[int] = 0
    LAST_POINT_INDEX: ClassVar[int] = -1
    LOOP_OFFSET: ClassVar[int] = 1
    NEXT_POINT_OFFSET: ClassVar[int] = 1
    SINGLE_POINT_COUNT: ClassVar[int] = 1

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

        if len(points) == self.SINGLE_POINT_COUNT:
            pt: Point2D = points[self.FIRST_POINT_INDEX]
            return [
                Waypoint(
                    x=pt.x,
                    y=pt.y,
                    z=z,
                    phi=self.DEFAULT_PHI,
                    speed=speed,
                    name=self.DEFAULT_NAME,
                    command=self.DEFAULT_COMMAND,
                )
            ]

        vertices: list[Point2D] = list(points)
        first_pt: Point2D = vertices[self.FIRST_POINT_INDEX]
        last_pt: Point2D = vertices[self.LAST_POINT_INDEX]

        if closed and (first_pt.x != last_pt.x or first_pt.y != last_pt.y):
            vertices.append(first_pt)

        result: list[Waypoint] = [
            Waypoint(
                x=first_pt.x,
                y=first_pt.y,
                z=z,
                phi=self.DEFAULT_PHI,
                speed=speed,
                name=self.DEFAULT_NAME,
                command=self.DEFAULT_COMMAND,
            )
        ]

        for i in range(len(vertices) - self.LOOP_OFFSET):
            p_start: Point2D = vertices[i]
            p_end: Point2D = vertices[i + self.NEXT_POINT_OFFSET]

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
                    Waypoint(
                        x=p_end.x,
                        y=p_end.y,
                        z=z,
                        phi=self.DEFAULT_PHI,
                        speed=speed,
                        name=self.DEFAULT_NAME,
                        command=self.DEFAULT_COMMAND,
                    )
                )

        return result

    def get_version(self) -> str:
        '''
            Returns planner component version string representation.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return __version__
