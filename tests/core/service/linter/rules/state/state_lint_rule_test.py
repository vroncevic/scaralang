# -*- coding: UTF-8 -*-

'''
Module
    state_lint_rule_test.py
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
    Unit tests for StateLintRule operations.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.model.dsl.ast.command_type import ScaraCommandType
from scaralang.core.model.dsl.ast.instruction import ScaraInstruction
from scaralang.core.model.dsl.ast.instruction_param import InstructionParam
from scaralang.core.model.dsl.ast.zone_mode import ZoneMode
from scaralang.core.model.dsl.diagnostic.scara_diagnostic_code import ScaraDiagnosticCode
from scaralang.core.model.dsl.linter.scara_lint_context import ScaraLintContext
from scaralang.core.model.motor.motor_drive_mode import MotorDriveMode
from scaralang.core.service.linter.rules.state.motor_mode_validator_factory import MotorModeValidatorFactory
from scaralang.core.service.linter.rules.state.state_homing_validator_factory import StateHomingValidatorFactory
from scaralang.core.service.linter.rules.state.state_zone_validator_factory import StateZoneValidatorFactory
from scaralang.core.service.linter.rules.state.state_lint_rule import StateLintRule

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestStateLintRule(TestCase):
    '''
        Test cases verifying StateLintRule operations.

        It defines:

            :methods:
                | setUp - Initializes StateLintRule with injected validators.
                | test_name - Verifies rule identifier name.
                | test_home_instruction_updates_context - Verifies HOME updates context.
                | test_zone_instruction_updates_context - Verifies ZONE updates context.
                | test_invalid_zone_mode_emits_diagnostic - Verifies invalid zone mode diagnostic.
                | test_unrelated_instruction_ignored - Verifies unhandled instructions are ignored cleanly.
    '''

    def setUp(self) -> None:
        '''
            Sets up test StateLintRule instance with collaborating validators.
        '''
        self.rule = StateLintRule(
            homing_validator=StateHomingValidatorFactory.create(),
            zone_validator=StateZoneValidatorFactory.create(),
            motor_mode_validator=MotorModeValidatorFactory.create(),
        )

    def test_name(self) -> None:
        '''
            Verifies rule identifier name is 'state'.
        '''
        self.assertEqual(self.rule.name, 'state')

    def test_home_instruction_updates_context(self) -> None:
        '''
            Verifies HOME instruction sets is_homed to True and clears coords.
        '''
        rule = self.rule
        instruction = ScaraInstruction(
            command_type=ScaraCommandType.HOME,
            line_number=1,
            raw_text='HOME',
            parameters={},
        )
        context = ScaraLintContext(is_homed=False, last_coords=(10.0, 20.0, 30.0, 0.0))

        diagnostics = rule.check(
            instruction=instruction,
            context=context,
        )

        self.assertTrue(context.is_homed)
        self.assertEqual(context.last_coords, ())
        self.assertEqual(len(diagnostics), 0)

    def test_zone_instruction_updates_context(self) -> None:
        '''
            Verifies ZONE BLEND instruction updates context zone_mode and radius.
        '''
        rule = self.rule
        instruction = ScaraInstruction(
            command_type=ScaraCommandType.ZONE,
            line_number=2,
            raw_text='ZONE BLEND R=20.0',
            parameters={
                InstructionParam.MODE: 'BLEND',
                InstructionParam.RADIUS: 20.0,
            },
        )
        context = ScaraLintContext()

        diagnostics = rule.check(
            instruction=instruction,
            context=context,
        )

        self.assertEqual(context.zone_mode, ZoneMode.BLEND)
        self.assertEqual(context.zone_radius, 20.0)
        self.assertEqual(len(diagnostics), 0)

    def test_invalid_zone_mode_emits_diagnostic(self) -> None:
        '''
            Verifies invalid zone mode emits INVALID_ZONE_MODE diagnostic.
        '''
        rule = self.rule
        instruction = ScaraInstruction(
            command_type=ScaraCommandType.ZONE,
            line_number=3,
            raw_text='ZONE FAST',
            parameters={InstructionParam.MODE: 'FAST', InstructionParam.RADIUS: 0.0},
        )
        context = ScaraLintContext()

        diagnostics = rule.check(
            instruction=instruction,
            context=context,
        )

        codes = [d.code for d in diagnostics]
        self.assertIn(ScaraDiagnosticCode.INVALID_ZONE_MODE, codes)

    def test_unrelated_instruction_ignored(self) -> None:
        '''
            Verifies instructions other than HOME/ZONE are ignored cleanly.
        '''
        rule = self.rule
        instruction = ScaraInstruction(
            command_type=ScaraCommandType.MOVE_L,
            line_number=4,
            raw_text='MOVE_L X=10.0',
            parameters={},
        )
        context = ScaraLintContext()

        diagnostics = rule.check(
            instruction=instruction,
            context=context,
        )

        self.assertEqual(len(diagnostics), 0)

    def test_config_motor_updates_context(self) -> None:
        '''
            Verifies CONFIG_MOTOR updates motor_drive_mode in context.
        '''
        rule = self.rule
        instruction = ScaraInstruction(
            command_type=ScaraCommandType.CONFIG_MOTOR,
            line_number=5,
            raw_text='CONFIG MOTOR CLOSED_LOOP',
            parameters={
                InstructionParam.MODE: MotorDriveMode.CLOSED_LOOP.value,
            },
        )
        context = ScaraLintContext()

        diagnostics = rule.check(
            instruction=instruction,
            context=context,
        )

        self.assertEqual(context.motor_drive_mode, MotorDriveMode.CLOSED_LOOP)
        self.assertEqual(len(diagnostics), 0)


if __name__ == '__main__':
    main()
