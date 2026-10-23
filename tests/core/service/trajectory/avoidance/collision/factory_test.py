# -*- coding: UTF-8 -*-

'''
Module
    factory_test.py
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
    Unit tests for CollisionFactory implementation.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.service.trajectory.avoidance.collision.factory import CollisionFactory
from scaralang.core.service.trajectory.avoidance.collision.ibox_checker import IBoxCollisionChecker
from scaralang.core.service.trajectory.avoidance.collision.icircle_checker import ICircleCollisionChecker
from scaralang.core.service.trajectory.avoidance.collision.ispatial_checker import ISpatialCollisionChecker
from scaralang.core.service.trajectory.avoidance.collision.izone_registry import IZoneRegistry
from scaralang.core.service.trajectory.avoidance.collision.provides import CollisionProvides

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestCollisionFactory(TestCase):
    '''
        Test cases verifying CollisionFactory construction and wiring.

        It defines:

            :methods:
                | test_create - Verifies creation of CollisionProvides container.
                | test_get_version - Verifies implementation version string.
    '''

    def test_create(self) -> None:
        '''
            Verifies factory constructs fully wired CollisionProvides instance.

            :exceptions: None.
        '''
        provides: CollisionProvides = CollisionFactory.create()
        self.assertIsInstance(provides, CollisionProvides)
        self.assertIsInstance(provides.registry, IZoneRegistry)
        self.assertIsInstance(provides.spatial_checker, ISpatialCollisionChecker)
        self.assertIsInstance(provides.box_checker, IBoxCollisionChecker)
        self.assertIsInstance(provides.circle_checker, ICircleCollisionChecker)

    def test_get_version(self) -> None:
        '''
            Verifies get_version returns implementation version string.

            :exceptions: None.
        '''
        self.assertEqual(CollisionFactory.get_version(), __version__)


if __name__ == '__main__':
    main()
