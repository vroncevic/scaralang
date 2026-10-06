# -*- coding: UTF-8 -*-

'''
Module
    work_frame_test.py
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
    Unit testing for WorkFrame domain model.
'''

from __future__ import annotations

from dataclasses import FrozenInstanceError
from unittest import TestCase, main

from scaralang.core.model.dsl.macro.work_frame import WorkFrame
from scaralang.core.model.kinematics.point_2d import Point2D

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.6'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class WorkFrameTest(TestCase):
    '''
        Validates WorkFrame fields and immutability.
    '''

    def test_explicit_origin_values(self) -> None:
        '''
            Verifies initialization of WorkFrame at global origin with zero rotation.
        '''
        frame = WorkFrame(origin=Point2D(x=0.0, y=0.0), angle_deg=0.0)
        self.assertEqual(frame.origin, Point2D(x=0.0, y=0.0))
        self.assertAlmostEqual(frame.origin.x, 0.0)
        self.assertAlmostEqual(frame.origin.y, 0.0)
        self.assertAlmostEqual(frame.angle_deg, 0.0)

    def test_equality(self) -> None:
        '''
            Verifies value equality and inequality between WorkFrame instances.
        '''
        f1 = WorkFrame(origin=Point2D(x=10.0, y=20.0), angle_deg=30.0)
        f2 = WorkFrame(origin=Point2D(x=10.0, y=20.0), angle_deg=30.0)
        f3 = WorkFrame(origin=Point2D(x=10.0, y=20.0), angle_deg=45.0)
        self.assertEqual(f1, f2)
        self.assertNotEqual(f1, f3)

    def test_custom_values(self) -> None:
        '''
            Verifies custom translation and orientation attributes.
        '''
        frame = WorkFrame(origin=Point2D(x=120.0, y=-45.0), angle_deg=30.0)
        self.assertEqual(frame.origin, Point2D(x=120.0, y=-45.0))
        self.assertAlmostEqual(frame.origin.x, 120.0)
        self.assertAlmostEqual(frame.origin.y, -45.0)
        self.assertAlmostEqual(frame.angle_deg, 30.0)

    def test_immutability(self) -> None:
        '''
            Verifies that WorkFrame instances cannot be modified after construction.
        '''
        frame = WorkFrame(origin=Point2D(x=10.0, y=20.0), angle_deg=30.0)
        with self.assertRaises(FrozenInstanceError):
            frame.origin = Point2D(x=99.0, y=0.0)


if __name__ == '__main__':
    main()
