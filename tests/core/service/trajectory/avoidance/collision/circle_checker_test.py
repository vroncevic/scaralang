# -*- coding: UTF-8 -*-

'''
Module
    circle_checker_test.py
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
    Unit tests for CircleCollisionChecker implementation.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.model.kinematics.pose.point_2d import Point2D
from scaralang.core.model.trajectory.obstacle.circle import CircleObstacle
from scaralang.core.service.trajectory.avoidance.collision.circle_checker import CircleCollisionChecker

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestCircleCollisionChecker(TestCase):
    '''
        Test cases verifying CircleCollisionChecker point and segment collision detection.

        It defines:

            :methods:
                | setUp - Prepares CircleCollisionChecker test fixture.
                | test_point_inside - Verifies point containment inside circle.
                | test_point_outside - Verifies point outside circle returns False.
                | test_segment_through - Verifies segment crossing circle returns True.
                | test_segment_tangent - Verifies segment touching circle perimeter returns True.
                | test_segment_miss - Verifies segment missing circle returns False.
                | test_zero_length_inside - Verifies stationary point inside returns True.
                | test_zero_length_outside - Verifies stationary point outside returns False.
                | test_get_version - Verifies implementation version string.
    '''

    def setUp(self) -> None:
        '''
            Prepares CircleCollisionChecker test fixture.

            :exceptions: None.
        '''
        self._checker = CircleCollisionChecker()
        self._circle = CircleObstacle(center=Point2D(x=100.0, y=100.0), radius=20.0)

    def test_point_inside(self) -> None:
        '''
            Verifies point within circle radius returns True.

            :exceptions: None.
        '''
        pt = Point2D(x=105.0, y=105.0)
        self.assertTrue(self._checker.is_point_inside(point=pt, circle=self._circle))

    def test_point_outside(self) -> None:
        '''
            Verifies point beyond circle radius returns False.

            :exceptions: None.
        '''
        pt = Point2D(x=0.0, y=0.0)
        self.assertFalse(self._checker.is_point_inside(point=pt, circle=self._circle))

    def test_segment_through(self) -> None:
        '''
            Verifies segment passing through circle returns True.

            :exceptions: None.
        '''
        start = Point2D(x=50.0, y=100.0)
        end = Point2D(x=150.0, y=100.0)
        self.assertTrue(
            self._checker.is_segment_colliding(
                start=start, end=end, circle=self._circle
            )
        )

    def test_segment_tangent(self) -> None:
        '''
            Verifies segment touching tangent perimeter returns True.

            :exceptions: None.
        '''
        start = Point2D(x=50.0, y=120.0)
        end = Point2D(x=150.0, y=120.0)
        self.assertTrue(
            self._checker.is_segment_colliding(
                start=start, end=end, circle=self._circle
            )
        )

    def test_segment_miss(self) -> None:
        '''
            Verifies segment passing outside circle perimeter returns False.

            :exceptions: None.
        '''
        start = Point2D(x=50.0, y=150.0)
        end = Point2D(x=150.0, y=150.0)
        self.assertFalse(
            self._checker.is_segment_colliding(
                start=start, end=end, circle=self._circle
            )
        )

    def test_zero_length_inside(self) -> None:
        '''
            Verifies zero-length stationary segment inside circle returns True.

            :exceptions: None.
        '''
        start = Point2D(x=100.0, y=100.0)
        end = Point2D(x=100.0, y=100.0)
        self.assertTrue(
            self._checker.is_segment_colliding(
                start=start, end=end, circle=self._circle
            )
        )

    def test_zero_length_outside(self) -> None:
        '''
            Verifies zero-length stationary segment outside circle returns False.

            :exceptions: None.
        '''
        start = Point2D(x=0.0, y=0.0)
        end = Point2D(x=0.0, y=0.0)
        self.assertFalse(
            self._checker.is_segment_colliding(
                start=start, end=end, circle=self._circle
            )
        )

    def test_get_version(self) -> None:
        '''
            Verifies get_version returns implementation version string.

            :exceptions: None.
        '''
        self.assertEqual(self._checker.get_version(), __version__)


if __name__ == '__main__':
    main()
