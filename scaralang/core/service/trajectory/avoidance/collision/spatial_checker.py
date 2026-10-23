# -*- coding: UTF-8 -*-

'''
Module
    spatial_checker.py
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
    Implementation of composite spatial collision checker evaluating paths against obstacle zones.
'''

from __future__ import annotations

from scaralang.core.model.kinematics.pose.point_2d import Point2D
from scaralang.core.model.trajectory.obstacle.box import BoxObstacle
from scaralang.core.model.trajectory.obstacle.circle import CircleObstacle
from scaralang.core.model.trajectory.obstacle.shape import ObstacleShape
from scaralang.core.model.trajectory.obstacle.zone import ObstacleZone
from scaralang.core.service.trajectory.avoidance.collision.ibox_checker import IBoxCollisionChecker
from scaralang.core.service.trajectory.avoidance.collision.icircle_checker import ICircleCollisionChecker

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class SpatialCollisionChecker:
    '''
        Evaluates Cartesian points and linear segments against declared obstacle zones.

        It defines:

            :attributes:
                | _box_checker - Injected rectangular obstacle collision detector.
                | _circle_checker - Injected circular obstacle collision detector.
            :methods:
                | __init__ - Initializes SpatialCollisionChecker with injected checkers.
                | is_point_colliding - Identifies obstacle zones containing a point.
                | is_segment_colliding - Identifies obstacle zones intersected by a motion segment.
                | get_version - Gets implementation version string.
    '''

    def __init__(
        self,
        box_checker: IBoxCollisionChecker,
        circle_checker: ICircleCollisionChecker,
    ) -> None:
        '''
            Initializes SpatialCollisionChecker with injected shape checkers.

            :param box_checker: Injected rectangular collision checker.
            :param circle_checker: Injected circular collision checker.
        '''
        self._box_checker: IBoxCollisionChecker = box_checker
        self._circle_checker: ICircleCollisionChecker = circle_checker

    def is_point_colliding(
        self,
        *,
        point: Point2D,
        zones: tuple[ObstacleZone, ...],
    ) -> tuple[ObstacleZone, ...]:
        '''
            Identifies all obstacle zones containing a given 2D Cartesian point.

            :param point: Point2D Cartesian position.
            :param zones: Registered obstacle zones tuple.
            :return: Tuple of colliding ObstacleZone instances.
            :exceptions: None.
        '''
        colliding: list[ObstacleZone] = []

        for zone in zones:
            match zone.shape:
                case ObstacleShape.BOX:
                    if isinstance(zone.geometry, BoxObstacle) and self._box_checker.is_point_inside(
                        point=point, box=zone.geometry
                    ):
                        colliding.append(zone)
                case ObstacleShape.CIRCLE:
                    if isinstance(zone.geometry, CircleObstacle) and self._circle_checker.is_point_inside(
                        point=point, circle=zone.geometry
                    ):
                        colliding.append(zone)

        return tuple(colliding)

    def is_segment_colliding(
        self,
        *,
        start: Point2D,
        end: Point2D,
        zones: tuple[ObstacleZone, ...],
    ) -> tuple[ObstacleZone, ...]:
        '''
            Identifies all obstacle zones intersected by a 2D linear motion path segment.

            :param start: Starting Cartesian coordinate of motion path segment.
            :param end: Ending Cartesian coordinate of motion path segment.
            :param zones: Registered obstacle zones tuple.
            :return: Tuple of colliding ObstacleZone instances.
            :exceptions: None.
        '''
        colliding: list[ObstacleZone] = []

        for zone in zones:
            match zone.shape:
                case ObstacleShape.BOX:
                    if isinstance(zone.geometry, BoxObstacle) and self._box_checker.is_segment_colliding(
                        start=start, end=end, box=zone.geometry
                    ):
                        colliding.append(zone)
                case ObstacleShape.CIRCLE:
                    if isinstance(zone.geometry, CircleObstacle) and self._circle_checker.is_segment_colliding(
                        start=start, end=end, circle=zone.geometry
                    ):
                        colliding.append(zone)

        return tuple(colliding)

    def get_version(self) -> str:
        '''
            Gets implementation version string.

            :return: Version string.
            :exceptions: None.
        '''
        return __version__
