# -*- coding: UTF-8 -*-

'''
Module
    override_config_parser.py
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
    Implementation of ICommandParser parsing OVERRIDE global speed percentage commands.
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
__version__ = '1.0.6'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class OverrideConfigParser:
    '''
        Command parser handler for OVERRIDE speed percentage instructions.

        It defines:

            :attributes:
                | _name - Component identification name.
            :methods:
                | name - Property returning component name.
                | can_parse - Checks whether command is OVERRIDE.
                | parse - Parses OVERRIDE statement tokens into ScaraInstruction.
    '''

    def __init__(self) -> None:
        '''Initializes OverrideConfigParser.'''
        self._name: str = 'override_config_parser'

    @property
    def name(self) -> str:
        '''
            Gets component identification name.

            :return: Component name string.
        '''
        return self._name

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
        if len(tokens) < 2:
            raise ScaraSyntaxError(
                f'Missing argument for OVERRIDE at line {line_num}'
            )

        try:
            percent_val: float = float(tokens[1].value)

        except ValueError as exc:
            raise ScaraSyntaxError(
                f'Invalid OVERRIDE value {tokens[1].value!r} at line {line_num}. Expected numeric'
            ) from exc

        return ScaraInstruction(
            command_type=ScaraCommandType.OVERRIDE,
            line_number=line_num,
            raw_text=raw_text,
            parameters={InstructionParam.PERCENT: percent_val,},
        )
