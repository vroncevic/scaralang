# -*- coding: UTF-8 -*-

'''
Module
    token_line_splitter.py
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
    Implementation of ITokenLineSplitter segmenting token streams into statement lines.
'''

from __future__ import annotations

from collections.abc import Sequence

from scaralang.core.model.dsl.token.scara_token import ScaraToken
from scaralang.core.model.dsl.token.scara_token_type import ScaraTokenType

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.6'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TokenLineSplitter:
    '''
        Concrete component splitting a sequence of tokens into statement lines.

        It defines:

            :attributes:
                | name - Identifier name of the splitter.
            :methods:
                | split_lines - Splits flat token sequence into statement line token tuples.
    '''

    @property
    def name(self) -> str:
        '''
            Gets the splitter identifier name.

            :return: Splitter name string.
        '''
        return 'token_line_splitter'

    def split_lines(
        self, *, tokens: Sequence[ScaraToken]
    ) -> tuple[tuple[ScaraToken, ...], ...]:
        '''
            Segments a sequence of tokens into tuples of line tokens delimited by NEWLINE or EOF.

            :param tokens: Flat sequence of ScaraToken instances.
            :return: Tuple of token tuples, each representing one logical statement line.
        '''
        lines: list[tuple[ScaraToken, ...]] = []
        current: list[ScaraToken] = []

        for token in tokens:
            if token.token_type in (ScaraTokenType.NEWLINE, ScaraTokenType.EOF):
                if current:
                    lines.append(tuple(current))
                    current.clear()
            else:
                current.append(token)

        if current:
            lines.append(tuple(current))

        return tuple(lines)
