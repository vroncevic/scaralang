# -*- coding: UTF-8 -*-

'''
Module
    idead_zone_validator.py
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
    Defines structural protocol IDeadZoneValidator for manipulator dead zone checking.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from scaralang.core.model.kinematics.point_2d import Point2D

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.7'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IDeadZoneValidator(Protocol):
    '''
        Structural protocol defining boundary validation against central dead zone.

        It defines:

            :methods:
                | is_point_in_dead_zone - Checks if coordinates fall inside the dead zone.
                | is_segment_crossing_dead_zone - Checks if line segment traverses dead zone.
                | get_dead_zone_radius - Returns active dead zone radial threshold in mm.
                | get_version - Returns validator component version string.
    '''

    def is_point_in_dead_zone(self, x: float, y: float) -> bool:
        '''
            Determines whether the given 2D coordinates reside inside the dead zone.

            :param x: Cartesian X coordinate in mm.
            :param y: Cartesian Y coordinate in mm.
            :return: True if inside the dead zone, False otherwise.
            :exceptions: None.
        '''

    def is_segment_crossing_dead_zone(self, p1: Point2D, p2: Point2D) -> bool:
        '''
            Determines whether the linear segment between p1 and p2 traverses the dead zone.

            :param p1: Start coordinate Point2D in mm.
            :param p2: End coordinate Point2D in mm.
            :return: True if the segment traverses the dead zone, False otherwise.
            :exceptions: None.
        '''

    def get_dead_zone_radius(self) -> float:
        '''
            Returns the active mechanical dead zone radial threshold in mm.

            :return: Dead zone radius in mm.
            :exceptions: None.
        '''

    def get_version(self) -> str:
        '''
            Returns validator component version string representation.

            :return: Version string representation.
            :exceptions: None.
        '''
