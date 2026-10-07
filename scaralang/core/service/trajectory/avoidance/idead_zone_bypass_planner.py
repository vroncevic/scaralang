# -*- coding: UTF-8 -*-

'''
Module
    idead_zone_bypass_planner.py
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
    Defines structural protocol IDeadZoneBypassPlanner for obstacle detour routing.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from scaralang.core.model.kinematics.point_2d import Point2D
from scaralang.core.model.trajectory.waypoint import Waypoint

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.7'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IDeadZoneBypassPlanner(Protocol):
    '''
        Structural protocol defining obstacle bypass detour trajectory generation.

        It defines:

            :methods:
                | plan_bypass - Computes collision-free detour waypoints around dead zone.
                | get_safe_radius - Returns safe avoidance circle radius in mm.
                | get_version - Returns planner component version string.
    '''

    def plan_bypass(
        self,
        start_pt: Point2D,
        end_pt: Point2D,
        *,
        z: float,
        speed: float,
    ) -> list[Waypoint]:
        '''
            Computes a collision-free bypass trajectory sequence around the central dead zone.

            :param start_pt: Start coordinate Point2D in mm.
            :param end_pt: Target destination coordinate Point2D in mm.
            :param z: Z vertical height coordinate in mm.
            :param speed: Feedrate speed in mm/s.
            :return: Ordered list of intermediate detour Waypoints to destination.
            :exceptions: None.
        '''

    def get_safe_radius(self) -> float:
        '''
            Returns the safe radial clearance boundary distance in mm.

            :return: Safe avoidance radius in mm.
            :exceptions: None.
        '''

    def get_version(self) -> str:
        '''
            Returns planner component version string representation.

            :return: Version string representation.
            :exceptions: None.
        '''
