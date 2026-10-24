# -*- coding: UTF-8 -*-

'''
Module
    spatial_checker_test.py
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
    Unit tests for SpatialCollisionChecker implementation.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.model.kinematics.pose.point_2d import Point2D
from scaralang.core.model.trajectory.obstacle.box import BoxObstacle
from scaralang.core.model.trajectory.obstacle.circle import CircleObstacle
from scaralang.core.model.trajectory.obstacle.shape import ObstacleShape
from scaralang.core.model.trajectory.obstacle.zone import ObstacleZone
from scaralang.core.service.trajectory.avoidance.collision.box_checker import BoxCollisionChecker
from scaralang.core.service.trajectory.avoidance.collision.circle_checker import CircleCollisionChecker
from scaralang.core.service.trajectory.avoidance.collision.spatial_checker import SpatialCollisionChecker

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestSpatialCollisionChecker(TestCase):
    '''
        Test cases verifying SpatialCollisionChecker path evaluation against obstacle zones.

        It defines:

            :methods:
                | setUp - Prepares SpatialCollisionChecker and sample zones.
                | test_point_colliding_box - Verifies point colliding with box obstacle.
                | test_point_colliding_circle - Verifies point colliding with circle obstacle.
                | test_point_colliding_none - Verifies free point returns empty tuple.
                | test_segment_colliding_box - Verifies motion segment colliding with box.
                | test_segment_colliding_circle - Verifies motion segment colliding with circle.
                | test_segment_colliding_both - Verifies segment intersecting multiple obstacles.
                | test_segment_colliding_none - Verifies clear path returns empty tuple.
                | test_get_version - Verifies implementation version string.
    '''

    def setUp(self) -> None:
        '''
            Prepares SpatialCollisionChecker and sample obstacle zones.

            :exceptions: None.
        '''
        self._checker = SpatialCollisionChecker(
            box_checker=BoxCollisionChecker(),
            circle_checker=CircleCollisionChecker(),
        )
        self._box_zone = ObstacleZone(
            name='WORKCELL_WALL',
            shape=ObstacleShape.BOX,
            geometry=BoxObstacle(x_min=10.0, x_max=50.0, y_min=-20.0, y_max=30.0),
        )
        self._circle_zone = ObstacleZone(
            name='POST',
            shape=ObstacleShape.CIRCLE,
            geometry=CircleObstacle(center=Point2D(x=120.0, y=40.0), radius=25.0),
        )
        self._zones = (self._box_zone, self._circle_zone)

    def test_point_colliding_box(self) -> None:
        '''
            Verifies point inside box obstacle returns that zone in tuple.

            :exceptions: None.
        '''
        pt = Point2D(x=20.0, y=0.0)
        colliding = self._checker.is_point_colliding(point=pt, zones=self._zones)
        self.assertEqual(len(colliding), 1)
        self.assertEqual(colliding[0].name, 'WORKCELL_WALL')

    def test_point_colliding_circle(self) -> None:
        '''
            Verifies point inside circle obstacle returns that zone in tuple.

            :exceptions: None.
        '''
        pt = Point2D(x=125.0, y=45.0)
        colliding = self._checker.is_point_colliding(point=pt, zones=self._zones)
        self.assertEqual(len(colliding), 1)
        self.assertEqual(colliding[0].name, 'POST')

    def test_point_colliding_none(self) -> None:
        '''
            Verifies uninhibited point returns empty tuple.

            :exceptions: None.
        '''
        pt = Point2D(x=0.0, y=0.0)
        colliding = self._checker.is_point_colliding(point=pt, zones=self._zones)
        self.assertEqual(colliding, ())

    def test_segment_colliding_box(self) -> None:
        '''
            Verifies segment piercing box obstacle returns that zone in tuple.

            :exceptions: None.
        '''
        start = Point2D(x=0.0, y=0.0)
        end = Point2D(x=60.0, y=0.0)
        colliding = self._checker.is_segment_colliding(
            start=start, end=end, zones=self._zones
        )
        self.assertEqual(len(colliding), 1)
        self.assertEqual(colliding[0].name, 'WORKCELL_WALL')

    def test_segment_colliding_circle(self) -> None:
        '''
            Verifies segment intersecting circle returns that zone in tuple.

            :exceptions: None.
        '''
        start = Point2D(x=100.0, y=40.0)
        end = Point2D(x=150.0, y=40.0)
        colliding = self._checker.is_segment_colliding(
            start=start, end=end, zones=self._zones
        )
        self.assertEqual(len(colliding), 1)
        self.assertEqual(colliding[0].name, 'POST')

    def test_segment_colliding_both(self) -> None:
        '''
            Verifies long segment intersecting both obstacles returns both in tuple.

            :exceptions: None.
        '''
        start = Point2D(x=20.0, y=0.0)
        end = Point2D(x=120.0, y=40.0)
        colliding = self._checker.is_segment_colliding(
            start=start, end=end, zones=self._zones
        )
        self.assertEqual(len(colliding), 2)

    def test_segment_colliding_none(self) -> None:
        '''
            Verifies clear motion path returns empty tuple.

            :exceptions: None.
        '''
        start = Point2D(x=0.0, y=100.0)
        end = Point2D(x=200.0, y=100.0)
        colliding = self._checker.is_segment_colliding(
            start=start, end=end, zones=self._zones
        )
        self.assertEqual(colliding, ())

    def test_get_version(self) -> None:
        '''
            Verifies get_version returns implementation version string.

            :exceptions: None.
        '''
        self.assertEqual(self._checker.get_version(), __version__)


if __name__ == '__main__':
    main()
