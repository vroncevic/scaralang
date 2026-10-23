# -*- coding: UTF-8 -*-

'''
Module
    override.py
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
    Implementation of command parser parsing OVERRIDE global speed percentage commands.
'''

from __future__ import annotations

from typing import ClassVar

from scaralang.core.model.dsl.ast.command_type import ScaraCommandType
from scaralang.core.model.dsl.ast.instruction import ScaraInstruction
from scaralang.core.model.dsl.ast.instruction_param import ScaraInstructionParam
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


class OverrideParser:
    '''
        Command parser handler for OVERRIDE speed percentage instructions.

        It defines:

            :attributes:
                | NAME - Component identification name.
                | MIN_TOKENS - Minimum allowed token count for statement parsing.
                | CMD_INDEX - Index of command token.
                | ARG_INDEX - Index of override percentage value token.
                | name - Property returning component name.
            :methods:
                | can_parse - Checks whether command is OVERRIDE.
                | parse - Parses OVERRIDE statement tokens into ScaraInstruction.
    '''

    NAME: ClassVar[str] = 'override_parser'
    MIN_TOKENS: ClassVar[int] = 2
    CMD_INDEX: ClassVar[int] = 0
    ARG_INDEX: ClassVar[int] = 1

    @property
    def name(self) -> str:
        '''
            Gets component identification name.

            :return: Component name string.
        '''
        return self.NAME

    def can_parse(self, *, command_name: str) -> bool:
        '''
            Checks if command is OVERRIDE.

            :param command_name: Command keyword string.
            :return: True if match, False otherwise.
        '''
        return command_name == ScaraCommandType.OVERRIDE

    def parse(
        self,
        *,
        tokens: tuple[ScaraToken, ...],
        line_num: int,
        raw_text: str,
    ) -> ScaraInstruction:
        '''
            Parses OVERRIDE statement into ScaraInstruction.

            :param tokens: Statement token tuple.
            :param line_num: Line number in source code.
            :param raw_text: Original statement text.
            :return: ScaraInstruction node.
            :exceptions: ScaraSyntaxError on missing or invalid override percentage argument.
        '''
        if len(tokens) < self.MIN_TOKENS:
            raise ScaraSyntaxError(
                f'Missing argument for OVERRIDE at line {line_num}'
            )

        try:
            percent_val: float = float(tokens[self.ARG_INDEX].value)

        except ValueError as exc:
            raise ScaraSyntaxError(
                f'Invalid OVERRIDE value {tokens[self.ARG_INDEX].value!r} at line {line_num}. Expected numeric'
            ) from exc

        return ScaraInstruction(
            command_type=ScaraCommandType.OVERRIDE,
            line_number=line_num,
            raw_text=raw_text,
            parameters={ScaraInstructionParam.PERCENT: percent_val},
        )
