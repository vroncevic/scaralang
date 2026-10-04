# -*- coding: UTF-8 -*-

'''
Module
    iscara_decompiler.py
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
    Defines structural protocol IScaraDecompiler for binary wire decompilation into DSL.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from scaralang.core.model.protocol.binary_frame import BinaryFrame

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IScaraDecompiler(Protocol):
    '''
        Structural protocol defining binary wire stream decompilation into SCARA DSL script.

        It defines:

            :methods:
                | decompile_bytes - Decompiles raw binary bytes into SCARA DSL script text.
                | decompile_frames - Decompiles tuple of BinaryFrames into SCARA DSL script text.
                | get_version - Returns decompiler version string.
    '''

    def decompile_bytes(self, *, data: bytes) -> str:
        '''
            Decompiles contiguous raw binary frame bytes into SCARA DSL script text.

            :param data: Contiguous binary frame byte sequence.
            :return: Reconstructed SCARA DSL script source text.
        '''

    def decompile_frames(self, *, frames: tuple[BinaryFrame, ...]) -> str:
        '''
            Decompiles sequence of BinaryFrame instances into SCARA DSL script text.

            :param frames: Tuple of parsed BinaryFrame domain models.
            :return: Reconstructed SCARA DSL script source text.
        '''

    def get_version(self) -> str:
        '''
            Returns the decompiler version string representation.

            :return: Semantic version string.
        '''
