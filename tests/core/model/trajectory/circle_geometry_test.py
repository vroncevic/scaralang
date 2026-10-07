# -*- coding: UTF-8 -*-

'''
Module
    circle_geometry_test.py
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
    Unit tests for pure data structure CircleGeometry.
'''

from __future__ import annotations

from unittest import TestCase, main

from scaralang.core.model.kinematics.point_2d import Point2D
from scaralang.core.model.trajectory.circle_geometry import CircleGeometry

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.7'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestCircleGeometry(TestCase):
    '''Unit tests validating CircleGeometry initialization and immutability.'''

    def test_instantiation_defaults(self) -> None:
        '''Verify default parameters on initialization.'''
        geom = CircleGeometry(
            center=Point2D(x=100.0, y=50.0),
            radius=25.0,
            steps=36,
        )
        self.assertEqual(geom.center, Point2D(x=100.0, y=50.0))
        self.assertEqual(geom.radius, 25.0)
        self.assertEqual(geom.steps, 36)
        self.assertEqual(geom.z, 0.0)
        self.assertEqual(geom.speed, 40.0)

    def test_instantiation_custom(self) -> None:
        '''Verify custom parameters on initialization.'''
        geom = CircleGeometry(
            center=Point2D(x=0.0, y=0.0),
            radius=10.0,
            steps=18,
            z=15.0,
            speed=80.0,
        )
        self.assertEqual(geom.center, Point2D(x=0.0, y=0.0))
        self.assertEqual(geom.z, 15.0)
        self.assertEqual(geom.speed, 80.0)


if __name__ == '__main__':
    main()
