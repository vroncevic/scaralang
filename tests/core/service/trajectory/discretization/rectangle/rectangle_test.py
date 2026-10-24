# -*- coding: UTF-8 -*-

'''
Module
    rectangle_test.py
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
    Unit tests for RectangleDiscretizer service.
'''

from __future__ import annotations

from unittest import TestCase, main

from scaralang.core.model.kinematics.pose.point_2d import Point2D
from scaralang.core.service.trajectory.discretization.rectangle.rectangle import RectangleDiscretizer

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestRectangleDiscretizer(TestCase):
    '''
        Unit tests validating rectangular boundary discretization.

        It defines:

            :methods:
                | setUp - Instantiates RectangleDiscretizer instance.
                | test_discretize - Verifies rectangular boundary discretization.
                | test_name_property - Verifies name property returns expected identifier.
    '''

    def setUp(self) -> None:
        '''
            Instantiate RectangleDiscretizer instance.

            :exceptions: None.
        '''
        self.discretizer = RectangleDiscretizer()

    def test_discretize(self) -> None:
        '''
            Verify rectangular boundary discretization.

            :exceptions: None.
        '''
        pts = self.discretizer.discretize(
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
        self.assertEqual(pts[0].z, 12.0)
        self.assertEqual(pts[0].speed, 45.0)

    def test_name_property(self) -> None:
        '''
            Verify name property returns correct identifier.

            :exceptions: None.
        '''
        self.assertEqual(self.discretizer.name, 'rectangle_discretizer')


if __name__ == '__main__':
    main()
