# -*- coding: UTF-8 -*-

'''
Module
    state_lint_rule.py
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
    Tracks homing state and blend zone configurations during DSL static analysis.
'''

from __future__ import annotations

from typing import Final

from scaralang.core.model.dsl.ast.command_type import ScaraCommandType
from scaralang.core.model.dsl.ast.instruction import ScaraInstruction
from scaralang.core.model.dsl.diagnostic.scara_diagnostic import ScaraDiagnostic
from scaralang.core.model.dsl.linter.scara_lint_context import ScaraLintContext
from scaralang.core.service.linter.rules.state.imotor_mode_validator import IMotorModeValidator
from scaralang.core.service.linter.rules.state.istate_homing_validator import IStateHomingValidator
from scaralang.core.service.linter.rules.state.istate_zone_validator import IStateZoneValidator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class StateLintRule:
    '''
        Lint rule updating simulation state context on HOME, ZONE, and CONFIG_MOTOR instructions.

        It defines:

            :attributes:
                | _homing_validator - IStateHomingValidator collaborator.
                | _zone_validator - IStateZoneValidator collaborator.
                | _motor_mode_validator - IMotorModeValidator collaborator.
                | name - Unique identifier name of the lint rule.
            :methods:
                | __init__ - Initializes StateLintRule with injected validators.
                | check - Updates context state for homing, zone, and motor drive mode.
    '''

    _homing_validator: IStateHomingValidator
    _zone_validator: IStateZoneValidator
    _motor_mode_validator: IMotorModeValidator

    def __init__(
        self,
        *,
        homing_validator: IStateHomingValidator,
        zone_validator: IStateZoneValidator,
        motor_mode_validator: IMotorModeValidator,
    ) -> None:
        '''
            Initializes StateLintRule with injected collaborating validators.

            :param homing_validator: Injected IStateHomingValidator instance.
            :param zone_validator: Injected IStateZoneValidator instance.
            :param motor_mode_validator: Injected IMotorModeValidator instance.
            :exceptions: None.
        '''
        self._homing_validator: Final[IStateHomingValidator] = homing_validator
        self._zone_validator: Final[IStateZoneValidator] = zone_validator
        self._motor_mode_validator: Final[IMotorModeValidator] = motor_mode_validator

    @property
    def name(self) -> str:
        '''
            Returns the unique identifier name of the lint rule.

            :return: String identifier 'state'.
        '''
        return 'state'

    def check(
        self,
        *,
        instruction: ScaraInstruction,
        context: ScaraLintContext,
    ) -> tuple[ScaraDiagnostic, ...]:
        '''
            Evaluates homing, zone, and motor configuration instructions, updating context.

            :param instruction: Primitive AST instruction node.
            :param context: Mutable simulation state context.
            :return: Tuple of detected ScaraDiagnostic findings.
            :exceptions: None.
        '''
        cmd = instruction.command_type

        if cmd == ScaraCommandType.HOME:
            self._homing_validator.validate(
                instruction=instruction,
                context=context,
            )
            return ()
        if cmd == ScaraCommandType.ZONE:
            return self._zone_validator.validate(
                instruction=instruction,
                context=context,
            )
        if cmd == ScaraCommandType.CONFIG_MOTOR:
            return self._motor_mode_validator.validate(
                instruction=instruction,
                context=context,
            )
        return ()
