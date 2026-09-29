# -*- coding: UTF-8 -*-

'''
Module
    scara_token.py
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
    Defines immutable ScaraToken model representing a single lexed DSL token.
'''

from __future__ import annotations

from dataclasses import dataclass

from scaralang.core.model.dsl.token.scara_token_type import ScaraTokenType

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(frozen=True, slots=True, kw_only=True)
class ScaraToken:
    '''
        Lexed token entity.

        It defines:

            :attributes:
                | token_type - Classification type of the token.
                | value - Lexeme text or value.
                | line - Source code line number.
                | column - Source code column number.
    '''

    token_type: ScaraTokenType
    value: str
    line: int
    column: int
