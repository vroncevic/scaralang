# -*- coding: UTF-8 -*-

'''
Module
    timing_lint_rule.py
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
    Validates dwell timing delays and pause compatibility with continuous blend zones.
'''

from __future__ import annotations

from typing import Final

from scaralang.core.model.dsl.ast.command_type import ScaraCommandType
from scaralang.core.model.dsl.ast.instruction import ScaraInstruction
from scaralang.core.model.dsl.diagnostic.scara_diagnostic import ScaraDiagnostic
from scaralang.core.model.dsl.linter.scara_lint_context import ScaraLintContext
from scaralang.core.service.linter.rules.timing.itiming_blend_zone_validator import ITimingBlendZoneValidator
from scaralang.core.service.linter.rules.timing.itiming_dwell_validator import ITimingDwellValidator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.6'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TimingLintRule:
    '''
        Lint rule checking for non-positive dwell delays and dwell pauses during active blend zones.

        It defines:

            :attributes:
                | _dwell_validator - ITimingDwellValidator collaborator.
                | _blend_zone_validator - ITimingBlendZoneValidator collaborator.
                | name - Unique identifier name of the lint rule.
            :methods:
                | __init__ - Initializes TimingLintRule with injected validators.
                | check - Evaluates WAIT_MS instruction against dwell parameters and blend mode.
    '''

    _dwell_validator: ITimingDwellValidator
    _blend_zone_validator: ITimingBlendZoneValidator

    def __init__(
        self,
        *,
        dwell_validator: ITimingDwellValidator,
        blend_zone_validator: ITimingBlendZoneValidator,
    ) -> None:
        '''
            Initializes TimingLintRule with injected collaborating validators.

            :param dwell_validator: Injected ITimingDwellValidator instance.
            :param blend_zone_validator: Injected ITimingBlendZoneValidator instance.
            :exceptions: None.
        '''
        self._dwell_validator: Final[ITimingDwellValidator] = dwell_validator
        self._blend_zone_validator: Final[ITimingBlendZoneValidator] = blend_zone_validator

    @property
    def name(self) -> str:
        '''
            Returns the unique identifier name of the lint rule.

            :return: String identifier 'timing'.
        '''
        return 'timing'

    def check(
        self,
        *,
        instruction: ScaraInstruction,
        context: ScaraLintContext,
    ) -> tuple[ScaraDiagnostic, ...]:
        '''
            Evaluates WAIT_MS instructions, returning non-positive delays and blend flyby conflicts.

            :param instruction: Primitive AST instruction node.
            :param context: Mutable simulation state context.
            :return: Tuple of detected ScaraDiagnostic findings.
            :exceptions: None.
        '''
        if instruction.command_type != ScaraCommandType.WAIT_MS:
            return ()

        findings: list[ScaraDiagnostic] = []
        findings.extend(
            self._dwell_validator.validate(
                instruction=instruction,
            )
        )
        findings.extend(
            self._blend_zone_validator.validate(
                instruction=instruction,
                context=context,
            )
        )
        context.last_coords = ()
        return tuple(findings)
