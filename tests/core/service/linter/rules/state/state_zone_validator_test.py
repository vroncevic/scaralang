# -*- coding: UTF-8 -*-

'''
Module
    state_zone_validator_test.py
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
    Unit tests for StateZoneValidator operations.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.model.dsl.ast.command_type import ScaraCommandType
from scaralang.core.model.dsl.ast.instruction import ScaraInstruction
from scaralang.core.model.dsl.ast.instruction_param import InstructionParam
from scaralang.core.model.dsl.ast.zone_mode import ZoneMode
from scaralang.core.model.dsl.diagnostic.scara_diagnostic_code import ScaraDiagnosticCode
from scaralang.core.model.dsl.diagnostic.scara_diagnostic_severity import ScaraDiagnosticSeverity
from scaralang.core.model.dsl.linter.scara_lint_context import ScaraLintContext
from scaralang.core.service.linter.rules.state.state_zone_validator import StateZoneValidator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.6'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestStateZoneValidator(TestCase):
    '''
        Test cases verifying StateZoneValidator operations.

        It defines:

            :methods:
                | test_valid_zone_updates_context - Verifies valid ZONE BLEND updates context.
                | test_invalid_zone_mode_emits_warning - Verifies invalid zone mode diagnostic.
                | test_negative_radius_emits_warning - Verifies negative radius diagnostic.
                | test_non_zone_instruction_no_op - Verifies non-ZONE command ignored.
                | test_name - Verifies validator name property.
    '''

    def test_valid_zone_updates_context(self) -> None:
        '''
            Verifies valid ZONE BLEND updates context zone_mode and zone_radius.
        '''
        validator = StateZoneValidator()
        instruction = ScaraInstruction(
            command_type=ScaraCommandType.ZONE,
            line_number=1,
            raw_text='ZONE BLEND R=15.0',
            parameters={
                InstructionParam.MODE: 'BLEND',
                InstructionParam.RADIUS: 15.0,
            },
        )
        context = ScaraLintContext()

        diagnostics = validator.validate(
            instruction=instruction,
            context=context,
        )

        self.assertEqual(len(diagnostics), 0)
        self.assertEqual(context.zone_mode, ZoneMode.BLEND)
        self.assertEqual(context.zone_radius, 15.0)

    def test_invalid_zone_mode_emits_warning(self) -> None:
        '''
            Verifies WARNING diagnostic on unknown zone mode.
        '''
        validator = StateZoneValidator()
        instruction = ScaraInstruction(
            command_type=ScaraCommandType.ZONE,
            line_number=2,
            raw_text='ZONE TURBO',
            parameters={
                InstructionParam.MODE: 'TURBO',
                InstructionParam.RADIUS: 0.0,
            },
        )
        context = ScaraLintContext()

        diagnostics = validator.validate(
            instruction=instruction,
            context=context,
        )

        self.assertEqual(len(diagnostics), 1)
        self.assertEqual(diagnostics[0].code, ScaraDiagnosticCode.INVALID_ZONE_MODE)
        self.assertEqual(diagnostics[0].severity, ScaraDiagnosticSeverity.WARNING)
        self.assertEqual(context.zone_mode, ZoneMode.FINE)

    def test_negative_radius_emits_warning(self) -> None:
        '''
            Verifies WARNING diagnostic on negative zone radius.
        '''
        validator = StateZoneValidator()
        instruction = ScaraInstruction(
            command_type=ScaraCommandType.ZONE,
            line_number=3,
            raw_text='ZONE BLEND R=-5.0',
            parameters={
                InstructionParam.MODE: 'BLEND',
                InstructionParam.RADIUS: -5.0,
            },
        )
        context = ScaraLintContext()

        diagnostics = validator.validate(
            instruction=instruction,
            context=context,
        )

        self.assertEqual(len(diagnostics), 1)
        self.assertEqual(diagnostics[0].code, ScaraDiagnosticCode.INVALID_ZONE_RADIUS)
        self.assertEqual(diagnostics[0].severity, ScaraDiagnosticSeverity.WARNING)

    def test_non_zone_instruction_no_op(self) -> None:
        '''
            Verifies non-ZONE instruction produces no diagnostics or context updates.
        '''
        validator = StateZoneValidator()
        instruction = ScaraInstruction(
            command_type=ScaraCommandType.HOME,
            line_number=4,
            raw_text='HOME',
            parameters={},
        )
        context = ScaraLintContext()

        diagnostics = validator.validate(
            instruction=instruction,
            context=context,
        )

        self.assertEqual(len(diagnostics), 0)

    def test_name(self) -> None:
        '''
            Verifies validator name property.
        '''
        validator = StateZoneValidator()
        self.assertEqual(validator.name, 'state_zone')


if __name__ == '__main__':
    main()
