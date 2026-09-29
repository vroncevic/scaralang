# -*- coding: UTF-8 -*-
# pylint: disable=duplicate-code

'''
Module
    scara_disassembler_test.py
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
    Unit tests for ScaraDisassembler binary frame decoding service.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.model.dsl.binary.disassembled_frame import DisassembledFrame
from scaralang.core.model.dsl.binary.disassembly_summary import DisassemblySummary
from scaralang.core.model.protocol.binary_frame import BinaryFrame
from scaralang.core.model.protocol.message_id import MessageId
from scaralang.core.service.disassembler.frame_detail_decoder_factory import FrameDetailDecoderFactory
from scaralang.core.service.disassembler.iframe_detail_decoder import IFrameDetailDecoder
from scaralang.core.service.disassembler.iscara_disassembler import IScaraDisassembler
from scaralang.core.service.disassembler.scara_disassembler import ScaraDisassembler
from scaralang.core.service.protocol.ibinary_frame_builder import IBinaryFrameBuilder
from scaralang.core.service.protocol.ibinary_frame_parser import IBinaryFrameParser
from scaralang.infrastructure.communication.protocol.binary.builder.binary_frame_builder_factory import BinaryFrameBuilderFactory
from scaralang.infrastructure.communication.protocol.binary.parser.binary_frame_parser_factory import BinaryFrameParserFactory
from scaralang.infrastructure.communication.protocol.binary.parser.binary_payload_unpacker import BinaryPayloadUnpacker

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestScaraDisassembler(TestCase):
    '''Test suite verifying ScaraDisassembler operations.'''

    def setUp(self) -> None:
        '''Initializes parser, decoder, builder, and disassembler fixtures.'''
        self.parser: IBinaryFrameParser = BinaryFrameParserFactory.create_default()
        self.unpacker: BinaryPayloadUnpacker = BinaryPayloadUnpacker()
        self.decoder: IFrameDetailDecoder = FrameDetailDecoderFactory.create(
            unpacker=self.unpacker
        )
        self.disassembler: ScaraDisassembler = ScaraDisassembler(
            parser=self.parser,
            detail_decoder=self.decoder
        )
        self.builder: IBinaryFrameBuilder = BinaryFrameBuilderFactory.create()

    def test_implements_protocol(self) -> None:
        '''Verifies structural protocol conformance.'''
        self.assertTrue(isinstance(self.disassembler, IScaraDisassembler))

    def test_disassemble_empty(self) -> None:
        '''Verifies disassembling empty data returns empty tuple.'''
        frames: tuple[DisassembledFrame, ...] = self.disassembler.disassemble(data=b'')
        self.assertEqual(frames, ())

    def test_disassemble_frame_single(self) -> None:
        '''Verifies decoding single frame directly via disassemble_frame.'''
        frame: BinaryFrame = BinaryFrame(
            msg_id=MessageId.CMD_HOME,
            seq_num=7,
            payload=b'',
            crc16=0,
        )
        result: DisassembledFrame = self.disassembler.disassemble_frame(
            frame=frame,
            index=2
        )
        self.assertEqual(result.index, 2)
        self.assertEqual(result.seq_num, 7)
        self.assertEqual(result.msg_id, int(MessageId.CMD_HOME))
        self.assertEqual(result.msg_name, 'CMD_HOME')
        self.assertEqual(result.detail, 'HOME')

    def test_disassemble_stream_bytes(self) -> None:
        '''Verifies disassembling encoded byte stream into multiple frames.'''
        home_frame_model: BinaryFrame = self.builder.build_system_cmd(
            msg_id=MessageId.CMD_HOME,
            seq_num=1
        )
        home_bytes: bytes = self.builder.pack_frame(frame=home_frame_model)

        wait_frame_model: BinaryFrame = self.builder.build_frame(
            msg_id=MessageId.CMD_WAIT,
            seq_num=2,
            payload=(250).to_bytes(4, byteorder='little')
        )
        wait_bytes: bytes = self.builder.pack_frame(frame=wait_frame_model)

        pump_frame_model: BinaryFrame = self.builder.build_tool_cmd(
            seq_num=3,
            tool_id=0,
            state=True
        )
        pump_bytes: bytes = self.builder.pack_frame(frame=pump_frame_model)

        stream: bytes = home_bytes + wait_bytes + pump_bytes
        frames: tuple[DisassembledFrame, ...] = self.disassembler.disassemble(
            data=stream
        )

        self.assertEqual(len(frames), 3)

        self.assertEqual(frames[0].index, 0)
        self.assertEqual(frames[0].seq_num, 1)
        self.assertEqual(frames[0].msg_name, 'CMD_HOME')
        self.assertEqual(frames[0].detail, 'HOME')

        self.assertEqual(frames[1].index, 1)
        self.assertEqual(frames[1].seq_num, 2)
        self.assertEqual(frames[1].msg_name, 'CMD_WAIT')
        self.assertEqual(frames[1].detail, 'WAIT 250ms')

        self.assertEqual(frames[2].index, 2)
        self.assertEqual(frames[2].seq_num, 3)
        self.assertEqual(frames[2].msg_name, 'CMD_TOOL_PUMP')
        self.assertEqual(frames[2].detail, 'PUMP ON')

    def test_calculate_summary(self) -> None:
        '''Verifies calculating disassembly summary statistics.'''
        home_frame: DisassembledFrame = DisassembledFrame(
            index=0, seq_num=1, msg_id=int(MessageId.CMD_HOME),
            msg_name='CMD_HOME', detail='HOME'
        )
        move_frame: DisassembledFrame = DisassembledFrame(
            index=1, seq_num=2, msg_id=int(MessageId.CMD_MOVE_JOINT_STEPS),
            msg_name='CMD_MOVE_JOINT_STEPS', detail='MOVE'
        )
        pump_frame: DisassembledFrame = DisassembledFrame(
            index=2, seq_num=3, msg_id=int(MessageId.CMD_TOOL_PUMP),
            msg_name='CMD_TOOL_PUMP', detail='PUMP ON'
        )
        wait_frame: DisassembledFrame = DisassembledFrame(
            index=3, seq_num=4, msg_id=int(MessageId.CMD_WAIT),
            msg_name='CMD_WAIT', detail='WAIT 250ms'
        )
        summary: DisassemblySummary = self.disassembler.calculate_summary(
            frames=(home_frame, move_frame, pump_frame, wait_frame),
            byte_count=48
        )
        self.assertEqual(summary.total_bytes, 48)
        self.assertEqual(summary.decoded_frames, 4)
        self.assertEqual(summary.motion_frames, 1)
        self.assertEqual(summary.tool_commands, 1)
        self.assertEqual(summary.wait_delays, 1)
        self.assertEqual(summary.system_frames, 1)

if __name__ == '__main__':
    main()
