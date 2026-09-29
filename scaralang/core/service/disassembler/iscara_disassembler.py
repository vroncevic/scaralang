# -*- coding: UTF-8 -*-

'''
Module
    iscara_disassembler.py
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
    Defines IScaraDisassembler Protocol for disassembling raw binary protocol frames.
'''

from __future__ import annotations

from typing import Protocol
from typing import runtime_checkable

from scaralang.core.model.dsl.binary.disassembled_frame import DisassembledFrame
from scaralang.core.model.dsl.binary.disassembly_summary import DisassemblySummary
from scaralang.core.model.protocol.binary_frame import BinaryFrame

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IScaraDisassembler(Protocol):
    '''
        Structural protocol defining binary frame disassembly service operations.

        It defines:

            :methods:
                | disassemble_frame - Decodes single binary frame into DisassembledFrame model.
                | disassemble - Disassembles raw binary bytes into decoded DisassembledFrame models.
                | calculate_summary - Computes DisassemblySummary domain model from decoded frames.
    '''

    def disassemble_frame(
        self,
        *,
        frame: BinaryFrame,
        index: int = 0
    ) -> DisassembledFrame:
        '''
            Decodes a single binary frame into a DisassembledFrame domain model.

            :param frame: BinaryFrame instance to disassemble.
            :param index: Sequence zero-based position index.
            :return: Decoded DisassembledFrame domain model.
            :exceptions: None.
        '''

    def disassemble(self, *, data: bytes) -> tuple[DisassembledFrame, ...]:
        '''
            Disassembles raw binary stream bytes into structured frame models.

            :param data: Contiguous binary bytes containing one or more frames.
            :return: Tuple of decoded DisassembledFrame domain models.
            :exceptions: None.
        '''

    def calculate_summary(
        self,
        *,
        frames: tuple[DisassembledFrame, ...],
        byte_count: int,
    ) -> DisassemblySummary:
        '''
            Computes a DisassemblySummary domain model from decoded frames and total bytes.

            :param frames: Decoded DisassembledFrame domain models.
            :param byte_count: Total raw bytes parsed from binary source.
            :return: Computed DisassemblySummary domain model.
            :exceptions: None.
        '''
