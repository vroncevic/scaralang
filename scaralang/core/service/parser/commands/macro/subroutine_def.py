# -*- coding: UTF-8 -*-

'''
Module
    subroutine_def.py
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
    Implementation of command parser parsing DEF subroutine definition statements.
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


class DefParser:
    '''
        Command parser component responsible for parsing subroutine definition blocks.

        It defines:

            :attributes:
                | NAME - Parser component identification literal.
                | EXPECTED_TOKEN_COUNT - Strict required count of statement tokens.
                | name - Property accessor for parser component name.
            :methods:
                | can_parse - Validates whether keyword targets DEF instruction.
                | parse - Constructs ScaraInstruction model from statement tokens.
    '''

    NAME: ClassVar[str] = 'def_parser'
    EXPECTED_TOKEN_COUNT: ClassVar[int] = 2

    @property
    def name(self) -> str:
        '''
            Retrieves unique name identifier of definition parser.

            :return: Parser name string literal.
            :exceptions: None.
        '''
        return self.NAME

    def can_parse(self, *, command_name: str) -> bool:
        '''
            Determines whether target command keyword matches DEF directive.

            :param command_name: Raw command keyword string from source.
            :return: True if command is DEF, False otherwise.
            :exceptions: None.
        '''
        return command_name == ScaraCommandType.DEF

    def parse(
        self,
        *,
        tokens: tuple[ScaraToken, ...],
        line_num: int,
        raw_text: str,
    ) -> ScaraInstruction:
        '''
            Parses lexical tokens of DEF statement into ScaraInstruction AST node.

            :param tokens: Lexical tokens comprising the statement line.
            :param line_num: Source file line number.
            :param raw_text: Original unparsed source line text.
            :return: Instantiated ScaraInstruction AST representation.
            :exceptions:
                | ScaraSyntaxError: If token count deviates from expected syntax.
        '''
        token_count: int = len(tokens)
        if token_count != self.EXPECTED_TOKEN_COUNT:
            cmd: str = tokens[0].value.upper() if token_count > 0 else 'DEF'
            detail: str = (
                f'Missing subroutine name for {cmd} at line {line_num}'
                if token_count < self.EXPECTED_TOKEN_COUNT
                else f'Unexpected arguments for {cmd} at line {line_num}'
            )
            raise ScaraSyntaxError(detail)

        identifier: str = tokens[1].value.upper()
        return ScaraInstruction(
            command_type=ScaraCommandType.DEF,
            line_number=line_num,
            raw_text=raw_text,
            parameters={ScaraInstructionParam.NAME: identifier},
        )
