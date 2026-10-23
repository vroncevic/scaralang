# -*- coding: UTF-8 -*-

'''
Module
    router.py
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
    Implementation of unified safe trajectory routing with dead zone avoidance.
'''

from __future__ import annotations

from collections.abc import Sequence
from typing import Final

from scaralang.core.model.kinematics.pose.point_2d import Point2D
from scaralang.core.model.trajectory.plan.waypoint import Waypoint
from scaralang.core.service.trajectory.avoidance.bypass.planner.iplanner import IDeadZoneBypassPlanner
from scaralang.core.service.trajectory.avoidance.router.dependencies import RouterDependencies
from scaralang.core.service.trajectory.avoidance.validation.ivalidator import IDeadZoneValidator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class SafeTrajectoryRouter:
    '''
        Service planning unified trajectories with automated dead zone detour avoidance routing.

        It defines:

            :attributes:
                | _validator - Injected dead zone validation port.
                | _bypass_planner - Injected dead zone bypass path planner port.
            :methods:
                | __init__ - Initializes router with injected dependencies bundle.
                | plan_safe_trajectory - Plans complete safe trajectory bypassing dead zones.
                | get_version - Returns router component version string.
    '''

    _validator: IDeadZoneValidator
    _bypass_planner: IDeadZoneBypassPlanner

    def __init__(self, dependencies: RouterDependencies) -> None:
        '''
            Initializes SafeTrajectoryRouter with required avoidance collaborators.

            :param dependencies: Injected RouterDependencies container bundle.
            :exceptions: None.
        '''
        self._validator: Final[IDeadZoneValidator] = dependencies.validator
        self._bypass_planner: Final[IDeadZoneBypassPlanner] = (
            dependencies.bypass_planner
        )

    def plan_safe_trajectory(
        self,
        start_point: Waypoint,
        waypoints: Sequence[Waypoint],
    ) -> list[Waypoint]:
        '''
            Plans trajectory from start point through all waypoints with dead zone avoidance.

            :param start_point: Current physical or starting position of the manipulator.
            :param waypoints: Sequence of planned target waypoints to traverse.
            :return: Ordered list of safe waypoints with detour arcs inserted where needed.
            :exceptions: None.
        '''
        if not waypoints:
            return []

        result: list[Waypoint] = []
        current_point: Waypoint = start_point

        for target_point in waypoints:
            p_start: Point2D = Point2D(x=current_point.x, y=current_point.y)
            p_end: Point2D = Point2D(x=target_point.x, y=target_point.y)

            if self._validator.is_segment_crossing_dead_zone(p_start, p_end):
                detour: list[Waypoint] = self._bypass_planner.plan_bypass(
                    p_start,
                    p_end,
                    z=target_point.z,
                    speed=target_point.speed,
                )
                if detour:
                    result.extend(detour[:-1])
                    result.append(target_point)
            else:
                result.append(target_point)

            current_point = target_point

        return result

    def get_version(self) -> str:
        '''
            Returns router component version string representation.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return __version__
