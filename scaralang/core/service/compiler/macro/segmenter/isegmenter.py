# -*- coding: UTF-8 -*-

'''
Module
    isegmenter.py
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
    Structural protocol defining block boundary segmentation contract.
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
class ISegmenter(Protocol):
    '''
        Structural protocol defining matching block segmentation contract.

        It defines:

            :methods:
                | segment_block - Locates matching END index and extracts body instruction slice.
                | get_version - Returns segmenter component version string.
    '''

    def segment_block(
        self,
        *,
        instructions: Sequence[ScaraInstruction],
        start_index: int,
    ) -> tuple[int, tuple[ScaraInstruction, ...]]:
        '''
            Scans instruction sequence from start_index to locate matching END token.

            :param instructions: Complete sequence of AST instructions.
            :param start_index: Index of block opening instruction (DEF or REPEAT).
            :return: Tuple of index of matching END instruction and extracted body instructions.
        '''

    def get_version(self) -> str:
        '''
            Returns component version string representation.

            :return: Semantic version string.
        '''
