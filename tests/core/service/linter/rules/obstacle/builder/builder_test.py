# -*- coding: UTF-8 -*-

'''
Module
    builder_test.py
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
    Unit tests for ZoneBuilder implementation.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.model.dsl.ast.command_type import ScaraCommandType
from scaralang.core.model.dsl.ast.instruction import ScaraInstruction
from scaralang.core.model.dsl.ast.instruction_param import ScaraInstructionParam
from scaralang.core.model.trajectory.obstacle.box import BoxObstacle
from scaralang.core.model.trajectory.obstacle.circle import CircleObstacle
from scaralang.core.model.trajectory.obstacle.shape import ObstacleShape
from scaralang.core.model.trajectory.obstacle.zone import ObstacleZone
from scaralang.core.service.linter.rules.obstacle.builder.builder import ZoneBuilder

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestZoneBuilder(TestCase):
    '''
        Test cases verifying ZoneBuilder AST instruction mapping to ObstacleZone models.

        It defines:

            :methods:
                | setUp - Prepares ZoneBuilder test fixture.
                | test_build_box_zone - Verifies constructing rectangular obstacle zone.
                | test_build_circle_zone - Verifies constructing circular obstacle zone.
                | test_get_version - Verifies implementation version string.
    '''

    def setUp(self) -> None:
        '''
            Prepares ZoneBuilder test fixture.

            :exceptions: None.
        '''
        self._builder = ZoneBuilder()

    def test_build_box_zone(self) -> None:
        '''
            Verifies building an ObstacleZone containing BoxObstacle geometry.

            :exceptions: None.
        '''
        instruction = ScaraInstruction(
            command_type=ScaraCommandType.ZONE_DEF,
            line_number=1,
            raw_text='ZONE_DEF WALL BOX X_MIN=10.0 X_MAX=50.0 Y_MIN=-20.0 Y_MAX=30.0',
            parameters={
                ScaraInstructionParam.NAME.value: 'WALL',
                ScaraInstructionParam.SHAPE.value: ObstacleShape.BOX.value,
                ScaraInstructionParam.X_MIN.value: 10.0,
                ScaraInstructionParam.X_MAX.value: 50.0,
                ScaraInstructionParam.Y_MIN.value: -20.0,
                ScaraInstructionParam.Y_MAX.value: 30.0,
            },
        )
        zone: ObstacleZone = self._builder.build_zone(instruction=instruction)
        self.assertEqual(zone.name, 'WALL')
        self.assertEqual(zone.shape, ObstacleShape.BOX)
        self.assertIsInstance(zone.geometry, BoxObstacle)
        self.assertEqual(zone.geometry.x_min, 10.0)

    def test_build_circle_zone(self) -> None:
        '''
            Verifies building an ObstacleZone containing CircleObstacle geometry.

            :exceptions: None.
        '''
        instruction = ScaraInstruction(
            command_type=ScaraCommandType.ZONE_DEF,
            line_number=1,
            raw_text='ZONE_DEF POST CIRCLE X=120.0 Y=40.0 RADIUS=25.0',
            parameters={
                ScaraInstructionParam.NAME.value: 'POST',
                ScaraInstructionParam.SHAPE.value: ObstacleShape.CIRCLE.value,
                ScaraInstructionParam.X.value: 120.0,
                ScaraInstructionParam.Y.value: 40.0,
                ScaraInstructionParam.RADIUS.value: 25.0,
            },
        )
        zone: ObstacleZone = self._builder.build_zone(instruction=instruction)
        self.assertEqual(zone.name, 'POST')
        self.assertEqual(zone.shape, ObstacleShape.CIRCLE)
        self.assertIsInstance(zone.geometry, CircleObstacle)
        self.assertEqual(zone.geometry.radius, 25.0)

    def test_get_version(self) -> None:
        '''
            Verifies get_version returns implementation version string.

            :exceptions: None.
        '''
        self.assertEqual(self._builder.get_version(), __version__)


if __name__ == '__main__':
    main()
