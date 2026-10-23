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
    Unit tests for CircleDiscretizer service.
'''

from __future__ import annotations

from unittest import TestCase, main

from scaralang.core.model.exceptions.kinematics import ScaraKinematicsError
from scaralang.core.model.kinematics.pose.point_2d import Point2D
from scaralang.core.model.trajectory.geometry.circle import CircleGeometry
from scaralang.core.service.trajectory.discretization.circle.circle import CircleDiscretizer

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestCircleDiscretizer(TestCase):
    '''
        Unit tests validating circular boundary discretization.

        It defines:

            :methods:
                | setUp - Instantiates CircleDiscretizer instance.
                | test_discretize - Verifies circular boundary discretization.
                | test_name_property - Verifies name property returns expected identifier.
                | test_discretize_invalid_steps - Verifies error on non-positive steps.
                | test_discretize_invalid_radius - Verifies error on non-positive radius.
    '''

    def setUp(self) -> None:
        '''
            Instantiate CircleDiscretizer instance.

            :exceptions: None.
        '''
        self.discretizer = CircleDiscretizer()

    def test_discretize(self) -> None:
        '''
            Verify circular boundary discretization.

            :exceptions: None.
        '''
        geom = CircleGeometry(
            center=Point2D(x=50.0, y=50.0),
            radius=20.0,
            steps=8,
            z=5.0,
            speed=30.0,
        )
        pts = self.discretizer.discretize(geometry=geom)
        self.assertEqual(len(pts), 9)
        self.assertAlmostEqual(pts[0].x, 70.0)
        self.assertAlmostEqual(pts[0].y, 50.0)
        self.assertEqual(pts[0].z, 5.0)

    def test_name_property(self) -> None:
        '''
            Verify name property returns correct identifier.

            :exceptions: None.
        '''
        self.assertEqual(self.discretizer.name, 'circle_discretizer')

    def test_discretize_invalid_steps(self) -> None:
        '''
            Verify ScaraKinematicsError on non-positive steps.

            :exceptions: None.
        '''
        geom = CircleGeometry(
            center=Point2D(x=50.0, y=50.0),
            radius=20.0,
            steps=0,
            z=5.0,
            speed=30.0,
        )
        with self.assertRaises(ScaraKinematicsError):
            self.discretizer.discretize(geometry=geom)

    def test_discretize_invalid_radius(self) -> None:
        '''
            Verify ScaraKinematicsError on non-positive radius.

            :exceptions: None.
        '''
        geom = CircleGeometry(
            center=Point2D(x=50.0, y=50.0),
            radius=-5.0,
            steps=8,
            z=5.0,
            speed=30.0,
        )
        with self.assertRaises(ScaraKinematicsError):
            self.discretizer.discretize(geometry=geom)


if __name__ == '__main__':
    main()
