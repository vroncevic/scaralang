# -*- coding: UTF-8 -*-

'''
Module
    shape_discretizer_test.py
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
    Unit tests for ShapeDiscretizer service.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.model.exceptions.scara_kinematics_error import ScaraKinematicsError
from scaralang.core.model.kinematics.point_2d import Point2D
from scaralang.core.model.trajectory.circle_geometry import CircleGeometry
from scaralang.core.service.trajectory.discretization.ishape_discretizer import IShapeDiscretizer
from scaralang.core.service.trajectory.discretization.shape_discretizer_factory import ShapeDiscretizerFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestShapeDiscretizer(TestCase):
    '''
        Unit tests validating geometric contour discretization.

        It defines:

            :methods:
                | setUp - Instantiates ShapeDiscretizer via factory.
                | test_discretize_line - Verifies linear segment discretization.
                | test_discretize_circle - Verifies circular boundary discretization.
                | test_discretize_rectangle - Verifies rectangular boundary discretization.
                | test_name_property - Verifies name property returns expected identifier.
                | test_discretize_circle_invalid_steps - Verifies error on non-positive steps.
                | test_discretize_circle_invalid_radius - Verifies error on non-positive radius.
    '''

    def setUp(self) -> None:
        '''Instantiate ShapeDiscretizer via factory.'''
        self.discretizer: IShapeDiscretizer = ShapeDiscretizerFactory.create()

    def test_discretize_line(self) -> None:
        '''Verify linear segment discretization.'''
        pts = self.discretizer.discretize_line(
            Point2D(x=0.0, y=0.0),
            Point2D(x=100.0, y=100.0),
            z=10.0,
            speed=50.0,
        )
        self.assertEqual(len(pts), 2)
        self.assertEqual(pts[0].x, 0.0)
        self.assertEqual(pts[1].x, 100.0)
        self.assertEqual(pts[0].z, 10.0)
        self.assertEqual(pts[0].speed, 50.0)

    def test_discretize_circle(self) -> None:
        '''Verify circle boundary discretization.'''
        geom = CircleGeometry(
            center=Point2D(x=50.0, y=50.0),
            radius=20.0,
            steps=8,
            z=5.0,
            speed=30.0,
        )
        pts = self.discretizer.discretize_circle(geometry=geom)
        self.assertEqual(len(pts), 9)
        self.assertAlmostEqual(pts[0].x, 70.0)
        self.assertAlmostEqual(pts[0].y, 50.0)
        self.assertEqual(pts[0].z, 5.0)

    def test_discretize_rectangle(self) -> None:
        '''Verify rectangular boundary discretization.'''
        pts = self.discretizer.discretize_rectangle(
            Point2D(x=0.0, y=0.0),
            Point2D(x=80.0, y=40.0),
            z=12.0,
            speed=45.0,
        )
        self.assertEqual(len(pts), 5)
        self.assertEqual(pts[0].x, 0.0)
        self.assertEqual(pts[0].y, 0.0)
        self.assertEqual(pts[1].x, 80.0)
        self.assertEqual(pts[1].y, 0.0)
        self.assertEqual(pts[2].x, 80.0)
        self.assertEqual(pts[2].y, 40.0)
        self.assertEqual(pts[3].x, 0.0)
        self.assertEqual(pts[3].y, 40.0)
        self.assertEqual(pts[4].x, 0.0)
        self.assertEqual(pts[4].y, 0.0)

    def test_name_property(self) -> None:
        '''Verify name property returns correct identifier.'''
        self.assertEqual(self.discretizer.name, 'shape_discretizer')

    def test_discretize_circle_invalid_steps(self) -> None:
        '''Verify ScaraKinematicsError on non-positive steps.'''
        geom = CircleGeometry(
            center=Point2D(x=50.0, y=50.0),
            radius=20.0,
            steps=0,
            z=5.0,
            speed=30.0,
        )
        with self.assertRaises(ScaraKinematicsError):
            self.discretizer.discretize_circle(geometry=geom)

    def test_discretize_circle_invalid_radius(self) -> None:
        '''Verify ScaraKinematicsError on non-positive radius.'''
        geom = CircleGeometry(
            center=Point2D(x=50.0, y=50.0),
            radius=-5.0,
            steps=8,
            z=5.0,
            speed=30.0,
        )
        with self.assertRaises(ScaraKinematicsError):
            self.discretizer.discretize_circle(geometry=geom)


if __name__ == '__main__':
    main()
