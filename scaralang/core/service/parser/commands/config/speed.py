# -*- coding: UTF-8 -*-

'''
Module
    speed.py
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
    Implementation of command parser parsing SPEED setting commands.
'''

from __future__ import annotations

from typing import ClassVar

from scaralang.core.model.dsl.ast.command_type import ScaraCommandType
from scaralang.core.model.dsl.ast.instruction import ScaraInstruction
from scaralang.core.model.dsl.ast.instruction_param import ScaraInstructionParam
from scaralang.core.model.dsl.ast.speed_mode import SpeedMode
from scaralang.core.model.dsl.token.token import ScaraToken
from scaralang.core.model.exceptions.syntax import ScaraSyntaxError

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class SpeedParser:
    '''
        Command parser handler for SPEED mode and value setting instructions.

        It defines:

            :attributes:
                | NAME - Component identification name.
                | MIN_TOKENS - Minimum allowed token count for statement parsing.
                | CMD_INDEX - Index of command token.
                | MODE_INDEX - Index of speed mode token.
                | VAL_INDEX - Index of speed value token.
                | VALID_MODES - Supported operational speed modes.
                | name - Property returning component name.
            :methods:
                | can_parse - Checks whether command is SPEED.
                | parse - Parses SPEED statement tokens into ScaraInstruction.
    '''

    NAME: ClassVar[str] = 'speed_parser'
    MIN_TOKENS: ClassVar[int] = 3
    CMD_INDEX: ClassVar[int] = 0
    MODE_INDEX: ClassVar[int] = 1
    VAL_INDEX: ClassVar[int] = 2
    VALID_MODES: ClassVar[tuple[SpeedMode, SpeedMode]] = (
        SpeedMode.RAPID,
        SpeedMode.WORK,
    )

    @property
    def name(self) -> str:
        '''
            Gets component identification name.

            :return: Component name string.
        '''
        return self.NAME

    def can_parse(self, *, command_name: str) -> bool:
        '''
            Checks if command is SPEED.

            :param command_name: Command keyword string.
            :return: True if match, False otherwise.
        '''
        return command_name == ScaraCommandType.SPEED

    def parse(
        self,
        *,
        tokens: tuple[ScaraToken, ...],
        line_num: int,
        raw_text: str,
    ) -> ScaraInstruction:
        '''
            Parses SPEED statement into ScaraInstruction.

            :param tokens: Statement token tuple.
            :param line_num: Line number in source code.
            :param raw_text: Original statement text.
            :return: ScaraInstruction node.
            :exceptions: ScaraSyntaxError on invalid speed syntax, unknown mode, or non-numeric value.
        '''
        if len(tokens) < self.MIN_TOKENS:
            raise ScaraSyntaxError(
                f'Invalid SPEED syntax at line {line_num}. Expected: SPEED <RAPID|WORK> <val>'
            )

        mode: str = tokens[self.MODE_INDEX].value.upper()

        if mode not in self.VALID_MODES:
            raise ScaraSyntaxError(
                f'Invalid speed mode {mode!r} at line {line_num}. Expected RAPID or WORK'
            )

        try:
            val: float = float(tokens[self.VAL_INDEX].value)

        except ValueError as exc:
            raise ScaraSyntaxError(
                f'Invalid speed value {tokens[self.VAL_INDEX].value!r} at line {line_num}. Expected numeric'
            ) from exc

        return ScaraInstruction(
            command_type=ScaraCommandType.SPEED,
            line_number=line_num,
            raw_text=raw_text,
            parameters={
                ScaraInstructionParam.MODE: mode,
                ScaraInstructionParam.SPEED: val,
            },
        )
