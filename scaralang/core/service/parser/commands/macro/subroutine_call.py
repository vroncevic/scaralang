# -*- coding: UTF-8 -*-

'''
Module
    subroutine_call.py
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
    Implementation of command parser parsing CALL subroutine invocation statements.
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
__version__ = '1.1.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class CallParser:
    '''
        Command parser handler for CALL macro subroutine invocation statements.

        It defines:

            :attributes:
                | NAME - Component identification name.
                | MIN_TOKENS - Minimum allowed token count for statement parsing.
                | MAX_TOKENS - Maximum allowed token count for statement parsing.
                | CMD_INDEX - Index of command token.
                | NAME_INDEX - Index of subroutine identifier token.
                | PARSED_COMMAND - Handled command type.
                | name - Property returning component name.
            :methods:
                | can_parse - Checks whether command is CALL.
                | parse - Parses CALL statement tokens into ScaraInstruction.
    '''

    NAME: ClassVar[str] = 'call_parser'
    MIN_TOKENS: ClassVar[int] = 2
    MAX_TOKENS: ClassVar[int] = 2
    CMD_INDEX: ClassVar[int] = 0
    NAME_INDEX: ClassVar[int] = 1
    PARSED_COMMAND: ClassVar[ScaraCommandType] = ScaraCommandType.CALL

    @property
    def name(self) -> str:
        '''
            Gets component identification name.

            :return: Component name string.
            :exceptions: None.
        '''
        return self.NAME

    def can_parse(self, *, command_name: str) -> bool:
        '''
            Checks if command is CALL.

            :param command_name: Command keyword string.
            :return: True if match, False otherwise.
            :exceptions: None.
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
            Parses CALL statement into ScaraInstruction.

            :param tokens: Statement token tuple.
            :param line_num: Line number in source code.
            :param raw_text: Original statement text.
            :return: ScaraInstruction node.
            :exceptions:
                | ScaraSyntaxError: If subroutine name is missing or invalid.
        '''
        cmd: str = tokens[self.CMD_INDEX].value.upper()

        if len(tokens) < self.MIN_TOKENS:
            raise ScaraSyntaxError(
                f'Missing subroutine name for {cmd} at line {line_num}'
            )

        if len(tokens) > self.MAX_TOKENS:
            raise ScaraSyntaxError(
                f'Unexpected arguments for {cmd} at line {line_num}'
            )

        sub_name: str = tokens[self.NAME_INDEX].value.upper()
        params: dict[str, object] = {ScaraInstructionParam.NAME: sub_name}

        return ScaraInstruction(
            command_type=self.PARSED_COMMAND,
            line_number=line_num,
            raw_text=raw_text,
            parameters=params,
        )
