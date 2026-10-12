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

from scaralang.core.model.dsl.ast.command_type import ScaraCommandType
from scaralang.core.model.dsl.token.scara_token import ScaraToken
from scaralang.core.model.exceptions.scara_syntax_error import ScaraSyntaxError

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.8'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class MotorSyntaxExtractor:
    '''
        Syntax extractor isolating CONFIG MOTOR / MOTOR_MODE token unpacking.

        It defines:

            :methods:
                | extract - Extracts raw mode and interface strings from tokens.
                | get_version - Returns the syntax extractor version string.
    '''

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the syntax extractor version string.

            :return: Extractor version string.
            :exceptions: None.
        '''
        return '1.0.8'

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
        first_kw: str = tokens[0].value.upper()
        raw_val: str = ''
        raw_iface: str = ''

        if first_kw == ScaraCommandType.CONFIG:
            if len(tokens) < 3:
                raise ScaraSyntaxError(
                    f'Invalid CONFIG syntax at line {line_num}. '
                    'Expected: CONFIG MOTOR <OPEN_LOOP|CLOSED_LOOP> [INTERFACE]'
                )

            sub: str = tokens[1].value.upper()

            if sub != 'MOTOR':
                raise ScaraSyntaxError(
                    f'Unknown CONFIG property {sub!r} at line {line_num}'
                )

            raw_val = tokens[2].value.upper()

            if len(tokens) >= 4:
                raw_iface = tokens[3].value.upper()

        elif first_kw in (ScaraCommandType.CONFIG_MOTOR, 'MOTOR_MODE'):
            if len(tokens) < 2:
                raise ScaraSyntaxError(
                    f'Invalid {first_kw} syntax at line {line_num}. '
                    f'Expected: {first_kw} <OPEN_LOOP|CLOSED_LOOP> [INTERFACE]'
                )

            raw_val = tokens[1].value.upper()

            if len(tokens) >= 3:
                raw_iface = tokens[2].value.upper()

        else:
            raise ScaraSyntaxError(
                f'Unexpected command {first_kw!r} for motor config at line {line_num}'
            )

        return raw_val, raw_iface
