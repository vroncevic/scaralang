# -*- coding: UTF-8 -*-

'''
Module
    scara_decompiler.py
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
    Service decompiling binary wire frame streams into SCARA DSL source script.
'''

from __future__ import annotations

from typing import Final

from scaralang.core.model.protocol.binary_frame import BinaryFrame
from scaralang.core.service.decompiler.iframe_decompiler import IFrameDecompiler
from scaralang.core.service.protocol.ibinary_frame_parser import IBinaryFrameParser

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.7'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ScaraDecompiler:
    '''
        Service decompiling contiguous binary frame streams into SCARA DSL script text.

        It defines:

            :attributes:
                | _parser - Binary protocol frame parsing strategy.
                | _frame_decompiler - Single binary frame decompilation strategy.
            :methods:
                | __init__ - Initializes the decompiler with injected collaborators.
                | decompile - Decompiles raw binary frame bytes into SCARA DSL script.
                | decompile_bytes - Decompiles raw binary frame bytes into SCARA DSL script.
                | decompile_frames - Decompiles sequence of frames into SCARA DSL script.
                | get_version - Returns the decompiler version string.
    '''

    _parser: IBinaryFrameParser
    _frame_decompiler: IFrameDecompiler

    def __init__(
        self,
        *,
        parser: IBinaryFrameParser,
        frame_decompiler: IFrameDecompiler,
    ) -> None:
        '''
            Initializes the decompiler with frame parser and frame decompiler strategies.

            :param parser: Required IBinaryFrameParser implementation.
            :param frame_decompiler: Required IFrameDecompiler implementation.
            :exceptions: None.
        '''
        self._parser: Final[IBinaryFrameParser] = parser
        self._frame_decompiler: Final[IFrameDecompiler] = frame_decompiler

    def decompile(self, *, data: bytes) -> str:
        '''
            Decompiles contiguous raw binary frame bytes into SCARA DSL script text.

            :param data: Contiguous binary frame byte sequence.
            :return: Reconstructed SCARA DSL script source text.
            :exceptions: None.
        '''
        return self.decompile_bytes(data=data)

    def decompile_bytes(self, *, data: bytes) -> str:
        '''
            Decompiles contiguous raw binary frame bytes into SCARA DSL script text.

            :param data: Contiguous binary frame byte sequence.
            :return: Reconstructed SCARA DSL script source text.
            :exceptions: None.
        '''
        if not data:
            return ''

        frames: tuple[BinaryFrame, ...] = self._parser.feed_bytes(data)

        return self.decompile_frames(frames=frames)

    def decompile_frames(self, *, frames: tuple[BinaryFrame, ...]) -> str:
        '''
            Decompiles sequence of BinaryFrame instances into SCARA DSL script text.

            :param frames: Tuple of parsed BinaryFrame domain models.
            :return: Reconstructed SCARA DSL script source text.
            :exceptions: None.
        '''
        if not frames:
            return ''

        lines: list[str] = [
            '# SCARA DSL Script decompiled from binary stream',
            f'# Frame Count: {len(frames)}',
            '',
        ]

        for frame in frames:
            cmd: str = self._frame_decompiler.decompile_frame(frame=frame)
            if cmd:
                lines.append(cmd)

        return '\n'.join(lines)

    def get_version(self) -> str:
        '''
            Returns the decompiler version string.

            :return: Version string.
            :exceptions: None.
        '''
        return __version__
