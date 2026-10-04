# -*- coding: UTF-8 -*-

'''
Module
    binary_frame_parser.py
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
    FSM streaming parser for binary wire protocol frames.
'''

from __future__ import annotations

from typing import ClassVar
from typing import Final

from scaralang.core.model.protocol.binary_delimiter import BinaryDelimiter
from scaralang.core.model.protocol.binary_frame import BinaryFrame
from scaralang.infrastructure.communication.protocol.binary.parser.ibinary_frame_assembler import IBinaryFrameAssembler
from scaralang.infrastructure.communication.protocol.binary.parser.parser_state import ParserState

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class BinaryFrameParser:
    '''
        Stateful streaming binary frame parser with CRC-16-CCITT validation.

        It defines:

            :attributes:
                | name - Identifier name of the parser.
                | SOF1 - First start of frame byte delimiter (0xAA).
                | SOF2 - Second start of frame byte delimiter (0x55).
                | EOF - End of frame byte delimiter (0x0D).
                | MAX_PAYLOAD_LEN - Maximum supported payload byte length (64).
                | _state - Current discrete ParserState enum value.
                | _msg_id - Currently parsed message ID.
                | _seq_num - Currently parsed sequence number.
                | _payload_len - Expected payload byte length.
                | _payload_buffer - Bytearray accumulating payload.
                | _crc_bytes - Bytearray accumulating received CRC bytes.
                | _assembler - Collaborating binary frame assembler.
            :methods:
                | feed_byte - Feeds a single byte into the FSM.
                | feed_bytes - Processes contiguous bytes and yields complete frames.
                | reset - Clears state back to start of frame search.
                | get_state - Returns current FSM parser state.
    '''

    SOF1: ClassVar[int] = int(BinaryDelimiter.SOF1)
    SOF2: ClassVar[int] = int(BinaryDelimiter.SOF2)
    EOF: ClassVar[int] = int(BinaryDelimiter.EOF)
    MAX_PAYLOAD_LEN: ClassVar[int] = int(BinaryDelimiter.MAX_PAYLOAD_LEN)

    _state: ParserState
    _msg_id: int
    _seq_num: int
    _payload_len: int
    _payload_buffer: bytearray
    _crc_bytes: bytearray
    _assembler: IBinaryFrameAssembler

    def __init__(self, *, assembler: IBinaryFrameAssembler) -> None:
        '''
            Initializes parser FSM state machine, buffers, and frame assembler.

            :param assembler: Collaborating binary frame assembler and validator.
        '''
        self._state = ParserState.SEARCH_SOF1
        self._msg_id = 0
        self._seq_num = 0
        self._payload_len = 0
        self._payload_buffer = bytearray()
        self._crc_bytes = bytearray()
        self._assembler: Final[IBinaryFrameAssembler] = assembler

    @property
    def name(self) -> str:
        '''
            Gets the parser identifier name.

            :return: Parser name string.
        '''
        return 'binary_frame_parser'

    def reset(self) -> None:
        '''
            Resets parser state machine back to initial SOF search state.
        '''
        self._state = ParserState.SEARCH_SOF1
        self._payload_buffer.clear()
        self._crc_bytes.clear()

    def get_state(self) -> ParserState:
        '''
            Returns current discrete parser FSM state.

            :return: ParserState enum value.
        '''
        return self._state

    def feed_byte(self, byte: int) -> BinaryFrame | None:
        '''
            Processes a single incoming byte through the FSM.

            :param byte: Integer byte value (0 - 255).
            :return: Assembled BinaryFrame if completed and valid, None otherwise.
        '''
        safe_byte: Final[int] = byte & 0xFF
        frame: BinaryFrame | None = None

        match self._state:
            case ParserState.SEARCH_SOF1:
                if safe_byte == self.SOF1:
                    self._state = ParserState.SEARCH_SOF2

            case ParserState.SEARCH_SOF2:
                if safe_byte == self.SOF2:
                    self._state = ParserState.READ_MSG_ID
                elif safe_byte != self.SOF1:
                    self._state = ParserState.SEARCH_SOF1

            case ParserState.READ_MSG_ID:
                self._msg_id = safe_byte
                self._state = ParserState.READ_SEQ_NUM

            case ParserState.READ_SEQ_NUM:
                self._seq_num = safe_byte
                self._state = ParserState.READ_PAYLOAD_LEN

            case ParserState.READ_PAYLOAD_LEN:
                if safe_byte > self.MAX_PAYLOAD_LEN:
                    self._state = ParserState.SEARCH_SOF1
                else:
                    self._payload_len = safe_byte
                    self._payload_buffer.clear()
                    self._crc_bytes.clear()
                    self._state = (
                        ParserState.READ_CRC_LO if safe_byte == 0
                        else ParserState.READ_PAYLOAD
                    )

            case ParserState.READ_PAYLOAD:
                self._payload_buffer.append(safe_byte)
                if len(self._payload_buffer) >= self._payload_len:
                    self._state = ParserState.READ_CRC_LO

            case ParserState.READ_CRC_LO:
                self._crc_bytes.append(safe_byte)
                self._state = ParserState.READ_CRC_HI

            case ParserState.READ_CRC_HI:
                self._crc_bytes.append(safe_byte)
                self._state = ParserState.READ_EOF

            case ParserState.READ_EOF:
                self._state = ParserState.SEARCH_SOF1
                if safe_byte == self.EOF:
                    frame = self._assembler.assemble(
                        msg_id=self._msg_id,
                        seq_num=self._seq_num,
                        payload=bytes(self._payload_buffer),
                        crc_bytes=(self._crc_bytes[0], self._crc_bytes[1]),
                    )

        return frame

    def feed_bytes(self, data: bytes) -> tuple[BinaryFrame, ...]:
        '''
            Processes a block of bytes and returns all complete parsed frames.

            :param data: Contiguous input bytes.
            :return: Tuple of complete BinaryFrame instances.
        '''
        frames: list[BinaryFrame] = []

        for b in data:
            frame: BinaryFrame | None = self.feed_byte(b)

            if frame is not None:
                frames.append(frame)

        return tuple(frames)
