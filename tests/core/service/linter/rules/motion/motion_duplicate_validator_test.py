# -*- coding: UTF-8 -*-

'''
Module
    motion_duplicate_validator_test.py
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
    Unit tests for MotionDuplicateValidator operations.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.model.dsl.ast.command_type import ScaraCommandType
from scaralang.core.model.dsl.ast.instruction import ScaraInstruction
from scaralang.core.model.dsl.ast.instruction_param import InstructionParam
from scaralang.core.model.dsl.diagnostic.scara_diagnostic_code import ScaraDiagnosticCode
from scaralang.core.model.dsl.diagnostic.scara_diagnostic_severity import ScaraDiagnosticSeverity
from scaralang.core.model.dsl.linter.scara_lint_context import ScaraLintContext
from scaralang.core.service.linter.rules.motion.motion_duplicate_validator import MotionDuplicateValidator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.5'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestMotionDuplicateValidator(TestCase):
    '''
        Test cases verifying MotionDuplicateValidator duplicate detection.

        It defines:

            :methods:
                | test_consecutive_duplicate_motion_emits_info - Verifies DUPLICATE_MOTION on identical moves.
                | test_distinct_target_no_diagnostic - Verifies no diagnostic when targets differ.
                | test_non_linear_motion_clears_coords - Verifies arc/jump clears last_coords.
                | test_missing_coordinates_clears_coords - Verifies incomplete coordinates clears last_coords.
                | test_name - Verifies validator name property.
    '''

    def test_consecutive_duplicate_motion_emits_info(self) -> None:
        '''
            Verifies DUPLICATE_MOTION info diagnostic when target matches last_coords.
        '''
        validator = MotionDuplicateValidator()
        instruction = ScaraInstruction(
            command_type=ScaraCommandType.MOVE_L,
            line_number=10,
            raw_text='MOVE_L X=150.0 Y=50.0 Z=20.0 PHI=0.0',
            parameters={
                InstructionParam.X: 150.0,
                InstructionParam.Y: 50.0,
                InstructionParam.Z: 20.0,
                InstructionParam.PHI: 0.0,
            },
        )
        context = ScaraLintContext(last_coords=(150.0, 50.0, 20.0, 0.0))

        diagnostics = validator.validate(
            instruction=instruction,
            context=context,
        )

        self.assertEqual(len(diagnostics), 1)
        self.assertEqual(diagnostics[0].code, ScaraDiagnosticCode.DUPLICATE_MOTION)
        self.assertEqual(diagnostics[0].severity, ScaraDiagnosticSeverity.INFO)
        self.assertEqual(context.last_coords, (150.0, 50.0, 20.0, 0.0))

    def test_distinct_target_no_diagnostic(self) -> None:
        '''
            Verifies no diagnostic is emitted when move targets new coordinates.
        '''
        validator = MotionDuplicateValidator()
        instruction = ScaraInstruction(
            command_type=ScaraCommandType.MOVE_L,
            line_number=11,
            raw_text='MOVE_L X=160.0 Y=50.0 Z=20.0',
            parameters={
                InstructionParam.X: 160.0,
                InstructionParam.Y: 50.0,
                InstructionParam.Z: 20.0,
            },
        )
        context = ScaraLintContext(last_coords=(150.0, 50.0, 20.0, 0.0))

        diagnostics = validator.validate(
            instruction=instruction,
            context=context,
        )

        self.assertEqual(len(diagnostics), 0)
        self.assertEqual(context.last_coords, (160.0, 50.0, 20.0, 0.0))

    def test_non_linear_motion_clears_coords(self) -> None:
        '''
            Verifies non MOVE_L/MOVE_J commands reset last_coords to empty tuple.
        '''
        validator = MotionDuplicateValidator()
        instruction = ScaraInstruction(
            command_type=ScaraCommandType.ARC_CW,
            line_number=12,
            raw_text='ARC_CW X=150.0 Y=50.0 Z=20.0 R=30.0',
            parameters={
                InstructionParam.X: 150.0,
                InstructionParam.Y: 50.0,
                InstructionParam.Z: 20.0,
                InstructionParam.R: 30.0,
            },
        )
        context = ScaraLintContext(last_coords=(150.0, 50.0, 20.0, 0.0))

        diagnostics = validator.validate(
            instruction=instruction,
            context=context,
        )

        self.assertEqual(len(diagnostics), 0)
        self.assertEqual(context.last_coords, ())

    def test_missing_coordinates_clears_coords(self) -> None:
        '''
            Verifies MOVE_L without complete X/Y/Z parameters resets last_coords.
        '''
        validator = MotionDuplicateValidator()
        instruction = ScaraInstruction(
            command_type=ScaraCommandType.MOVE_L,
            line_number=13,
            raw_text='MOVE_L X=150.0',
            parameters={InstructionParam.X: 150.0},
        )
        context = ScaraLintContext(last_coords=(150.0, 50.0, 20.0, 0.0))

        diagnostics = validator.validate(
            instruction=instruction,
            context=context,
        )

        self.assertEqual(len(diagnostics), 0)
        self.assertEqual(context.last_coords, ())

    def test_name(self) -> None:
        '''
            Verifies validator name property.
        '''
        validator = MotionDuplicateValidator()
        self.assertEqual(validator.name, 'motion_duplicate')


if __name__ == '__main__':
    main()
