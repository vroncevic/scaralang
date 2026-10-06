# -*- coding: UTF-8 -*-

'''
Module
    motion_lint_rule.py
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
    Validates calibration prerequisites and duplicate moves for motion instructions.
'''

from __future__ import annotations

from typing import Final

from scaralang.core.model.dsl.ast.command_type import ScaraCommandType
from scaralang.core.model.dsl.ast.instruction import ScaraInstruction
from scaralang.core.model.dsl.diagnostic.scara_diagnostic import ScaraDiagnostic
from scaralang.core.model.dsl.linter.scara_lint_context import ScaraLintContext
from scaralang.core.service.linter.rules.motion.imotion_calibration_validator import IMotionCalibrationValidator
from scaralang.core.service.linter.rules.motion.imotion_duplicate_validator import IMotionDuplicateValidator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.6'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class MotionLintRule:
    '''
        Lint rule checking for uncalibrated moves and consecutive duplicate targets.

        It defines:

            :attributes:
                | _MOTION_COMMANDS - Frozenset of instructions representing robot motion.
                | _calibration_validator - IMotionCalibrationValidator collaborator.
                | _duplicate_validator - IMotionDuplicateValidator collaborator.
                | name - Unique identifier name of the lint rule.
            :methods:
                | __init__ - Initializes MotionLintRule with injected validators.
                | check - Analyzes motion instruction against current simulation context.
    '''

    _MOTION_COMMANDS: frozenset[ScaraCommandType] = frozenset({
        ScaraCommandType.MOVE_L,
        ScaraCommandType.MOVE_J,
        ScaraCommandType.ARC_CW,
        ScaraCommandType.ARC_CCW,
        ScaraCommandType.JUMP,
        ScaraCommandType.APPROACH,
        ScaraCommandType.RETRACT,
        ScaraCommandType.MOVE_PALLET,
    })

    _calibration_validator: IMotionCalibrationValidator
    _duplicate_validator: IMotionDuplicateValidator

    def __init__(
        self,
        *,
        calibration_validator: IMotionCalibrationValidator,
        duplicate_validator: IMotionDuplicateValidator,
    ) -> None:
        '''
            Initializes MotionLintRule with injected collaborating validators.

            :param calibration_validator: Injected IMotionCalibrationValidator instance.
            :param duplicate_validator: Injected IMotionDuplicateValidator instance.
            :exceptions: None.
        '''
        self._calibration_validator: Final[IMotionCalibrationValidator] = calibration_validator
        self._duplicate_validator: Final[IMotionDuplicateValidator] = duplicate_validator

    @property
    def name(self) -> str:
        '''
            Returns the unique identifier name of the lint rule.

            :return: String identifier 'motion'.
        '''
        return 'motion'

    def check(
        self,
        *,
        instruction: ScaraInstruction,
        context: ScaraLintContext,
    ) -> tuple[ScaraDiagnostic, ...]:
        '''
            Evaluates motion calibration and duplicate move findings.

            :param instruction: Primitive AST instruction node.
            :param context: Mutable simulation state context.
            :return: Tuple of detected ScaraDiagnostic findings.
            :exceptions: None.
        '''
        if instruction.command_type not in self._MOTION_COMMANDS:
            return ()

        findings: list[ScaraDiagnostic] = []
        findings.extend(
            self._calibration_validator.validate(
                instruction=instruction,
                context=context,
            )
        )
        findings.extend(
            self._duplicate_validator.validate(
                instruction=instruction,
                context=context,
            )
        )
        context.motion_occurred = True
        return tuple(findings)
