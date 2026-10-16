# -*- coding: UTF-8 -*-

'''
Module
    itangent_heading_calculator.py
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
    Defines structural runtime-checkable protocol ITangentHeadingCalculator.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from scaralang.core.model.kinematics.point_2d import Point2D

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.9'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class ITangentHeadingCalculator(Protocol):
    '''
        Structural protocol defining tangent heading calculation contract.

        It defines:

            :methods:
                | calculate_tangent_angle - Calculates orientation angle between two points.
                | get_version - Gets implementation version string.
    '''

    def calculate_tangent_angle(
        self,
        *,
        source: Point2D,
        target: Point2D,
        fallback_phi: float,
    ) -> float:
        '''
            Calculates tangent heading angle from source point to target point.

            :param source: Current Cartesian coordinate point.
            :param target: Target Cartesian coordinate point.
            :param fallback_phi: Heading angle to retain if movement is negligible.
            :return: Computed heading angle in degrees in [-180, 180].
        '''

    def get_version(self) -> str:
        '''
            Gets implementation version string.

            :return: Version string.
        '''
