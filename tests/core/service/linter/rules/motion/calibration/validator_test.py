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
    Unit tests for CalibrationValidator operations.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.model.dsl.ast.command_type import ScaraCommandType
from scaralang.core.model.dsl.ast.instruction import ScaraInstruction
from scaralang.core.model.dsl.diagnostic.code import ScaraDiagnosticCode
from scaralang.core.model.dsl.diagnostic.severity import ScaraDiagnosticSeverity
from scaralang.core.service.linter.context.factory import LintContextFactory
from scaralang.core.service.linter.rules.motion.calibration.validator import CalibrationValidator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestCalibrationValidator(TestCase):
    '''
        Test cases verifying CalibrationValidator behavior.

        It defines:

            :methods:
                | test_uncalibrated_motion_emits_warning - Verifies UNCALIBRATED_MOTION on unhomed move.
                | test_homed_motion_no_diagnostic - Verifies no diagnostic when robot is homed.
                | test_subsequent_motion_no_diagnostic - Verifies no warning after motion occurred.
                | test_name - Verifies validator name property.
    '''

    def test_uncalibrated_motion_emits_warning(self) -> None:
        '''
            Verifies UNCALIBRATED_MOTION diagnostic when motion occurs before homing.
        '''
        validator = CalibrationValidator()
        instruction = ScaraInstruction(
            command_type=ScaraCommandType.MOVE_L,
            line_number=5,
            raw_text='MOVE_L X=100.0 Y=50.0 Z=20.0',
            parameters={'X': 100.0, 'Y': 50.0, 'Z': 20.0},
        )
        context = LintContextFactory.create()

        diagnostics = validator.validate(
            instruction=instruction,
            context=context,
        )

        self.assertEqual(len(diagnostics), 1)
        self.assertEqual(diagnostics[0].code, ScaraDiagnosticCode.UNCALIBRATED_MOTION)
        self.assertEqual(diagnostics[0].severity, ScaraDiagnosticSeverity.WARNING)
        self.assertEqual(diagnostics[0].line, 5)

    def test_homed_motion_no_diagnostic(self) -> None:
        '''
            Verifies no diagnostic is emitted when machine is already homed.
        '''
        validator = CalibrationValidator()
        instruction = ScaraInstruction(
            command_type=ScaraCommandType.MOVE_L,
            line_number=2,
            raw_text='MOVE_L X=100.0 Y=50.0 Z=20.0',
            parameters={'X': 100.0, 'Y': 50.0, 'Z': 20.0},
        )
        context = LintContextFactory.create()
        context.is_homed = True

        diagnostics = validator.validate(
            instruction=instruction,
            context=context,
        )

        self.assertEqual(len(diagnostics), 0)

    def test_subsequent_motion_no_diagnostic(self) -> None:
        '''
            Verifies no diagnostic is emitted on subsequent motions once motion has occurred.
        '''
        validator = CalibrationValidator()
        instruction = ScaraInstruction(
            command_type=ScaraCommandType.MOVE_J,
            line_number=3,
            raw_text='MOVE_J X=120.0 Y=60.0 Z=20.0',
            parameters={'X': 120.0, 'Y': 60.0, 'Z': 20.0},
        )
        context = LintContextFactory.create()
        context.motion_occurred = True

        diagnostics = validator.validate(
            instruction=instruction,
            context=context,
        )

        self.assertEqual(len(diagnostics), 0)

    def test_name(self) -> None:
        '''
            Verifies validator name property.
        '''
        validator = CalibrationValidator()
        self.assertEqual(validator.name, 'motion_calibration')


if __name__ == '__main__':
    main()
