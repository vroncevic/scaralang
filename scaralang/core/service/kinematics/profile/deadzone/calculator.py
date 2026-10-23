# -*- coding: UTF-8 -*-

'''
Module
    calculator.py
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
    Service calculating physical robot reach deadzone radius.
'''

from __future__ import annotations

from math import cos, pi, sqrt

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DeadzoneCalculator:
    '''
        Calculates the physical minimum reach dead zone radius.

        It defines:

            :methods:
                | __init__ - Initializes calculator instance.
                | calculate_radius - Calculates minimum reach dead zone radius.
                | get_version - Returns calculator version string.
    '''

    def __init__(self) -> None:
        '''
            Initializes DeadzoneCalculator instance.

            :exceptions: None.
        '''

    def calculate_radius(
        self,
        *,
        l1: float,
        l2: float,
        j2_max_rad: float
    ) -> float:
        '''
            Calculates the physical minimum reach dead zone radius in millimeters.

            :param l1: Shoulder link length in mm.
            :param l2: Elbow link length in mm.
            :param j2_max_rad: Maximum elbow joint angle in radians.
            :return: Dead zone radius in mm.
            :exceptions: None.
        '''
        return max(
            abs(l1 - l2),
            sqrt(l1**2 + l2**2 - 2.0 * l1 * l2 * cos(pi - abs(j2_max_rad))),
        )

    def get_version(self) -> str:
        '''
            Returns the calculator version string.

            :return: Version string representation.
            :exceptions: None.
        '''
        return __version__
