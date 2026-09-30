# -*- coding: UTF-8 -*-

'''
Module
    pneumatic_lint_rule_test.py
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
    Unit tests for PneumaticLintRule operations.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.model.dsl.ast.command_type import ScaraCommandType
from scaralang.core.model.dsl.ast.instruction import ScaraInstruction
from scaralang.core.model.dsl.ast.instruction_param import InstructionParam
from scaralang.core.model.dsl.ast.pneumatic_state import PneumaticState
from scaralang.core.model.dsl.ast.zone_mode import ZoneMode
from scaralang.core.model.dsl.diagnostic.scara_diagnostic_code import ScaraDiagnosticCode
from scaralang.core.model.dsl.linter.scara_lint_context import ScaraLintContext
from scaralang.core.service.linter.rules.pneumatic.pneumatic_conflict_validator_factory import PneumaticConflictValidatorFactory
from scaralang.core.service.linter.rules.pneumatic.pneumatic_flyby_validator_factory import PneumaticFlybyValidatorFactory
from scaralang.core.service.linter.rules.pneumatic.pneumatic_redundancy_validator_factory import PneumaticRedundancyValidatorFactory
from scaralang.core.service.linter.rules.pneumatic.pneumatic_lint_rule import PneumaticLintRule

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestPneumaticLintRule(TestCase):
    '''
        Test cases verifying PneumaticLintRule operations.

        It defines:

            :methods:
                | setUp - Initializes PneumaticLintRule with injected validators.
                | test_name - Verifies rule identifier name.
                | test_pump_conflict_detected - Verifies PNEUMATIC_CONFLICT on pump/valve contention.
                | test_redundant_command_detected - Verifies REDUNDANT_TOOL_CMD on identical state.
                | test_tool_in_flyby_detected - Verifies TOOL_IN_FLYBY during blend zone.
                | test_non_pneumatic_instruction_ignored - Verifies other instructions are ignored.
    '''

    def setUp(self) -> None:
        '''
            Sets up test PneumaticLintRule instance with collaborating validators.
        '''
        self.rule = PneumaticLintRule(
            flyby_validator=PneumaticFlybyValidatorFactory.create(),
            redundancy_validator=PneumaticRedundancyValidatorFactory.create(),
            conflict_validator=PneumaticConflictValidatorFactory.create(),
        )

    def test_name(self) -> None:
        '''
            Verifies rule identifier name is 'pneumatic'.
        '''
        self.assertEqual(self.rule.name, 'pneumatic')

    def test_pump_conflict_detected(self) -> None:
        '''
            Verifies PNEUMATIC_CONFLICT diagnostic when PUMP ON is issued while VALVE is ON.
        '''
        rule = self.rule
        instruction = ScaraInstruction(
            command_type=ScaraCommandType.PUMP,
            line_number=1,
            raw_text='PUMP ON',
            parameters={InstructionParam.STATE: PneumaticState.ON},
        )
        context = ScaraLintContext(valve_on=True)

        diagnostics = rule.check(
            instruction=instruction,
            context=context,
        )

        codes = [d.code for d in diagnostics]
        self.assertIn(ScaraDiagnosticCode.PNEUMATIC_CONFLICT, codes)
        self.assertTrue(context.pump_on)

    def test_redundant_command_detected(self) -> None:
        '''
            Verifies REDUNDANT_TOOL_CMD diagnostic when VALVE ON is issued while VALVE is already ON.
        '''
        rule = self.rule
        instruction = ScaraInstruction(
            command_type=ScaraCommandType.VALVE,
            line_number=2,
            raw_text='VALVE ON',
            parameters={InstructionParam.STATE: PneumaticState.ON},
        )
        context = ScaraLintContext(valve_on=True)

        diagnostics = rule.check(
            instruction=instruction,
            context=context,
        )

        codes = [d.code for d in diagnostics]
        self.assertIn(ScaraDiagnosticCode.REDUNDANT_TOOL_CMD, codes)

    def test_tool_in_flyby_detected(self) -> None:
        '''
            Verifies TOOL_IN_FLYBY diagnostic when tool command issued in active blend zone.
        '''
        rule = self.rule
        instruction = ScaraInstruction(
            command_type=ScaraCommandType.PUMP,
            line_number=3,
            raw_text='PUMP ON',
            parameters={InstructionParam.STATE: PneumaticState.ON},
        )
        context = ScaraLintContext(zone_mode=ZoneMode.BLEND, zone_radius=5.0)

        diagnostics = rule.check(
            instruction=instruction,
            context=context,
        )

        codes = [d.code for d in diagnostics]
        self.assertIn(ScaraDiagnosticCode.TOOL_IN_FLYBY, codes)

    def test_non_pneumatic_instruction_ignored(self) -> None:
        '''
            Verifies non-pneumatic instructions produce no checks or changes.
        '''
        rule = self.rule
        instruction = ScaraInstruction(
            command_type=ScaraCommandType.HOME,
            line_number=4,
            raw_text='HOME',
            parameters={},
        )
        context = ScaraLintContext()

        diagnostics = rule.check(
            instruction=instruction,
            context=context,
        )

        self.assertEqual(len(diagnostics), 0)


if __name__ == '__main__':
    main()
