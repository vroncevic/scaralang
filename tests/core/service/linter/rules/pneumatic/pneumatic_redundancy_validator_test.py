# -*- coding: UTF-8 -*-

'''
Module
    pneumatic_redundancy_validator_test.py
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
    Unit tests for PneumaticRedundancyValidator operations.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.model.dsl.ast.command_type import ScaraCommandType
from scaralang.core.model.dsl.ast.instruction import ScaraInstruction
from scaralang.core.model.dsl.ast.instruction_param import InstructionParam
from scaralang.core.model.dsl.ast.pneumatic_state import PneumaticState
from scaralang.core.model.dsl.diagnostic.scara_diagnostic_code import ScaraDiagnosticCode
from scaralang.core.model.dsl.diagnostic.scara_diagnostic_severity import ScaraDiagnosticSeverity
from scaralang.core.model.dsl.linter.lint_tool_state import LintToolState
from scaralang.core.model.dsl.linter.scara_lint_context import ScaraLintContext
from scaralang.core.service.linter.rules.pneumatic.pneumatic_redundancy_validator import PneumaticRedundancyValidator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestPneumaticRedundancyValidator(TestCase):
    '''
        Test cases verifying PneumaticRedundancyValidator operations.

        It defines:

            :methods:
                | test_redundant_on_emits_warning - Verifies REDUNDANT_TOOL_CMD when tool already ON.
                | test_redundant_off_emits_warning - Verifies REDUNDANT_TOOL_CMD when tool already OFF.
                | test_state_transition_no_diagnostic - Verifies clean state change produces no warning.
                | test_name - Verifies validator name property.
    '''

    def test_redundant_on_emits_warning(self) -> None:
        '''
            Verifies warning diagnostic when command requests ON while already ON.
        '''
        validator = PneumaticRedundancyValidator()
        instruction = ScaraInstruction(
            command_type=ScaraCommandType.PUMP,
            line_number=7,
            raw_text='PUMP ON',
            parameters={InstructionParam.STATE: PneumaticState.ON},
        )
        context = ScaraLintContext(tool_state=LintToolState(pump_on=True))

        diagnostics = validator.validate(
            instruction=instruction,
            context=context,
        )

        self.assertEqual(len(diagnostics), 1)
        self.assertEqual(diagnostics[0].code, ScaraDiagnosticCode.REDUNDANT_TOOL_CMD)
        self.assertEqual(diagnostics[0].severity, ScaraDiagnosticSeverity.WARNING)
        self.assertIn('already ON', diagnostics[0].message)

    def test_redundant_off_emits_warning(self) -> None:
        '''
            Verifies warning diagnostic when command requests OFF while already OFF.
        '''
        validator = PneumaticRedundancyValidator()
        instruction = ScaraInstruction(
            command_type=ScaraCommandType.VALVE,
            line_number=8,
            raw_text='VALVE OFF',
            parameters={InstructionParam.STATE: PneumaticState.OFF},
        )
        context = ScaraLintContext(tool_state=LintToolState(valve_on=False))

        diagnostics = validator.validate(
            instruction=instruction,
            context=context,
        )

        self.assertEqual(len(diagnostics), 1)
        self.assertEqual(diagnostics[0].code, ScaraDiagnosticCode.REDUNDANT_TOOL_CMD)
        self.assertEqual(diagnostics[0].severity, ScaraDiagnosticSeverity.WARNING)
        self.assertIn('already OFF', diagnostics[0].message)

    def test_state_transition_no_diagnostic(self) -> None:
        '''
            Verifies no diagnostic is emitted when tool changes state legitimately.
        '''
        validator = PneumaticRedundancyValidator()
        instruction = ScaraInstruction(
            command_type=ScaraCommandType.PUMP,
            line_number=9,
            raw_text='PUMP ON',
            parameters={InstructionParam.STATE: PneumaticState.ON},
        )
        context = ScaraLintContext(tool_state=LintToolState(pump_on=False))

        diagnostics = validator.validate(
            instruction=instruction,
            context=context,
        )

        self.assertEqual(len(diagnostics), 0)

    def test_name(self) -> None:
        '''
            Verifies validator name property.
        '''
        validator = PneumaticRedundancyValidator()
        self.assertEqual(validator.name, 'pneumatic_redundancy')


if __name__ == '__main__':
    main()
