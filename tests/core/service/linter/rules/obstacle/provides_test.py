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
    Unit tests for ObstacleProvides container.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.service.linter.rules.obstacle.builder.builder import ZoneBuilder
from scaralang.core.service.linter.rules.obstacle.provides import ObstacleProvides
from scaralang.core.service.linter.rules.obstacle.rule import ObstacleLintRule
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


class TestObstacleProvides(TestCase):
    '''
        Test cases verifying ObstacleProvides container behavior.

        It defines:

            :methods:
                | test_rule_field - Verifies rule held in container.
                | test_get_version - Verifies implementation version string.
    '''

    def test_rule_field(self) -> None:
        '''
            Verifies rule port is correctly encapsulated in container.

            :exceptions: None.
        '''
        rule = ObstacleLintRule(
            zone_builder=ZoneBuilder(),
            zone_registry=ZoneRegistry(),
            spatial_checker=SpatialCollisionChecker(
                box_checker=BoxCollisionChecker(),
                circle_checker=CircleCollisionChecker(),
            ),
        )
        provides = ObstacleProvides(rule=rule)
        self.assertIs(provides.rule, rule)

    def test_get_version(self) -> None:
        '''
            Verifies get_version returns implementation version string.

            :exceptions: None.
        '''
        rule = ObstacleLintRule(
            zone_builder=ZoneBuilder(),
            zone_registry=ZoneRegistry(),
            spatial_checker=SpatialCollisionChecker(
                box_checker=BoxCollisionChecker(),
                circle_checker=CircleCollisionChecker(),
            ),
        )
        provides = ObstacleProvides(rule=rule)
        self.assertEqual(provides.get_version(), __version__)


if __name__ == '__main__':
    main()
