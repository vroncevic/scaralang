# -*- coding: UTF-8 -*-

'''
Module
    zone_test.py
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
    Unit tests for ObstacleZone data model.
'''

from __future__ import annotations

from dataclasses import FrozenInstanceError
from unittest import TestCase, main

from scaralang.core.model.kinematics.pose.point_2d import Point2D
from scaralang.core.model.trajectory.obstacle.box import BoxObstacle
from scaralang.core.model.trajectory.obstacle.circle import CircleObstacle
from scaralang.core.model.trajectory.obstacle.shape import ObstacleShape
from scaralang.core.model.trajectory.obstacle.zone import ObstacleZone

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ObstacleZoneTest(TestCase):
    '''Unit tests validating ObstacleZone binding, properties, and immutability.'''

    def test_box_zone_instantiation(self) -> None:
        '''
            Verifies box zone configuration.

            :exceptions: None.
        '''
        box = BoxObstacle(x_min=50.0, x_max=90.0, y_min=-70.0, y_max=-30.0)
        zone = ObstacleZone(
            name='CAMERA_STAND',
            shape=ObstacleShape.BOX,
            geometry=box,
        )
        self.assertEqual(zone.name, 'CAMERA_STAND')
        self.assertEqual(zone.shape, ObstacleShape.BOX)
        self.assertIs(zone.geometry, box)

    def test_circle_zone_instantiation(self) -> None:
        '''
            Verifies circle zone configuration.

            :exceptions: None.
        '''
        circle = CircleObstacle(center=Point2D(x=140.0, y=20.0), radius=25.0)
        zone = ObstacleZone(
            name='POST_OBSTACLE',
            shape=ObstacleShape.CIRCLE,
            geometry=circle,
        )
        self.assertEqual(zone.name, 'POST_OBSTACLE')
        self.assertEqual(zone.shape, ObstacleShape.CIRCLE)
        self.assertIs(zone.geometry, circle)

    def test_immutability(self) -> None:
        '''
            Verifies frozen instance raises FrozenInstanceError.

            :exceptions: None.
        '''
        box = BoxObstacle(x_min=0.0, x_max=10.0, y_min=0.0, y_max=10.0)
        zone = ObstacleZone(
            name='ZONE_A',
            shape=ObstacleShape.BOX,
            geometry=box,
        )
        with self.assertRaises(FrozenInstanceError):
            setattr(zone, 'name', 'ZONE_B')


if __name__ == '__main__':
    main()
