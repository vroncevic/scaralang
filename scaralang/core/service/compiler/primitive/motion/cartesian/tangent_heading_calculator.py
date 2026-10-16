# -*- coding: UTF-8 -*-

'''
Module
    tangent_heading_calculator.py
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
    Concrete implementation of tangent heading angle calculation.
'''

from __future__ import annotations

from math import atan2, degrees, hypot
from typing import ClassVar

from scaralang.core.model.kinematics.point_2d import Point2D

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.9'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TangentHeadingCalculator:
    '''
        Computes tangent heading orientation angle between consecutive points.

        It defines:

            :attributes:
                | MIN_DISPLACEMENT - Minimum displacement threshold to recalculate heading angle.
            :methods:
                | calculate_tangent_angle - Calculates orientation angle in degrees.
                | get_version - Gets implementation version string.
    '''

    MIN_DISPLACEMENT: ClassVar[float] = 1e-4

    def calculate_tangent_angle(
        self,
        *,
        source: Point2D,
        target: Point2D,
        fallback_phi: float,
    ) -> float:
        '''
            Calculates tangent heading angle from source to target point.

            :param source: Current Cartesian coordinate point.
            :param target: Target Cartesian coordinate point.
            :param fallback_phi: Heading angle to retain if movement is negligible.
            :return: Computed heading angle in degrees in [-180, 180].
            :exceptions: None.
        '''
        delta_x: float = target.x - source.x
        delta_y: float = target.y - source.y

        if hypot(delta_x, delta_y) < self.MIN_DISPLACEMENT:
            return fallback_phi

        return degrees(atan2(delta_y, delta_x))

    def get_version(self) -> str:
        '''
            Gets implementation version string.

            :return: Version string.
            :exceptions: None.
        '''
        return __version__
