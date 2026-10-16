# -*- coding: UTF-8 -*-

'''
Module
    zone.py
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
    Implementation of command parser parsing corner path blending ZONE instructions.
'''

from __future__ import annotations

from typing import ClassVar

from scaralang.core.model.dsl.ast.command_type import ScaraCommandType
from scaralang.core.model.dsl.ast.instruction import ScaraInstruction
from scaralang.core.model.dsl.ast.instruction_param import ScaraInstructionParam
from scaralang.core.model.dsl.ast.zone_mode import ZoneMode
from scaralang.core.model.dsl.token.scara_token import ScaraToken
from scaralang.core.model.exceptions.scara_syntax_error import ScaraSyntaxError
from scaralang.core.service.parser.commands.parameter.extractor import ParameterExtractor

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.9'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ZoneParser:
    '''
        Command parser handler for corner path blending ZONE instructions.

        It defines:

            :attributes:
                | NAME - Component identification name.
                | MIN_TOKENS - Minimum allowed token count for statement parsing.
                | CMD_INDEX - Index of command token.
                | MODE_INDEX - Index of zone mode token.
                | PARAMS_START_INDEX - Slice start index for key-value parameters.
                | DEFAULT_BLEND_RADIUS - Fallback radius value when unspecified.
                | name - Property returning component name.
            :methods:
                | can_parse - Checks whether command is ZONE.
                | parse - Parses zone statement tokens into ScaraInstruction.
    '''

    NAME: ClassVar[str] = 'zone_parser'
    MIN_TOKENS: ClassVar[int] = 2
    CMD_INDEX: ClassVar[int] = 0
    MODE_INDEX: ClassVar[int] = 1
    PARAMS_START_INDEX: ClassVar[int] = 2
    DEFAULT_BLEND_RADIUS: ClassVar[float] = 5.0

    @property
    def name(self) -> str:
        '''
            Gets component identification name.

            :return: Component name string.
        '''
        return self.NAME

    def can_parse(self, *, command_name: str) -> bool:
        '''
            Checks if command is ZONE.

            :param command_name: Command keyword string.
            :return: True if match, False otherwise.
        '''
        return command_name == ScaraCommandType.ZONE

    def parse(
        self,
        *,
        tokens: tuple[ScaraToken, ...],
        line_num: int,
        raw_text: str,
    ) -> ScaraInstruction:
        '''
            Parses zone statement into ScaraInstruction.

            :param tokens: Statement token tuple.
            :param line_num: Line number in source code.
            :param raw_text: Original statement text.
            :return: ScaraInstruction node.
            :exceptions: ScaraSyntaxError on invalid zone mode.
        '''
        if len(tokens) < self.MIN_TOKENS:
            raise ScaraSyntaxError(
                f'Invalid ZONE syntax at line {line_num}. '
                'Expected: ZONE FINE or ZONE BLEND R=<radius>'
            )

        mode: str = tokens[self.MODE_INDEX].value.upper()
        params: dict[str, object] = {ScaraInstructionParam.MODE: mode}

        if mode == ZoneMode.BLEND:
            sub_params: dict[str, object] = ParameterExtractor.extract_key_values(
                tokens=tokens[self.PARAMS_START_INDEX:]
            )
            radius_val: object = sub_params.get(ScaraInstructionParam.R)

            if radius_val is None:
                radius_val = sub_params.get(
                    ScaraInstructionParam.RADIUS, self.DEFAULT_BLEND_RADIUS
                )

            params[ScaraInstructionParam.RADIUS] = radius_val

        return ScaraInstruction(
            command_type=ScaraCommandType.ZONE,
            line_number=line_num,
            raw_text=raw_text,
            parameters=params,
        )
