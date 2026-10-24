# -*- coding: UTF-8 -*-

'''
Module
    dependencies_test.py
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
    Unit tests for ObstacleDependencies container.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.service.linter.rules.obstacle.dependencies import ObstacleDependencies
from scaralang.core.service.trajectory.avoidance.collision.box_checker import BoxCollisionChecker
from scaralang.core.service.trajectory.avoidance.collision.circle_checker import CircleCollisionChecker
from scaralang.core.service.trajectory.avoidance.collision.spatial_checker import SpatialCollisionChecker
from scaralang.core.service.trajectory.avoidance.collision.zone_registry import ZoneRegistry

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestObstacleDependencies(TestCase):
    '''
        Test cases verifying ObstacleDependencies container.

        It defines:

            :methods:
                | test_dependencies_encapsulation - Verifies fields held in bundle.
    '''

    def test_dependencies_encapsulation(self) -> None:
        '''
            Verifies inbound dependencies container correctly encapsulates protocol ports.

            :exceptions: None.
        '''
        registry = ZoneRegistry()
        spatial_checker = SpatialCollisionChecker(
            box_checker=BoxCollisionChecker(),
            circle_checker=CircleCollisionChecker(),
        )
        dependencies = ObstacleDependencies(
            zone_registry=registry,
            spatial_checker=spatial_checker,
        )
        self.assertIs(dependencies.zone_registry, registry)
        self.assertIs(dependencies.spatial_checker, spatial_checker)


if __name__ == '__main__':
    main()
