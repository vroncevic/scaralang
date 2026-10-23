# -*- coding: UTF-8 -*-

'''
Module
    box_checker_test.py
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
    Unit tests for BoxCollisionChecker implementation.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.model.kinematics.pose.point_2d import Point2D
from scaralang.core.model.trajectory.obstacle.box import BoxObstacle
from scaralang.core.service.trajectory.avoidance.collision.box_checker import BoxCollisionChecker

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestBoxCollisionChecker(TestCase):
    '''
        Test cases verifying BoxCollisionChecker point and segment collision detection.

        It defines:

            :methods:
                | setUp - Prepares BoxCollisionChecker test fixture.
                | test_point_inside - Verifies point containment inside box.
                | test_point_outside - Verifies point outside box returns False.
                | test_segment_through - Verifies segment piercing through box returns True.
                | test_segment_inside - Verifies segment completely inside returns True.
                | test_segment_miss - Verifies segment clearly missing returns False.
                | test_segment_parallel_outside - Verifies parallel segment outside returns False.
                | test_get_version - Verifies implementation version string.
    '''

    def setUp(self) -> None:
        '''
            Prepares BoxCollisionChecker test fixture.

            :exceptions: None.
        '''
        self._checker = BoxCollisionChecker()
        self._box = BoxObstacle(x_min=10.0, x_max=50.0, y_min=-20.0, y_max=30.0)

    def test_point_inside(self) -> None:
        '''
            Verifies point within boundary coordinates returns True.

            :exceptions: None.
        '''
        pt = Point2D(x=20.0, y=5.0)
        self.assertTrue(self._checker.is_point_inside(point=pt, box=self._box))

    def test_point_outside(self) -> None:
        '''
            Verifies point outside boundary coordinates returns False.

            :exceptions: None.
        '''
        pt = Point2D(x=0.0, y=0.0)
        self.assertFalse(self._checker.is_point_inside(point=pt, box=self._box))

    def test_segment_through(self) -> None:
        '''
            Verifies motion segment crossing through box boundaries returns True.

            :exceptions: None.
        '''
        start = Point2D(x=0.0, y=5.0)
        end = Point2D(x=60.0, y=5.0)
        self.assertTrue(
            self._checker.is_segment_colliding(start=start, end=end, box=self._box)
        )

    def test_segment_inside(self) -> None:
        '''
            Verifies motion segment completely inside box returns True.

            :exceptions: None.
        '''
        start = Point2D(x=15.0, y=0.0)
        end = Point2D(x=25.0, y=0.0)
        self.assertTrue(
            self._checker.is_segment_colliding(start=start, end=end, box=self._box)
        )

    def test_segment_miss(self) -> None:
        '''
            Verifies motion segment passing beside box returns False.

            :exceptions: None.
        '''
        start = Point2D(x=0.0, y=50.0)
        end = Point2D(x=60.0, y=50.0)
        self.assertFalse(
            self._checker.is_segment_colliding(start=start, end=end, box=self._box)
        )

        start_short = Point2D(x=-20.0, y=0.0)
        end_short = Point2D(x=0.0, y=0.0)
        self.assertFalse(
            self._checker.is_segment_colliding(
                start=start_short, end=end_short, box=self._box
            )
        )

    def test_segment_parallel_outside(self) -> None:
        '''
            Verifies vertical segment parallel to box but outside returns False.

            :exceptions: None.
        '''
        start = Point2D(x=5.0, y=-50.0)
        end = Point2D(x=5.0, y=50.0)
        self.assertFalse(
            self._checker.is_segment_colliding(start=start, end=end, box=self._box)
        )

    def test_get_version(self) -> None:
        '''
            Verifies get_version returns implementation version string.

            :exceptions: None.
        '''
        self.assertEqual(self._checker.get_version(), __version__)


if __name__ == '__main__':
    main()
