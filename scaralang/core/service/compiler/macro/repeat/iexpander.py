# -*- coding: UTF-8 -*-

'''
Module
    iexpander.py
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
    Structural protocol defining repeat loop macro expander contract.
'''

from __future__ import annotations

from collections.abc import Sequence
from typing import Protocol, runtime_checkable

from scaralang.core.model.dsl.ast.instruction import ScaraInstruction

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IRepeatExpander(Protocol):
    '''
        Structural protocol defining repeat loop unrolling contract.

        It defines:

            :methods:
                | expand_repeats - Unrolls repeat loops into linear instruction stream.
                | get_version - Returns expander component version string.
    '''

    def expand_repeats(
        self,
        *,
        instructions: Sequence[ScaraInstruction],
    ) -> tuple[ScaraInstruction, ...]:
        '''
            Unrolls repeat loops into a linear instruction sequence.

            :param instructions: Input sequence of parsed AST instructions.
            :return: Linear sequence of fully expanded instructions.
        '''

    def get_version(self) -> str:
        '''
            Returns component version string representation.

            :return: Semantic version string.
        '''
