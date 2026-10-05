# -*- coding: UTF-8 -*-

'''
Module
    scara_disassembler.py
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
    Service disassembling binary protocol frame bytes into structured frame models.
'''

from __future__ import annotations

from typing import Final

from scaralang.core.model.dsl.binary.disassembled_frame import DisassembledFrame
from scaralang.core.model.dsl.binary.disassembly_summary import DisassemblySummary
from scaralang.core.model.protocol.binary_frame import BinaryFrame
from scaralang.core.model.protocol.message_id import MessageId
from scaralang.core.service.disassembler.iframe_detail_decoder import IFrameDetailDecoder
from scaralang.core.service.protocol.ibinary_frame_parser import IBinaryFrameParser

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.5'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ScaraDisassembler:
    '''
        Disassembly service translating raw binary wire frames into structured models.

        It defines:

            :attributes:
                | _parser - Binary frame parsing strategy.
                | _detail_decoder - Frame payload and message name decoder strategy.
            :methods:
                | __init__ - Initializes disassembler with injected parser and detail decoder.
                | disassemble_frame - Decodes single binary frame into DisassembledFrame model.
                | disassemble - Decodes contiguous binary data into DisassembledFrame models.
    '''

    _parser: IBinaryFrameParser
    _detail_decoder: IFrameDetailDecoder

    def __init__(
        self,
        *,
        parser: IBinaryFrameParser,
        detail_decoder: IFrameDetailDecoder
    ) -> None:
        '''
            Initializes disassembler service with injected parser and detail decoder.

            :param parser: Frame parsing protocol strategy.
            :param detail_decoder: Frame payload and message name decoder strategy.
        '''
        self._parser: Final[IBinaryFrameParser] = parser
        self._detail_decoder: Final[IFrameDetailDecoder] = detail_decoder

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
        '''
        return DisassembledFrame(
            index=index,
            seq_num=frame.seq_num,
            msg_id=int(frame.msg_id),
            msg_name=self._detail_decoder.decode_msg_name(msg_id=int(frame.msg_id)),
            detail=self._detail_decoder.decode_detail(frame=frame),
        )

    def disassemble(self, *, data: bytes) -> tuple[DisassembledFrame, ...]:
        '''
            Disassembles raw binary stream bytes into structured frame models.

            :param data: Contiguous binary bytes containing one or more frames.
            :return: Tuple of decoded DisassembledFrame domain models.
        '''
        frames: tuple[BinaryFrame, ...] = self._parser.feed_bytes(data)

        return tuple(
            self.disassemble_frame(frame=frame, index=i)
            for i, frame in enumerate(frames)
        )

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
        '''
        motion_count = sum(
            1 for item in frames
            if item.msg_id in (
                MessageId.CMD_MOVE_JOINT_STEPS,
                MessageId.CMD_JOG_JOINT,
                MessageId.CMD_SETPOS_STEPS,
            )
        )
        tool_count = sum(
            1 for item in frames
            if item.msg_id in (
                MessageId.CMD_TOOL_PUMP,
                MessageId.CMD_TOOL_VALVE,
            )
        )
        wait_count = sum(
            1 for item in frames
            if item.msg_id == MessageId.CMD_WAIT
        )
        system_count = len(frames) - motion_count - tool_count - wait_count

        return DisassemblySummary(
            total_bytes=byte_count,
            decoded_frames=len(frames),
            motion_frames=motion_count,
            tool_commands=tool_count,
            wait_delays=wait_count,
            system_frames=system_count,
        )

    def get_version(self) -> str:
        '''
            Returns the disassembler version string.

            :return: Version string.
            :exceptions: None.
        '''
        return __version__
