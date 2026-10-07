# -*- coding: UTF-8 -*-

'''
Module
    pneumatic_flyby_validator_test.py
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
    Unit tests for PneumaticFlybyValidator operations.
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
from scaralang.core.model.dsl.diagnostic.scara_diagnostic_severity import ScaraDiagnosticSeverity
from scaralang.core.model.dsl.linter.scara_lint_context import ScaraLintContext
from scaralang.core.service.linter.rules.pneumatic.pneumatic_flyby_validator import PneumaticFlybyValidator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.7'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestPneumaticFlybyValidator(TestCase):
    '''
        Test cases verifying PneumaticFlybyValidator operations.

        It defines:

            :methods:
                | test_tool_action_during_blend_emits_warning - Verifies TOOL_IN_FLYBY in active BLEND.
                | test_tool_action_during_fine_no_diagnostic - Verifies clean execution in FINE mode.
                | test_name - Verifies validator name property.
    '''

    def test_tool_action_during_blend_emits_warning(self) -> None:
        '''
            Verifies TOOL_IN_FLYBY diagnostic when tool action occurs during continuous blend.
        '''
        validator = PneumaticFlybyValidator()
        instruction = ScaraInstruction(
            command_type=ScaraCommandType.PUMP,
            line_number=4,
            raw_text='PUMP ON',
            parameters={InstructionParam.STATE: PneumaticState.ON},
        )
        context = ScaraLintContext(
            zone_mode=ZoneMode.BLEND,
            zone_radius=10.0,
        )

        diagnostics = validator.validate(
            instruction=instruction,
            context=context,
        )

        self.assertEqual(len(diagnostics), 1)
        self.assertEqual(diagnostics[0].code, ScaraDiagnosticCode.TOOL_IN_FLYBY)
        self.assertEqual(diagnostics[0].severity, ScaraDiagnosticSeverity.WARNING)
        self.assertEqual(diagnostics[0].line, 4)

    def test_tool_action_during_fine_no_diagnostic(self) -> None:
        '''
            Verifies no diagnostic is emitted when tool action occurs in FINE zone mode.
        '''
        validator = PneumaticFlybyValidator()
        instruction = ScaraInstruction(
            command_type=ScaraCommandType.VALVE,
            line_number=5,
            raw_text='VALVE OFF',
            parameters={InstructionParam.STATE: PneumaticState.OFF},
        )
        context = ScaraLintContext(
            zone_mode=ZoneMode.FINE,
            zone_radius=0.0,
        )

        diagnostics = validator.validate(
            instruction=instruction,
            context=context,
        )

        self.assertEqual(len(diagnostics), 0)

    def test_name(self) -> None:
        '''
            Verifies validator name property.
        '''
        validator = PneumaticFlybyValidator()
        self.assertEqual(validator.name, 'pneumatic_flyby')


if __name__ == '__main__':
    main()
