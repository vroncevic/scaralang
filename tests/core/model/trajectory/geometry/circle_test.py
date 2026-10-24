# -*- coding: UTF-8 -*-

'''
Module
    circle_test.py
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

from dataclasses import FrozenInstanceError
from unittest import TestCase, main

from scaralang.core.model.kinematics.pose.point_2d import Point2D
from scaralang.core.model.trajectory.geometry.circle import CircleGeometry

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class CircleGeometryTest(TestCase):
    '''Unit tests validating CircleGeometry initialization and immutability.'''

    def test_instantiation_and_attributes(self) -> None:
        '''
            Verify proper initialization and access of CircleGeometry fields.

            :exceptions: None.
        '''
        circle = CircleGeometry(
            center=Point2D(x=100.0, y=100.0),
            radius=50.0,
            steps=36,
            z=10.0,
            speed=20.0
        )
        self.assertEqual(circle.center, Point2D(x=100.0, y=100.0))
        self.assertEqual(circle.radius, 50.0)
        self.assertEqual(circle.steps, 36)
        self.assertEqual(circle.z, 10.0)
        self.assertEqual(circle.speed, 20.0)

    def test_immutability(self) -> None:
        '''
            Verify that modifying attributes raises FrozenInstanceError.

            :exceptions: None.
        '''
        circle = CircleGeometry(
            center=Point2D(x=0.0, y=0.0),
            radius=10.0,
            steps=10,
            z=0.0,
            speed=1.0
        )
        with self.assertRaises(FrozenInstanceError):
            setattr(circle, 'radius', 20.0)


if __name__ == '__main__':
    main()
