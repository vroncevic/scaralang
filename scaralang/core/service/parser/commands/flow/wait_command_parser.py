# -*- coding: UTF-8 -*-

'''
Module
    wait_command_parser.py
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
    Implementation of ICommandParser parsing WAIT and WAIT_MS dwell delay commands.
'''

from __future__ import annotations

from scaralang.core.model.dsl.ast.command_type import ScaraCommandType
from scaralang.core.model.dsl.ast.instruction import ScaraInstruction
from scaralang.core.model.dsl.ast.instruction_param import InstructionParam
from scaralang.core.model.dsl.token.scara_token import ScaraToken
from scaralang.core.model.exceptions.scara_syntax_error import ScaraSyntaxError

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.7'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class WaitCommandParser:
    '''
        Command parser handler for WAIT and WAIT_MS execution dwell instructions.

        It defines:

            :attributes:
                | _name - Component identification name.
            :methods:
                | name - Property returning component name.
                | can_parse - Checks whether command is WAIT or WAIT_MS.
                | parse - Parses WAIT statement tokens into ScaraInstruction.
    '''

    def __init__(self) -> None:
        '''Initializes WaitCommandParser.'''
        self._name: str = 'wait_command_parser'

    @property
    def name(self) -> str:
        '''
            Gets component identification name.

            :return: Component name string.
        '''
        return self._name

    def can_parse(self, *, command_name: str) -> bool:
        '''
            Checks if command is WAIT or WAIT_MS.

            :param command_name: Command keyword string.
            :return: True if match, False otherwise.
        '''
        return command_name in (
            ScaraCommandType.WAIT,
            ScaraCommandType.WAIT_MS,
        )

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
        cmd: str = tokens[0].value.upper()

        if len(tokens) < 2:
            raise ScaraSyntaxError(
                f'Missing millisecond argument for {cmd} at line {line_num}'
            )

        try:
            ms_val: float = float(tokens[1].value)

        except ValueError as exc:
            raise ScaraSyntaxError(
                f'Invalid millisecond delay {tokens[1].value!r} at line {line_num}. '
                'Must be a valid number'
            ) from exc

        params: dict[str, object] = {InstructionParam.MS: ms_val}

        return ScaraInstruction(
            command_type=ScaraCommandType.WAIT_MS,
            line_number=line_num,
            raw_text=raw_text,
            parameters=params,
        )
