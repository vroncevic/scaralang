# -*- coding: UTF-8 -*-

'''
Module
    motion_lint_rule_test.py
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
    Unit tests for MotionLintRule operations.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.model.dsl.ast.command_type import ScaraCommandType
from scaralang.core.model.dsl.ast.instruction import ScaraInstruction
from scaralang.core.model.dsl.ast.instruction_param import InstructionParam
from scaralang.core.model.dsl.diagnostic.scara_diagnostic_code import ScaraDiagnosticCode
from scaralang.core.model.dsl.linter.scara_lint_context import ScaraLintContext
from scaralang.core.service.linter.rules.motion.motion_calibration_validator_factory import MotionCalibrationValidatorFactory
from scaralang.core.service.linter.rules.motion.motion_duplicate_validator_factory import MotionDuplicateValidatorFactory
from scaralang.core.service.linter.rules.motion.motion_lint_rule import MotionLintRule

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestMotionLintRule(TestCase):
    '''
        Test cases verifying MotionLintRule analysis and diagnostic generation.

        It defines:

            :methods:
                | setUp - Initializes MotionLintRule with injected validators.
                | test_name - Verifies rule identifier name.
                | test_non_motion_instruction_ignored - Verifies non-motion command produces no check.
                | test_uncalibrated_motion_detected - Verifies uncalibrated motion check.
                | test_duplicate_motion_detected - Verifies duplicate motion target check.
    '''

    def setUp(self) -> None:
        '''
            Sets up test MotionLintRule instance with collaborating validators.
        '''
        self.rule = MotionLintRule(
            calibration_validator=MotionCalibrationValidatorFactory.create(),
            duplicate_validator=MotionDuplicateValidatorFactory.create(),
        )

    def test_name(self) -> None:
        '''
            Verifies rule identifier name is 'motion'.
        '''
        self.assertEqual(self.rule.name, 'motion')

    def test_non_motion_instruction_ignored(self) -> None:
        '''
            Verifies non-motion commands (e.g. WAIT_MS) are ignored by MotionLintRule.
        '''
        rule = self.rule
        instruction = ScaraInstruction(
            command_type=ScaraCommandType.WAIT_MS,
            line_number=1,
            raw_text='WAIT_MS 100',
            parameters={},
        )
        context = ScaraLintContext()

        diagnostics = rule.check(
            instruction=instruction,
            context=context,
        )

        self.assertEqual(len(diagnostics), 0)
        self.assertFalse(context.motion_occurred)

    def test_uncalibrated_motion_detected(self) -> None:
        '''
            Verifies uncalibrated motion produces UNCALIBRATED_MOTION diagnostic.
        '''
        rule = self.rule
        instruction = ScaraInstruction(
            command_type=ScaraCommandType.MOVE_L,
            line_number=2,
            raw_text='MOVE_L X=100.0 Y=50.0 Z=20.0',
            parameters={
                InstructionParam.X: 100.0,
                InstructionParam.Y: 50.0,
                InstructionParam.Z: 20.0,
            },
        )
        context = ScaraLintContext(is_homed=False, motion_occurred=False)

        diagnostics = rule.check(
            instruction=instruction,
            context=context,
        )

        codes = [d.code for d in diagnostics]
        self.assertIn(ScaraDiagnosticCode.UNCALIBRATED_MOTION, codes)
        self.assertTrue(context.motion_occurred)

    def test_duplicate_motion_detected(self) -> None:
        '''
            Verifies consecutive move to identical coordinates produces DUPLICATE_MOTION.
        '''
        rule = self.rule
        instruction = ScaraInstruction(
            command_type=ScaraCommandType.MOVE_L,
            line_number=3,
            raw_text='MOVE_L X=100.0 Y=50.0 Z=20.0',
            parameters={
                InstructionParam.X: 100.0,
                InstructionParam.Y: 50.0,
                InstructionParam.Z: 20.0,
            },
        )
        context = ScaraLintContext(
            is_homed=True,
            motion_occurred=True,
            last_coords=(100.0, 50.0, 20.0, 0.0),
        )

        diagnostics = rule.check(
            instruction=instruction,
            context=context,
        )

        codes = [d.code for d in diagnostics]
        self.assertIn(ScaraDiagnosticCode.DUPLICATE_MOTION, codes)


if __name__ == '__main__':
    main()
