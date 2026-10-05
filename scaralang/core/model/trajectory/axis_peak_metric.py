# -*- coding: UTF-8 -*-

'''
Module
    axis_peak_metric.py
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
    Defines immutable AxisPeakMetric model representing peak velocity and acceleration for a joint axis.
'''

from __future__ import annotations

from dataclasses import dataclass

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.5'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(slots=True, frozen=True, kw_only=True)
class AxisPeakMetric:
    '''
        Immutable data model recording kinematic peak values for a single robot axis.

        It defines:

            :attributes:
                | axis_name - Joint axis identifier (e.g. 'J1', 'J2', 'Z', 'J4').
                | peak_velocity - Maximum observed velocity in physical units (rad/s or mm/s).
                | peak_acceleration - Maximum observed acceleration in physical units.
                | peak_steps - Maximum total displacement in motor microsteps.
    '''

    axis_name: str
    peak_velocity: float
    peak_acceleration: float
    peak_steps: int
