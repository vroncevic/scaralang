# -*- coding: UTF-8 -*-

'''
Module
    timing_lint_rule_test.py
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
    Unit tests for TimingLintRule operations.
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
from scaralang.core.service.linter.rules.timing.timing_blend_zone_validator_factory import TimingBlendZoneValidatorFactory
from scaralang.core.service.linter.rules.timing.timing_dwell_validator_factory import TimingDwellValidatorFactory
from scaralang.core.service.linter.rules.timing.timing_lint_rule import TimingLintRule

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestTimingLintRule(TestCase):
    '''
        Test cases verifying TimingLintRule operations.

        It defines:

            :methods:
                | setUp - Initializes TimingLintRule with injected validators.
                | test_name - Verifies rule identifier name.
                | test_dead_wait_detected - Verifies non-positive dwell delay detected.
                | test_dwell_in_flyby_detected - Verifies dwell during blend zone detected.
                | test_non_timing_instruction_ignored - Verifies non-timing command ignored.
    '''

    def setUp(self) -> None:
        '''
            Sets up test TimingLintRule instance with collaborating validators.
        '''
        self.rule = TimingLintRule(
            dwell_validator=TimingDwellValidatorFactory.create(),
            blend_zone_validator=TimingBlendZoneValidatorFactory.create(),
        )

    def test_name(self) -> None:
        '''
            Verifies rule identifier name is 'timing'.
        '''
        self.assertEqual(self.rule.name, 'timing')

    def test_dead_wait_detected(self) -> None:
        '''
            Verifies DEAD_WAIT diagnostic when delay is 0.
        '''
        rule = self.rule
        instruction = ScaraInstruction(
            command_type=ScaraCommandType.WAIT_MS,
            line_number=1,
            raw_text='WAIT_MS 0',
            parameters={InstructionParam.MS: 0.0},
        )
        context = ScaraLintContext()

        diagnostics = rule.check(
            instruction=instruction,
            context=context,
        )

        codes = [d.code for d in diagnostics]
        self.assertIn(ScaraDiagnosticCode.DEAD_WAIT, codes)
        self.assertEqual(context.last_coords, ())

    def test_dwell_in_flyby_detected(self) -> None:
        '''
            Verifies TOOL_IN_FLYBY diagnostic when dwell occurs during active BLEND zone.
        '''
        rule = self.rule
        instruction = ScaraInstruction(
            command_type=ScaraCommandType.WAIT_MS,
            line_number=2,
            raw_text='WAIT_MS 100',
            parameters={InstructionParam.MS: 100.0},
        )
        context = ScaraLintContext(zone_mode=ZoneMode.BLEND, zone_radius=5.0)

        diagnostics = rule.check(
            instruction=instruction,
            context=context,
        )

        codes = [d.code for d in diagnostics]
        self.assertIn(ScaraDiagnosticCode.TOOL_IN_FLYBY, codes)

    def test_non_timing_instruction_ignored(self) -> None:
        '''
            Verifies non-WAIT_MS instruction is ignored.
        '''
        rule = self.rule
        instruction = ScaraInstruction(
            command_type=ScaraCommandType.MOVE_L,
            line_number=3,
            raw_text='MOVE_L X=10.0',
            parameters={},
        )
        context = ScaraLintContext(last_coords=(10.0, 20.0, 30.0, 0.0))

        diagnostics = rule.check(
            instruction=instruction,
            context=context,
        )

        self.assertEqual(len(diagnostics), 0)
        self.assertEqual(context.last_coords, (10.0, 20.0, 30.0, 0.0))


if __name__ == '__main__':
    main()
