# -*- coding: UTF-8 -*-

'''
Module
    arc_geometry.py
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
    Defines ArcGeometry immutable data model representing circular arc interpolation parameters.
'''

from __future__ import annotations

from dataclasses import dataclass

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(slots=True, frozen=True, kw_only=True)
class ArcGeometry:
    '''
        Geometric description of a circular arc for discretization into linear waypoints.

        It defines:

            :attributes:
                | start_x - Starting arc X Cartesian coordinate.
                | start_y - Starting arc Y Cartesian coordinate.
                | target_x - Destination arc X Cartesian coordinate.
                | target_y - Destination arc Y Cartesian coordinate.
                | offset_i - Arc center X offset relative to start position.
                | offset_j - Arc center Y offset relative to start position.
                | is_clockwise - True for clockwise arc (ARC_CW), False for counter-clockwise.
                | step_angle_deg - Angular discretization step size in degrees.
    '''

    start_x: float
    start_y: float
    target_x: float
    target_y: float
    offset_i: float
    offset_j: float
    is_clockwise: bool
    step_angle_deg: float = 5.0
