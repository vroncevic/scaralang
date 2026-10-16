# -*- coding: UTF-8 -*-

'''
Module
    validator_test.py
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
    Unit tests for FlybyValidator operations.
'''

from __future__ import annotations

from unittest import TestCase, main

from scaralang.core.model.dsl.ast.command_type import ScaraCommandType
from scaralang.core.model.dsl.ast.instruction import ScaraInstruction
from scaralang.core.model.dsl.ast.instruction_param import ScaraInstructionParam
from scaralang.core.model.dsl.ast.pneumatic_state import PneumaticState
from scaralang.core.model.dsl.ast.zone_mode import ZoneMode
from scaralang.core.model.dsl.diagnostic.scara_diagnostic_code import ScaraDiagnosticCode
from scaralang.core.model.dsl.diagnostic.scara_diagnostic_severity import ScaraDiagnosticSeverity
from scaralang.core.service.linter.context.factory import LintContextFactory
from scaralang.core.service.linter.rules.pneumatic.flyby.validator import FlybyValidator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.9'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestFlybyValidator(TestCase):
    '''
        Test cases verifying FlybyValidator operations.

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
        validator = FlybyValidator()
        instruction = ScaraInstruction(
            command_type=ScaraCommandType.PUMP,
            line_number=4,
            raw_text='PUMP ON',
            parameters={ScaraInstructionParam.STATE: PneumaticState.ON},
        )
        context = LintContextFactory.create()
        context.zone_mode = ZoneMode.BLEND
        context.zone_radius = 10.0

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
        validator = FlybyValidator()
        instruction = ScaraInstruction(
            command_type=ScaraCommandType.VALVE,
            line_number=5,
            raw_text='VALVE OFF',
            parameters={ScaraInstructionParam.STATE: PneumaticState.OFF},
        )
        context = LintContextFactory.create()

        diagnostics = validator.validate(
            instruction=instruction,
            context=context,
        )

        self.assertEqual(len(diagnostics), 0)

    def test_name(self) -> None:
        '''
            Verifies validator name property.
        '''
        validator = FlybyValidator()
        self.assertEqual(validator.name, 'pneumatic_flyby')


if __name__ == '__main__':
    main()
