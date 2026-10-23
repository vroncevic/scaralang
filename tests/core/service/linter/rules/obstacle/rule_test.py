# -*- coding: UTF-8 -*-

'''
Module
    rule_test.py
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
    Unit tests for ObstacleLintRule implementation.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.model.dsl.ast.command_type import ScaraCommandType
from scaralang.core.model.dsl.ast.instruction import ScaraInstruction
from scaralang.core.model.dsl.ast.instruction_param import ScaraInstructionParam
from scaralang.core.model.dsl.ast.zone_mode import ZoneMode
from scaralang.core.model.dsl.diagnostic.code import ScaraDiagnosticCode
from scaralang.core.model.dsl.diagnostic.diagnostic import ScaraDiagnostic
from scaralang.core.model.dsl.linter.context import LintContext
from scaralang.core.model.dsl.linter.tool_state import LintToolState
from scaralang.core.model.motor.mode import MotorDriveMode
from scaralang.core.model.trajectory.obstacle.shape import ObstacleShape
from scaralang.core.service.linter.rules.obstacle.builder.builder import ZoneBuilder
from scaralang.core.service.linter.rules.obstacle.rule import ObstacleLintRule
from scaralang.core.service.trajectory.avoidance.collision.box_checker import BoxCollisionChecker
from scaralang.core.service.trajectory.avoidance.collision.circle_checker import CircleCollisionChecker
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


class TestObstacleLintRule(TestCase):
    '''
        Test cases verifying ObstacleLintRule collision detection and obstacle registration.

        It defines:

            :methods:
                | setUp - Prepares ObstacleLintRule test fixture.
                | test_name_property - Verifies rule identifier name.
                | test_zone_def_registers_obstacle - Verifies ZONE_DEF registers obstacle.
                | test_motion_colliding_emits_diagnostic - Verifies path collision diagnostic.
                | test_motion_clear_returns_empty - Verifies collision-free path returns empty.
                | test_non_motion_instruction_returns_empty - Verifies non-motion returns empty.
                | test_get_version - Verifies implementation version string.
    '''

    def setUp(self) -> None:
        '''
            Prepares ObstacleLintRule test fixture.

            :exceptions: None.
        '''
        self._registry = ZoneRegistry()
        self._spatial_checker = SpatialCollisionChecker(
            box_checker=BoxCollisionChecker(),
            circle_checker=CircleCollisionChecker(),
        )
        self._rule = ObstacleLintRule(
            zone_builder=ZoneBuilder(),
            zone_registry=self._registry,
            spatial_checker=self._spatial_checker,
        )
        self._context = LintContext(
            is_homed=True,
            motion_occurred=True,
            tool_state=LintToolState(pump_on=False, valve_on=False),
            zone_mode=ZoneMode.FINE,
            zone_radius=0.0,
            last_coords=(0.0, 0.0),
            motor_drive_mode=MotorDriveMode.CLOSED_LOOP,
        )

    def test_name_property(self) -> None:
        '''
            Verifies rule identifier name is obstacle.

            :exceptions: None.
        '''
        self.assertEqual(self._rule.name, 'obstacle')

    def test_zone_def_registers_obstacle(self) -> None:
        '''
            Verifies ZONE_DEF statement registers obstacle in registry without diagnostics.

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
        diagnostics = self._rule.check(
            instruction=instruction, context=self._context
        )
        self.assertEqual(diagnostics, ())
        self.assertTrue(self._registry.has_zone('WALL'))

    def test_motion_colliding_emits_diagnostic(self) -> None:
        '''
            Verifies motion through declared obstacle produces diagnostic finding.

            :exceptions: None.
        '''
        zone_def_inst = ScaraInstruction(
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
        self._rule.check(instruction=zone_def_inst, context=self._context)

        move_inst = ScaraInstruction(
            command_type=ScaraCommandType.MOVE_L,
            line_number=2,
            raw_text='MOVE_L X=60.0 Y=0.0',
            parameters={
                ScaraInstructionParam.X.value: 60.0,
                ScaraInstructionParam.Y.value: 0.0,
            },
        )
        findings: tuple[ScaraDiagnostic, ...] = self._rule.check(
            instruction=move_inst, context=self._context
        )
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0].code, ScaraDiagnosticCode.OBSTACLE_COLLISION.value)

        context_no_coords = LintContext(
            is_homed=True,
            motion_occurred=True,
            tool_state=LintToolState(pump_on=False, valve_on=False),
            zone_mode=ZoneMode.FINE,
            zone_radius=0.0,
            last_coords=(),
            motor_drive_mode=MotorDriveMode.CLOSED_LOOP,
        )
        point_move = ScaraInstruction(
            command_type=ScaraCommandType.MOVE_L,
            line_number=3,
            raw_text='MOVE_L X=20.0 Y=0.0',
            parameters={
                ScaraInstructionParam.X.value: 20.0,
                ScaraInstructionParam.Y.value: 0.0,
            },
        )
        point_findings: tuple[ScaraDiagnostic, ...] = self._rule.check(
            instruction=point_move, context=context_no_coords
        )
        self.assertEqual(len(point_findings), 1)
        self.assertEqual(point_findings[0].code, ScaraDiagnosticCode.OBSTACLE_COLLISION.value)

    def test_motion_clear_returns_empty(self) -> None:
        '''
            Verifies motion path avoiding obstacles produces no diagnostics.

            :exceptions: None.
        '''
        zone_def_inst = ScaraInstruction(
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
        self._rule.check(instruction=zone_def_inst, context=self._context)

        move_inst = ScaraInstruction(
            command_type=ScaraCommandType.MOVE_L,
            line_number=2,
            raw_text='MOVE_L X=0.0 Y=100.0',
            parameters={
                ScaraInstructionParam.X.value: 0.0,
                ScaraInstructionParam.Y.value: 100.0,
            },
        )
        findings = self._rule.check(
            instruction=move_inst, context=self._context
        )
        self.assertEqual(findings, ())

    def test_non_motion_instruction_returns_empty(self) -> None:
        '''
            Verifies non-motion instruction produces no diagnostics.

            :exceptions: None.
        '''
        instruction = ScaraInstruction(
            command_type=ScaraCommandType.SYNC,
            line_number=5,
            raw_text='SYNC',
            parameters={},
        )
        findings = self._rule.check(
            instruction=instruction, context=self._context
        )
        self.assertEqual(findings, ())

    def test_get_version(self) -> None:
        '''
            Verifies get_version returns implementation version string.

            :exceptions: None.
        '''
        self.assertEqual(self._rule.get_version(), __version__)


if __name__ == '__main__':
    main()
