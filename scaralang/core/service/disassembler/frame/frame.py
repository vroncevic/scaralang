# -*- coding: UTF-8 -*-

'''
Module
    frame.py
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
    Defines FrameDetailDecoder decoding binary wire frame payloads and symbolic message names.
'''

from __future__ import annotations

from typing import Final

from scaralang.core.model.protocol.frame import BinaryFrame
from scaralang.core.model.protocol.message import MessageId
from scaralang.core.service.disassembler.frame.decoder.idecoder import IFramePayloadDecoder

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class FrameDetailDecoder:
    '''
        Decodes wire protocol frame payloads into structured, human-readable representations.

        It defines:

            :attributes:
                | _decoders - Injected tuple of specialized payload decoders.
            :methods:
                | __init__ - Initializes decoder with injected payload decoders.
                | decode_msg_name - Returns symbolic message identifier name.
                | decode_detail - Routes frame to specialized payload decoder.
                | get_version - Returns decoder version string.
    '''

    _decoders: tuple[IFramePayloadDecoder, ...]

    def __init__(
        self, *, decoders: tuple[IFramePayloadDecoder, ...]
    ) -> None:
        '''
            Initializes FrameDetailDecoder with injected payload decoders.

            :param decoders: Tuple of IFramePayloadDecoder protocol instances.
            :exceptions: None.
        '''
        self._decoders: Final[tuple[IFramePayloadDecoder, ...]] = decoders

    def decode_msg_name(self, *, msg_id: int) -> str:
        '''
            Decodes integer message identifier into symbolic enum name.

            :param msg_id: Numeric message identifier.
            :return: Symbolic name string or UNKNOWN.
            :exceptions: None.
        '''
        try:
            return MessageId(msg_id).name

        except ValueError:
            return 'UNKNOWN'

    def decode_detail(self, *, frame: BinaryFrame) -> str:
        '''
            Dispatches binary frame to matching payload decoder.

            :param frame: BinaryFrame instance to decode.
            :return: Human-readable decoded detail string.
            :exceptions: None.
        '''
        msg_id: int = int(frame.msg_id)

        for decoder in self._decoders:
            if decoder.can_decode(msg_id=msg_id):
                return decoder.decode(frame=frame)

        return f'payload={frame.payload.hex()}' if frame.payload else ''

    def get_version(self) -> str:
        '''
            Returns the decoder version string representation.

            :return: Decoder version string.
            :exceptions: None.
        '''
        return __version__
