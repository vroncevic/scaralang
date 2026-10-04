# -*- coding: UTF-8 -*-

'''
Module
    pneumatic_conflict_validator_test.py
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
    Unit tests for PneumaticConflictValidator operations.
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
from scaralang.core.service.linter.rules.pneumatic.pneumatic_conflict_validator import PneumaticConflictValidator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestPneumaticConflictValidator(TestCase):
    '''
        Test cases verifying PneumaticConflictValidator operations.

        It defines:

            :methods:
                | test_pump_conflict_with_valve_emits_error - Verifies ERROR on PUMP ON while VALVE active.
                | test_valve_conflict_with_pump_emits_error - Verifies ERROR on VALVE ON while PUMP active.
                | test_non_conflicting_state_no_diagnostic - Verifies clean activation without conflict.
                | test_name - Verifies validator name property.
    '''

    def test_pump_conflict_with_valve_emits_error(self) -> None:
        '''
            Verifies PNEUMATIC_CONFLICT ERROR when turning PUMP ON while VALVE is active.
        '''
        validator = PneumaticConflictValidator()
        instruction = ScaraInstruction(
            command_type=ScaraCommandType.PUMP,
            line_number=10,
            raw_text='PUMP ON',
            parameters={InstructionParam.STATE: PneumaticState.ON},
        )
        context = ScaraLintContext(tool_state=LintToolState(valve_on=True))

        diagnostics = validator.validate(
            instruction=instruction,
            context=context,
        )

        self.assertEqual(len(diagnostics), 1)
        self.assertEqual(diagnostics[0].code, ScaraDiagnosticCode.PNEUMATIC_CONFLICT)
        self.assertEqual(diagnostics[0].severity, ScaraDiagnosticSeverity.ERROR)
        self.assertIn('blow-off VALVE is active', diagnostics[0].message)

    def test_valve_conflict_with_pump_emits_error(self) -> None:
        '''
            Verifies PNEUMATIC_CONFLICT ERROR when turning VALVE ON while PUMP is active.
        '''
        validator = PneumaticConflictValidator()
        instruction = ScaraInstruction(
            command_type=ScaraCommandType.VALVE,
            line_number=11,
            raw_text='VALVE ON',
            parameters={InstructionParam.STATE: PneumaticState.ON},
        )
        context = ScaraLintContext(tool_state=LintToolState(pump_on=True))

        diagnostics = validator.validate(
            instruction=instruction,
            context=context,
        )

        self.assertEqual(len(diagnostics), 1)
        self.assertEqual(diagnostics[0].code, ScaraDiagnosticCode.PNEUMATIC_CONFLICT)
        self.assertEqual(diagnostics[0].severity, ScaraDiagnosticSeverity.ERROR)
        self.assertIn('vacuum PUMP is active', diagnostics[0].message)

    def test_non_conflicting_state_no_diagnostic(self) -> None:
        '''
            Verifies no diagnostic when turning tool ON with no conflicting tool active.
        '''
        validator = PneumaticConflictValidator()
        instruction = ScaraInstruction(
            command_type=ScaraCommandType.PUMP,
            line_number=12,
            raw_text='PUMP ON',
            parameters={InstructionParam.STATE: PneumaticState.ON},
        )
        context = ScaraLintContext(tool_state=LintToolState(valve_on=False))

        diagnostics = validator.validate(
            instruction=instruction,
            context=context,
        )

        self.assertEqual(len(diagnostics), 0)

    def test_name(self) -> None:
        '''
            Verifies validator name property.
        '''
        validator = PneumaticConflictValidator()
        self.assertEqual(validator.name, 'pneumatic_conflict')


if __name__ == '__main__':
    main()
