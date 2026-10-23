# -*- coding: UTF-8 -*-

'''
Module
    provides_test.py
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
    Unit tests for CollisionProvides container.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.service.trajectory.avoidance.collision.box_checker import BoxCollisionChecker
from scaralang.core.service.trajectory.avoidance.collision.circle_checker import CircleCollisionChecker
from scaralang.core.service.trajectory.avoidance.collision.provides import CollisionProvides
from scaralang.core.service.trajectory.avoidance.collision.spatial_checker import SpatialCollisionChecker
from scaralang.core.service.trajectory.avoidance.collision.zone_registry import ZoneRegistry

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestCollisionProvides(TestCase):
    '''
        Test cases verifying CollisionProvides container behavior.

        It defines:

            :methods:
                | test_container_fields - Verifies components held in container.
                | test_get_version - Verifies implementation version string.
    '''

    def test_container_fields(self) -> None:
        '''
            Verifies all expected collision ports are correctly encapsulated.

            :exceptions: None.
        '''
        box_checker = BoxCollisionChecker()
        circle_checker = CircleCollisionChecker()
        spatial_checker = SpatialCollisionChecker(
            box_checker=box_checker,
            circle_checker=circle_checker,
        )
        registry = ZoneRegistry()

        provides = CollisionProvides(
            registry=registry,
            spatial_checker=spatial_checker,
            box_checker=box_checker,
            circle_checker=circle_checker,
        )
        self.assertIs(provides.registry, registry)
        self.assertIs(provides.spatial_checker, spatial_checker)
        self.assertIs(provides.box_checker, box_checker)
        self.assertIs(provides.circle_checker, circle_checker)

    def test_get_version(self) -> None:
        '''
            Verifies get_version returns implementation version string.

            :exceptions: None.
        '''
        box_checker = BoxCollisionChecker()
        circle_checker = CircleCollisionChecker()
        spatial_checker = SpatialCollisionChecker(
            box_checker=box_checker,
            circle_checker=circle_checker,
        )
        registry = ZoneRegistry()

        provides = CollisionProvides(
            registry=registry,
            spatial_checker=spatial_checker,
            box_checker=box_checker,
            circle_checker=circle_checker,
        )
        self.assertEqual(provides.get_version(), __version__)


if __name__ == '__main__':
    main()
