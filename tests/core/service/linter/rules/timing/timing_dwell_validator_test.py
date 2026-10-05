# -*- coding: UTF-8 -*-

'''
Module
    timing_dwell_validator_test.py
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
    Unit tests for TimingDwellValidator operations.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.model.dsl.ast.command_type import ScaraCommandType
from scaralang.core.model.dsl.ast.instruction import ScaraInstruction
from scaralang.core.model.dsl.ast.instruction_param import InstructionParam
from scaralang.core.model.dsl.diagnostic.scara_diagnostic_code import ScaraDiagnosticCode
from scaralang.core.model.dsl.diagnostic.scara_diagnostic_severity import ScaraDiagnosticSeverity
from scaralang.core.service.linter.rules.timing.timing_dwell_validator import TimingDwellValidator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestTimingDwellValidator(TestCase):
    '''
        Test cases verifying TimingDwellValidator operations.

        It defines:

            :methods:
                | test_zero_delay_emits_dead_wait_info - Verifies zero delay produces DEAD_WAIT.
                | test_negative_delay_emits_dead_wait_info - Verifies negative delay produces DEAD_WAIT.
                | test_positive_delay_no_diagnostic - Verifies positive delay is accepted cleanly.
                | test_non_wait_command_no_op - Verifies other commands are ignored.
                | test_name - Verifies validator name property.
    '''

    def test_zero_delay_emits_dead_wait_info(self) -> None:
        '''
            Verifies DEAD_WAIT diagnostic when delay is 0 ms.
        '''
        validator = TimingDwellValidator()
        instruction = ScaraInstruction(
            command_type=ScaraCommandType.WAIT_MS,
            line_number=5,
            raw_text='WAIT_MS 0',
            parameters={InstructionParam.MS: 0.0},
        )

        diagnostics = validator.validate(instruction=instruction)

        self.assertEqual(len(diagnostics), 1)
        self.assertEqual(diagnostics[0].code, ScaraDiagnosticCode.DEAD_WAIT)
        self.assertEqual(diagnostics[0].severity, ScaraDiagnosticSeverity.INFO)
        self.assertEqual(diagnostics[0].line, 5)

    def test_negative_delay_emits_dead_wait_info(self) -> None:
        '''
            Verifies DEAD_WAIT diagnostic when delay is negative.
        '''
        validator = TimingDwellValidator()
        instruction = ScaraInstruction(
            command_type=ScaraCommandType.WAIT_MS,
            line_number=6,
            raw_text='WAIT_MS -50',
            parameters={InstructionParam.MS: -50.0},
        )

        diagnostics = validator.validate(instruction=instruction)

        self.assertEqual(len(diagnostics), 1)
        self.assertEqual(diagnostics[0].code, ScaraDiagnosticCode.DEAD_WAIT)
        self.assertEqual(diagnostics[0].severity, ScaraDiagnosticSeverity.INFO)

    def test_positive_delay_no_diagnostic(self) -> None:
        '''
            Verifies positive dwell delay produces no diagnostic findings.
        '''
        validator = TimingDwellValidator()
        instruction = ScaraInstruction(
            command_type=ScaraCommandType.WAIT_MS,
            line_number=7,
            raw_text='WAIT_MS 250',
            parameters={InstructionParam.MS: 250.0},
        )

        diagnostics = validator.validate(instruction=instruction)

        self.assertEqual(len(diagnostics), 0)

    def test_non_wait_command_no_op(self) -> None:
        '''
            Verifies non-WAIT_MS command is ignored.
        '''
        validator = TimingDwellValidator()
        instruction = ScaraInstruction(
            command_type=ScaraCommandType.HOME,
            line_number=8,
            raw_text='HOME',
            parameters={},
        )

        diagnostics = validator.validate(instruction=instruction)

        self.assertEqual(len(diagnostics), 0)

    def test_name(self) -> None:
        '''
            Verifies validator name property.
        '''
        validator = TimingDwellValidator()
        self.assertEqual(validator.name, 'timing_dwell')


if __name__ == '__main__':
    main()
