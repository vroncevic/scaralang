# -*- coding: UTF-8 -*-

'''
Module
    pallet_def_command_parser.py
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
    Implementation of ICommandParser parsing PALLET_DEF commands.
'''

from __future__ import annotations

from scaralang.core.model.dsl.ast.command_type import ScaraCommandType
from scaralang.core.model.dsl.ast.instruction import ScaraInstruction
from scaralang.core.model.dsl.ast.instruction_param import InstructionParam
from scaralang.core.model.dsl.token.scara_token import ScaraToken
from scaralang.core.model.exceptions.scara_syntax_error import ScaraSyntaxError
from scaralang.core.service.parser.commands.parameter.parameter_extractor import ParameterExtractor

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.5'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class PalletDefCommandParser:
    '''
        Command parser handler for matrix pallet definition instructions.

        It defines:

            :attributes:
                | _name - Component identification name.
            :methods:
                | name - Property returning component name.
                | can_parse - Checks whether command is PALLET_DEF.
                | parse - Parses PALLET_DEF statement tokens into ScaraInstruction.
    '''

    def __init__(self) -> None:
        '''Initializes PalletDefCommandParser.'''
        self._name: str = 'pallet_def_command_parser'

    @property
    def name(self) -> str:
        '''
            Gets component identification name.

            :return: Component name string.
        '''
        return self._name

    def can_parse(self, *, command_name: str) -> bool:
        '''
            Checks if command is PALLET_DEF.

            :param command_name: Command keyword string.
            :return: True if match, False otherwise.
        '''
        return command_name == ScaraCommandType.PALLET_DEF

    def parse(
        self,
        *,
        tokens: tuple[ScaraToken, ...],
        line_num: int,
        raw_text: str,
    ) -> ScaraInstruction:
        '''
            Parses PALLET_DEF statement into ScaraInstruction.

            :param tokens: Statement token tuple.
            :param line_num: Line number in source code.
            :param raw_text: Original statement text.
            :return: ScaraInstruction node.
            :exceptions: ScaraSyntaxError on missing pallet name argument.
        '''
        cmd: str = tokens[0].value.upper()

        if len(tokens) < 2:
            raise ScaraSyntaxError(
                f'Missing pallet name for {cmd} at line {line_num}'
            )

        pallet_name: str = tokens[1].value.upper()
        params: dict[str, object] = ParameterExtractor.extract_key_values(
            tokens=tokens[2:]
        )
        params[InstructionParam.NAME] = pallet_name

        return ScaraInstruction(
            command_type=ScaraCommandType.PALLET_DEF,
            line_number=line_num,
            raw_text=raw_text,
            parameters=params,
        )
