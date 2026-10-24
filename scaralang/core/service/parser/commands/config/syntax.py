# -*- coding: UTF-8 -*-

'''
Module
    syntax.py
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
    Syntax extraction collaborator isolating CONFIG MOTOR token unpacking.
'''

from __future__ import annotations

from typing import ClassVar

from scaralang.core.model.dsl.ast.command_type import ScaraCommandType
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


class MotorSyntaxExtractor:
    '''
        Syntax extractor isolating CONFIG MOTOR / MOTOR_MODE token unpacking.

        It defines:

            :attributes:
                | CONFIG_MIN_TOKENS - Minimum allowed token count for CONFIG MOTOR.
                | CONFIG_IFACE_TOKENS - Token count when interface parameter is supplied.
                | DIRECT_MIN_TOKENS - Minimum allowed token count for CONFIG_MOTOR / MOTOR_MODE.
                | DIRECT_IFACE_TOKENS - Direct mode token count with interface parameter.
                | CMD_INDEX - Index of command token.
                | CONFIG_SUB_INDEX - Index of configuration property subcommand token.
                | CONFIG_VAL_INDEX - Index of drive mode token in CONFIG form.
                | CONFIG_IFACE_INDEX - Index of interface type token in CONFIG form.
                | DIRECT_VAL_INDEX - Index of drive mode token in direct form.
                | DIRECT_IFACE_INDEX - Index of interface type token in direct form.
                | SUBCOMMAND_KEYWORD - Expected configuration property keyword.
                | MOTOR_MODE_COMMAND - Alternative motor mode direct command keyword.
                | DIRECT_COMMANDS - Direct motor configuration command types.
            :methods:
                | extract - Extracts raw mode and interface strings from tokens.
                | get_version - Returns the syntax extractor version string.
    '''

    CONFIG_MIN_TOKENS: ClassVar[int] = 3
    CONFIG_IFACE_TOKENS: ClassVar[int] = 4
    DIRECT_MIN_TOKENS: ClassVar[int] = 2
    DIRECT_IFACE_TOKENS: ClassVar[int] = 3
    CMD_INDEX: ClassVar[int] = 0
    CONFIG_SUB_INDEX: ClassVar[int] = 1
    CONFIG_VAL_INDEX: ClassVar[int] = 2
    CONFIG_IFACE_INDEX: ClassVar[int] = 3
    DIRECT_VAL_INDEX: ClassVar[int] = 1
    DIRECT_IFACE_INDEX: ClassVar[int] = 2
    SUBCOMMAND_KEYWORD: ClassVar[str] = 'MOTOR'
    MOTOR_MODE_COMMAND: ClassVar[str] = 'MOTOR_MODE'
    DIRECT_COMMANDS: ClassVar[tuple[ScaraCommandType, str]] = (
        ScaraCommandType.CONFIG_MOTOR,
        'MOTOR_MODE',
    )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the syntax extractor version string.

            :return: Extractor version string.
            :exceptions: None.
        '''
        return '1.1.1'

    @classmethod
    def extract(
        cls,
        *,
        tokens: tuple[ScaraToken, ...],
        line_num: int,
    ) -> tuple[str, str]:
        '''
            Extracts raw drive mode and interface strings from statement tokens.

            :param tokens: Statement token tuple.
            :param line_num: Line number in source code.
            :return: Tuple of (raw_drive_mode, raw_interface).
            :exceptions: ScaraSyntaxError on invalid token count or unknown subproperty.
        '''
        first_kw: str = tokens[cls.CMD_INDEX].value.upper()
        raw_val: str = ''
        raw_iface: str = ''

        if first_kw == ScaraCommandType.CONFIG:
            if len(tokens) < cls.CONFIG_MIN_TOKENS:
                raise ScaraSyntaxError(
                    f'Invalid CONFIG syntax at line {line_num}. '
                    'Expected: CONFIG MOTOR <OPEN_LOOP|CLOSED_LOOP> [INTERFACE]'
                )

            sub: str = tokens[cls.CONFIG_SUB_INDEX].value.upper()

            if sub != cls.SUBCOMMAND_KEYWORD:
                raise ScaraSyntaxError(
                    f'Unknown CONFIG property {sub!r} at line {line_num}'
                )

            raw_val = tokens[cls.CONFIG_VAL_INDEX].value.upper()

            if len(tokens) >= cls.CONFIG_IFACE_TOKENS:
                raw_iface = tokens[cls.CONFIG_IFACE_INDEX].value.upper()

        elif first_kw in cls.DIRECT_COMMANDS:
            if len(tokens) < cls.DIRECT_MIN_TOKENS:
                raise ScaraSyntaxError(
                    f'Invalid {first_kw} syntax at line {line_num}. '
                    f'Expected: {first_kw} <OPEN_LOOP|CLOSED_LOOP> [INTERFACE]'
                )

            raw_val = tokens[cls.DIRECT_VAL_INDEX].value.upper()

            if len(tokens) >= cls.DIRECT_IFACE_TOKENS:
                raw_iface = tokens[cls.DIRECT_IFACE_INDEX].value.upper()

        else:
            raise ScaraSyntaxError(
                f'Unexpected command {first_kw!r} for motor config at line {line_num}'
            )

        return raw_val, raw_iface
