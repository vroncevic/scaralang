# -*- coding: UTF-8 -*-

'''
Module
    bottleneck_incident.py
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
    Defines immutable BottleneckIncident model identifying motion performance bottlenecks.
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


@dataclass(slots=True, frozen=True, kw_only=True)
class BottleneckIncident:
    '''
        Immutable data model recording an axis bottleneck constraining cycle time.

        It defines:

            :attributes:
                | step_index - Sequence index of the constrained trajectory step.
                | limiting_axis - Axis name that dictated the segment duration.
                | constraint_type - Constraint category ('VELOCITY' or 'ACCELERATION').
                | duration_us - Allocated duration for the segment in microseconds.
    '''

    step_index: int
    limiting_axis: str
    constraint_type: str
    duration_us: int
