# -*- coding: UTF-8 -*-

'''
Module
    rule.py
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
from scaralang.core.model.dsl.diagnostic.diagnostic import ScaraDiagnostic
from scaralang.core.model.dsl.linter.context import LintContext
from scaralang.core.service.linter.rules.state.homing.ivalidator import IHomingValidator
from scaralang.core.service.linter.rules.state.mode.ivalidator import IModeValidator
from scaralang.core.service.linter.rules.state.zone.ivalidator import IZoneValidator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class StateLintRule:
    '''
        Lint rule updating simulation state context on HOME, ZONE, and CONFIG_MOTOR instructions.

        It defines:

            :attributes:
                | _homing_validator - IHomingValidator collaborator.
                | _zone_validator - IZoneValidator collaborator.
                | _mode_validator - IModeValidator collaborator.
            :methods:
                | name - Returns unique identifier name of the lint rule.
                | check - Updates context state for homing, zone, and motor drive mode.
    '''

    _homing_validator: IHomingValidator
    _zone_validator: IZoneValidator
    _mode_validator: IModeValidator

    def __init__(
        self,
        *,
        homing_validator: IHomingValidator,
        zone_validator: IZoneValidator,
        mode_validator: IModeValidator,
    ) -> None:
        '''
            Initializes StateLintRule with injected collaborating validators.

            :param homing_validator: Injected IHomingValidator instance.
            :param zone_validator: Injected IZoneValidator instance.
            :param mode_validator: Injected IModeValidator instance.
            :exceptions: None.
        '''
        self._homing_validator: Final[IHomingValidator] = homing_validator
        self._zone_validator: Final[IZoneValidator] = zone_validator
        self._mode_validator: Final[IModeValidator] = mode_validator

    @property
    def name(self) -> str:
        '''
            Returns the unique identifier name of the lint rule.

            :return: String identifier 'state'.
            :exceptions: None.
        '''
        return 'state'

    def check(
        self,
        *,
        instruction: ScaraInstruction,
        context: LintContext,
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
            return self._mode_validator.validate(
                instruction=instruction,
                context=context,
            )
        return ()
