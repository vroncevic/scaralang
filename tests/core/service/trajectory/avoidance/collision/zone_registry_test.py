# -*- coding: UTF-8 -*-

'''
Module
    zone_registry_test.py
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
    Unit tests for ZoneRegistry implementation.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.model.exceptions.semantic import ScaraSemanticError
from scaralang.core.model.kinematics.pose.point_2d import Point2D
from scaralang.core.model.trajectory.obstacle.box import BoxObstacle
from scaralang.core.model.trajectory.obstacle.circle import CircleObstacle
from scaralang.core.model.trajectory.obstacle.shape import ObstacleShape
from scaralang.core.model.trajectory.obstacle.zone import ObstacleZone
from scaralang.core.service.trajectory.avoidance.collision.zone_registry import ZoneRegistry

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestZoneRegistry(TestCase):
    '''
        Test cases verifying ZoneRegistry storage and retrieval.

        It defines:

            :methods:
                | setUp - Prepares ZoneRegistry test fixture.
                | test_register_and_get_zone - Verifies registering and retrieving zone.
                | test_duplicate_registration - Verifies duplicate name raises semantic error.
                | test_get_nonexistent_zone - Verifies getting missing zone raises error.
                | test_get_all_zones - Verifies retrieving all registered zones tuple.
                | test_has_zone - Verifies checking zone existence.
                | test_get_version - Verifies implementation version string.
    '''

    def setUp(self) -> None:
        '''
            Prepares ZoneRegistry test fixture.

            :exceptions: None.
        '''
        self._registry = ZoneRegistry()
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

    def test_register_and_get_zone(self) -> None:
        '''
            Verifies successful registration and retrieval of obstacle zone.

            :exceptions: None.
        '''
        self._registry.register_zone(self._box_zone)
        retrieved: ObstacleZone = self._registry.get_zone('WORKCELL_WALL')
        self.assertEqual(retrieved.name, 'WORKCELL_WALL')
        self.assertEqual(retrieved.shape, ObstacleShape.BOX)

    def test_duplicate_registration(self) -> None:
        '''
            Verifies duplicate zone registration raises ScaraSemanticError.

            :exceptions: None.
        '''
        self._registry.register_zone(self._box_zone)
        with self.assertRaises(ScaraSemanticError):
            self._registry.register_zone(self._box_zone)

    def test_get_nonexistent_zone(self) -> None:
        '''
            Verifies retrieving missing zone raises ScaraSemanticError.

            :exceptions: None.
        '''
        with self.assertRaises(ScaraSemanticError):
            self._registry.get_zone('UNKNOWN')

    def test_get_all_zones(self) -> None:
        '''
            Verifies retrieving all registered obstacle zones tuple.

            :exceptions: None.
        '''
        self.assertEqual(self._registry.get_all_zones(), ())
        self._registry.register_zone(self._box_zone)
        self._registry.register_zone(self._circle_zone)
        all_zones = self._registry.get_all_zones()
        self.assertEqual(len(all_zones), 2)

    def test_has_zone(self) -> None:
        '''
            Verifies checking zone existence by name.

            :exceptions: None.
        '''
        self.assertFalse(self._registry.has_zone('WORKCELL_WALL'))
        self._registry.register_zone(self._box_zone)
        self.assertTrue(self._registry.has_zone('WORKCELL_WALL'))

    def test_get_version(self) -> None:
        '''
            Verifies get_version returns implementation version string.

            :exceptions: None.
        '''
        self.assertEqual(self._registry.get_version(), __version__)


if __name__ == '__main__':
    main()
