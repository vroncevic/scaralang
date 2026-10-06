# -*- coding: UTF-8 -*-

'''
Module
    speed_limits.py
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
    Defines SpeedLimits domain value object for SCARA velocity and acceleration limits.
'''

from __future__ import annotations

from dataclasses import dataclass

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.6'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(frozen=True, slots=True, kw_only=True)
class SpeedLimits:
    '''
        Domain Value Object encapsulating feedrate velocity and acceleration boundaries.

        It defines:

            :attributes:
                | min_speed - Minimum feedrate speed limit in mm/s.
                | max_speed - Maximum feedrate speed limit in mm/s.
                | default_speed - Default Cartesian linear speed in mm/s.
                | default_accel - Default acceleration in mm/s^2.
                | max_accel - Maximum acceleration in mm/s^2.
    '''

    min_speed: float
    max_speed: float
    default_speed: float
    default_accel: float
    max_accel: float
