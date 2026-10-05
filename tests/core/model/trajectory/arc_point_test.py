# -*- coding: UTF-8 -*-

'''
Module
    arc_point_test.py
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
    Unit tests for pure data model ArcPoint.
'''

from __future__ import annotations

from dataclasses import FrozenInstanceError
from unittest import TestCase, main

from scaralang.core.model.kinematics.point_2d import Point2D
from scaralang.core.model.trajectory.arc_point import ArcPoint

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.5'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestArcPoint(TestCase):
    '''Unit tests validating ArcPoint initialization, slots, and immutability.'''

    def test_instantiation(self) -> None:
        '''Verify field values on initialization.'''
        pt = ArcPoint(
            point=Point2D(x=120.5, y=-85.25),
            heading_deg=45.0,
        )
        self.assertEqual(pt.point.x, 120.5)
        self.assertEqual(pt.point.y, -85.25)
        self.assertEqual(pt.heading_deg, 45.0)

    def test_immutability(self) -> None:
        '''Verify frozen dataclass prevents mutation.'''
        pt = ArcPoint(
            point=Point2D(x=0.0, y=0.0),
            heading_deg=0.0,
        )
        with self.assertRaises(FrozenInstanceError):
            pt.point = Point2D(x=10.0, y=10.0)

    def test_equality(self) -> None:
        '''Verify value-object equality semantics.'''
        pt1 = ArcPoint(
            point=Point2D(x=10.0, y=20.0),
            heading_deg=30.0,
        )
        pt2 = ArcPoint(
            point=Point2D(x=10.0, y=20.0),
            heading_deg=30.0,
        )
        pt3 = ArcPoint(
            point=Point2D(x=10.0, y=20.0),
            heading_deg=35.0,
        )
        self.assertEqual(pt1, pt2)
        self.assertNotEqual(pt1, pt3)


if __name__ == '__main__':
    main()
