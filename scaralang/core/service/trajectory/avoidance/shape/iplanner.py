# -*- coding: UTF-8 -*-

'''
Module
    iplanner.py
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
    Defines structural protocol IAvoidanceShapePlanner for obstacle detour routing.
'''

from __future__ import annotations

from collections.abc import Sequence
from typing import Protocol, runtime_checkable

from scaralang.core.model.kinematics.point_2d import Point2D
from scaralang.core.model.trajectory.waypoint import Waypoint

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.9'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IAvoidanceShapePlanner(Protocol):
    '''
        Structural protocol defining shape contour planning with obstacle detour routing.

        It defines:

            :methods:
                | plan_contour - Plans geometric contour with dead zone avoidance detours.
                | get_version - Returns planner component version string.
    '''

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

    def get_version(self) -> str:
        '''
            Returns planner component version string representation.

            :return: Semantic version string.
            :exceptions: None.
        '''
