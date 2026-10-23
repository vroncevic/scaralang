# -*- coding: UTF-8 -*-

'''
Module
    definition.py
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
    Implementation of command parser parsing ZONE_DEF obstacle commands.
'''

from __future__ import annotations

from typing import ClassVar

from scaralang.core.model.dsl.ast.command_type import ScaraCommandType
from scaralang.core.model.dsl.ast.instruction import ScaraInstruction
from scaralang.core.model.dsl.ast.instruction_param import ScaraInstructionParam
from scaralang.core.model.dsl.token.token import ScaraToken
from scaralang.core.model.exceptions.syntax import ScaraSyntaxError
from scaralang.core.model.trajectory.obstacle.shape import ObstacleShape
from scaralang.core.service.parser.commands.parameter.extractor import ParameterExtractor
from scaralang.core.service.parser.commands.zone.validator.ibox_validator import IBoxZoneValidator
from scaralang.core.service.parser.commands.zone.validator.icircle_validator import ICircleZoneValidator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ZoneDefParser:
    '''
        Command parser handler for obstacle zone definition instructions.

        It defines:

            :cvar NAME: Component identification name.
            :cvar MIN_TOKENS: Minimum required token count for ZONE_DEF.
            :cvar CMD_INDEX: Index of command token in tuple.
            :cvar NAME_INDEX: Index of zone name token in tuple.
            :cvar SHAPE_INDEX: Index of zone shape token in tuple.
            :cvar PARAMS_START_INDEX: Slice start index for key-value parameters.
            :cvar PARSED_COMMAND: Target command keyword string.
            :attributes:
                | _box_validator - Rectangular zone boundary validator.
                | _circle_validator - Circular zone parameter validator.
            :methods:
                | __init__ - Initializes ZoneDefParser with injected validators.
                | name - Property returning component name.
                | can_parse - Checks whether command is ZONE_DEF.
                | parse - Parses ZONE_DEF statement tokens into ScaraInstruction.
    '''

    NAME: ClassVar[str] = 'zone_def_parser'
    MIN_TOKENS: ClassVar[int] = 3
    CMD_INDEX: ClassVar[int] = 0
    NAME_INDEX: ClassVar[int] = 1
    SHAPE_INDEX: ClassVar[int] = 2
    PARAMS_START_INDEX: ClassVar[int] = 3
    PARSED_COMMAND: ClassVar[str] = ScaraCommandType.ZONE_DEF

    def __init__(
        self,
        box_validator: IBoxZoneValidator,
        circle_validator: ICircleZoneValidator,
    ) -> None:
        '''
            Initializes ZoneDefParser with injected shape validators.

            :param box_validator: Validator for rectangular obstacle zones.
            :param circle_validator: Validator for circular obstacle zones.
        '''
        self._box_validator: IBoxZoneValidator = box_validator
        self._circle_validator: ICircleZoneValidator = circle_validator

    @property
    def name(self) -> str:
        '''
            Gets component identification name.

            :return: Component name string.
        '''
        return self.NAME

    def can_parse(self, *, command_name: str) -> bool:
        '''
            Checks if command is ZONE_DEF.

            :param command_name: Command keyword string.
            :return: True if match, False otherwise.
        '''
        return command_name == self.PARSED_COMMAND

    def parse(
        self,
        *,
        tokens: tuple[ScaraToken, ...],
        line_num: int,
        raw_text: str,
    ) -> ScaraInstruction:
        '''
            Parses ZONE_DEF statement into ScaraInstruction.

            :param tokens: Statement token tuple.
            :param line_num: Line number in source code.
            :param raw_text: Original statement text.
            :return: ScaraInstruction node.
            :exceptions:
                | ScaraSyntaxError: If statement is incomplete or shape is invalid.
        '''
        if len(tokens) < self.MIN_TOKENS:
            raise ScaraSyntaxError(
                f'Incomplete ZONE_DEF statement at line {line_num}: '
                f'expected ZONE_DEF <NAME> <SHAPE> ...'
            )

        zone_name: str = tokens[self.NAME_INDEX].value.upper()
        shape_raw: str = tokens[self.SHAPE_INDEX].value.upper()

        if shape_raw not in (ObstacleShape.BOX.value, ObstacleShape.CIRCLE.value):
            raise ScaraSyntaxError(
                f'Unknown obstacle shape {shape_raw} at line {line_num}: '
                f'must be BOX or CIRCLE'
            )

        params: dict[str, object] = ParameterExtractor.extract_key_values(
            tokens=tokens[self.PARAMS_START_INDEX:]
        )
        params[ScaraInstructionParam.NAME.value] = zone_name
        params[ScaraInstructionParam.SHAPE.value] = shape_raw

        if shape_raw == ObstacleShape.BOX.value:
            self._box_validator.validate_parameters(
                params=params, line_num=line_num
            )
        elif shape_raw == ObstacleShape.CIRCLE.value:
            self._circle_validator.validate_parameters(
                params=params, line_num=line_num
            )

        return ScaraInstruction(
            command_type=self.PARSED_COMMAND,
            line_number=line_num,
            raw_text=raw_text,
            parameters=params,
        )
