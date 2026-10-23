# -*- coding: UTF-8 -*-

'''
Module
    wait.py
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
    Implementation of command parser parsing WAIT and WAIT_MS dwell delay commands.
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


class WaitParser:
    '''
        Command parser handler for WAIT and WAIT_MS execution dwell instructions.

        It defines:

            :attributes:
                | NAME - Component identification name.
                | MIN_TOKENS - Minimum allowed token count for statement parsing.
                | CMD_INDEX - Index of command token.
                | ARG_INDEX - Index of millisecond delay value token.
                | PARSED_COMMANDS - Handled command types tuple.
                | TARGET_COMMAND - Target instruction command type.
                | name - Property returning component name.
            :methods:
                | can_parse - Checks whether command is WAIT or WAIT_MS.
                | parse - Parses WAIT statement tokens into ScaraInstruction.
    '''

    NAME: ClassVar[str] = 'wait_parser'
    MIN_TOKENS: ClassVar[int] = 2
    CMD_INDEX: ClassVar[int] = 0
    ARG_INDEX: ClassVar[int] = 1
    PARSED_COMMANDS: ClassVar[tuple[ScaraCommandType, ScaraCommandType]] = (
        ScaraCommandType.WAIT,
        ScaraCommandType.WAIT_MS,
    )
    TARGET_COMMAND: ClassVar[ScaraCommandType] = ScaraCommandType.WAIT_MS

    @property
    def name(self) -> str:
        '''
            Gets component identification name.

            :return: Component name string.
        '''
        return self.NAME

    def can_parse(self, *, command_name: str) -> bool:
        '''
            Checks if command is WAIT or WAIT_MS.

            :param command_name: Command keyword string.
            :return: True if match, False otherwise.
        '''
        return command_name in self.PARSED_COMMANDS

    def parse(
        self,
        *,
        tokens: tuple[ScaraToken, ...],
        line_num: int,
        raw_text: str,
    ) -> ScaraInstruction:
        '''
            Parses WAIT statement into ScaraInstruction.

            :param tokens: Statement token tuple.
            :param line_num: Line number in source code.
            :param raw_text: Original statement text.
            :return: ScaraInstruction node.
            :exceptions: ScaraSyntaxError on missing millisecond delay argument.
        '''
        cmd: str = tokens[self.CMD_INDEX].value.upper()

        if len(tokens) < self.MIN_TOKENS:
            raise ScaraSyntaxError(
                f'Missing millisecond argument for {cmd} at line {line_num}'
            )

        try:
            ms_val: float = float(tokens[self.ARG_INDEX].value)

        except ValueError as exc:
            raise ScaraSyntaxError(
                f'Invalid millisecond delay {tokens[self.ARG_INDEX].value!r} at line {line_num}. '
                'Must be a valid number'
            ) from exc

        params: dict[str, object] = {ScaraInstructionParam.MS: ms_val}

        return ScaraInstruction(
            command_type=self.TARGET_COMMAND,
            line_number=line_num,
            raw_text=raw_text,
            parameters=params,
        )
