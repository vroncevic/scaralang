# -*- coding: UTF-8 -*-

'''
Module
    axis_peak_steps.py
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
    Defines immutable AxisPeakSteps model holding peak joint step metrics.
'''

from __future__ import annotations

from dataclasses import dataclass

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(frozen=True, slots=True, kw_only=True)
class AxisPeakSteps:
    '''
        Peak joint step metrics observed across compiled binary program execution.

        It defines:

            :attributes:
                | peak_j1_steps - Peak step count for joint 1 axis.
                | peak_j2_steps - Peak step count for joint 2 axis.
                | peak_z_steps - Peak step count for linear Z axis.
                | peak_j4_steps - Peak step count for wrist orientation axis.
    '''

    peak_j1_steps: int = 0
    peak_j2_steps: int = 0
    peak_z_steps: int = 0
    peak_j4_steps: int = 0
