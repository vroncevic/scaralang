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
    Unit tests for BlendZoneValidator operations.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.model.dsl.ast.command_type import ScaraCommandType
from scaralang.core.model.dsl.ast.instruction import ScaraInstruction
from scaralang.core.model.dsl.ast.instruction_param import ScaraInstructionParam
from scaralang.core.model.dsl.ast.zone_mode import ZoneMode
from scaralang.core.model.dsl.diagnostic.scara_diagnostic_code import ScaraDiagnosticCode
from scaralang.core.model.dsl.diagnostic.scara_diagnostic_severity import ScaraDiagnosticSeverity
from scaralang.core.service.linter.context.factory import LintContextFactory
from scaralang.core.service.linter.rules.timing.blend_zone.validator import BlendZoneValidator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.9'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestBlendZoneValidator(TestCase):
    '''
        Test cases verifying BlendZoneValidator operations.

        It defines:

            :methods:
                | test_dwell_during_blend_zone_emits_warning - Verifies dwell in active BLEND emits warning.
                | test_dwell_during_fine_zone_no_diagnostic - Verifies dwell in FINE mode produces no warning.
                | test_non_wait_command_no_op - Verifies other commands are ignored.
                | test_name - Verifies validator name property.
    '''

    def test_dwell_during_blend_zone_emits_warning(self) -> None:
        '''
            Verifies TOOL_IN_FLYBY warning diagnostic when dwell pause is inside blend zone.
        '''
        validator = BlendZoneValidator()
        instruction = ScaraInstruction(
            command_type=ScaraCommandType.WAIT_MS,
            line_number=3,
            raw_text='WAIT_MS 100',
            parameters={ScaraInstructionParam.MS: 100.0},
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
        self.assertEqual(diagnostics[0].line, 3)

    def test_dwell_during_fine_zone_no_diagnostic(self) -> None:
        '''
            Verifies no diagnostic is emitted when dwell occurs in FINE zone mode.
        '''
        validator = BlendZoneValidator()
        instruction = ScaraInstruction(
            command_type=ScaraCommandType.WAIT_MS,
            line_number=4,
            raw_text='WAIT_MS 100',
            parameters={ScaraInstructionParam.MS: 100.0},
        )
        context = LintContextFactory.create()

        diagnostics = validator.validate(
            instruction=instruction,
            context=context,
        )

        self.assertEqual(len(diagnostics), 0)

    def test_non_wait_command_no_op(self) -> None:
        '''
            Verifies non-WAIT_MS command is ignored.
        '''
        validator = BlendZoneValidator()
        instruction = ScaraInstruction(
            command_type=ScaraCommandType.MOVE_L,
            line_number=5,
            raw_text='MOVE_L X=100.0',
            parameters={},
        )
        context = LintContextFactory.create()
        context.zone_mode = ZoneMode.BLEND
        context.zone_radius = 10.0

        diagnostics = validator.validate(
            instruction=instruction,
            context=context,
        )

        self.assertEqual(len(diagnostics), 0)

    def test_name(self) -> None:
        '''
            Verifies validator name property.
        '''
        validator = BlendZoneValidator()
        self.assertEqual(validator.name, 'timing_blend_zone')


if __name__ == '__main__':
    main()
