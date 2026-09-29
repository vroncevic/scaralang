# -*- coding: UTF-8 -*-

'''
Module
    arc_command_parser.py
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
    Implementation of ICommandParser parsing circular ARC_CW and ARC_CCW commands.
'''

from __future__ import annotations

from scaralang.core.model.dsl.ast.command_type import ScaraCommandType
from scaralang.core.model.dsl.ast.instruction import ScaraInstruction
from scaralang.core.model.dsl.token.scara_token import ScaraToken
from scaralang.core.service.parser.commands.parameter.parameter_extractor import ParameterExtractor

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ArcCommandParser:
    '''
        Command parser handler for circular arc motion instructions.

        It defines:

            :attributes:
                | name - Identifier name of the parser.
            :methods:
                | __init__ - Initializes ArcCommandParser instance.
                | can_parse - Checks whether command is ARC_CW or ARC_CCW.
                | parse - Parses arc statement tokens into ScaraInstruction.
    '''

    def __init__(self) -> None:
        '''
            Initializes ArcCommandParser instance.
        '''

    @property
    def name(self) -> str:
        '''
            Gets the command parser identifier name.

            :return: Parser name string.
        '''
        return 'arc_command_parser'

    def can_parse(self, *, command_name: str) -> bool:
        '''
            Checks if command is ARC_CW or ARC_CCW.

            :param command_name: Command keyword string.
            :return: True if match, False otherwise.
        '''
        return command_name in (
            ScaraCommandType.ARC_CW,
            ScaraCommandType.ARC_CCW,
        )

    def parse(
        self,
        *,
        tokens: tuple[ScaraToken, ...],
        line_num: int,
        raw_text: str,
    ) -> ScaraInstruction:
        '''
            Parses circular arc statement into ScaraInstruction.

            :param tokens: Statement token tuple.
            :param line_num: Line number in source code.
            :param raw_text: Original statement text.
            :return: ScaraInstruction node.
        '''
        cmd = tokens[0].value.upper()
        cmd_type = (
            ScaraCommandType.ARC_CW
            if cmd == ScaraCommandType.ARC_CW
            else ScaraCommandType.ARC_CCW
        )
        params = ParameterExtractor.extract_key_values(tokens=tokens[1:])

        return ScaraInstruction(
            command_type=cmd_type,
            line_number=line_num,
            raw_text=raw_text,
            parameters=params,
        )
