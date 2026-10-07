# -*- coding: UTF-8 -*-

'''
Module
    dead_zone_validator.py
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
    Implementation of dead zone boundary and line segment traversal validator.
'''

from __future__ import annotations

from math import hypot
from typing import Final

from scaralang.core.model.kinematics.point_2d import Point2D

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.7'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DeadZoneValidator:
    '''
        Validates Cartesian coordinates and linear path segments against dead zone limits.

        It defines:

            :attributes:
                | _dead_zone_radius - Mechanical inner singularity dead zone radius in mm.
            :methods:
                | __init__ - Initializes validator with dead zone radial threshold.
                | is_point_in_dead_zone - Checks if coordinates fall inside the dead zone.
                | is_segment_crossing_dead_zone - Checks if line segment traverses dead zone.
                | get_dead_zone_radius - Returns active dead zone radius in mm.
                | get_version - Returns validator component version string.
    '''

    _dead_zone_radius: float

    def __init__(self, dead_zone_radius: float) -> None:
        '''
            Initializes dead zone validator with mechanical radial threshold.

            :param dead_zone_radius: Mechanical inner dead zone radius in mm.
            :exceptions: None.
        '''
        self._dead_zone_radius: Final[float] = max(0.0, dead_zone_radius)

    def is_point_in_dead_zone(self, x: float, y: float) -> bool:
        '''
            Determines whether the given 2D coordinates reside inside the dead zone.

            :param x: Cartesian X coordinate in mm.
            :param y: Cartesian Y coordinate in mm.
            :return: True if inside the dead zone, False otherwise.
            :exceptions: None.
        '''
        return hypot(x, y) < self._dead_zone_radius

    def is_segment_crossing_dead_zone(self, p1: Point2D, p2: Point2D) -> bool:
        '''
            Determines whether the linear segment between p1 and p2 traverses the dead zone.

            :param p1: Start coordinate Point2D in mm.
            :param p2: End coordinate Point2D in mm.
            :return: True if the segment traverses the dead zone, False otherwise.
            :exceptions: None.
        '''
        if self.is_point_in_dead_zone(p1.x, p1.y) or self.is_point_in_dead_zone(p2.x, p2.y):
            return True

        dx: float = p2.x - p1.x
        dy: float = p2.y - p1.y
        seg_len_sq: float = dx * dx + dy * dy

        if seg_len_sq < 1e-9:
            return False

        t: float = -(p1.x * dx + p1.y * dy) / seg_len_sq
        t_clamped: float = max(0.0, min(1.0, t))
        closest_x: float = p1.x + t_clamped * dx
        closest_y: float = p1.y + t_clamped * dy

        return hypot(closest_x, closest_y) < self._dead_zone_radius

    def get_dead_zone_radius(self) -> float:
        '''
            Returns the active mechanical dead zone radial threshold in mm.

            :return: Dead zone radius in mm.
            :exceptions: None.
        '''
        return self._dead_zone_radius

    def get_version(self) -> str:
        '''
            Returns validator component version string representation.

            :return: Version string representation.
            :exceptions: None.
        '''
        return __version__
