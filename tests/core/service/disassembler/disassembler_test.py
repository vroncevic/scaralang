# -*- coding: UTF-8 -*-

'''
Module
    disassembler_test.py
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

from unittest import TestCase, main

from scaralang.core.model.disassembler.disassembled_frame import DisassembledFrame
from scaralang.core.model.protocol.frame import BinaryFrame
from scaralang.core.model.protocol.message import MessageId
from scaralang.core.service.disassembler.disassembler import ScaraDisassembler
from scaralang.core.service.disassembler.frame.dependencies import FrameDependencies
from scaralang.core.service.disassembler.frame.factory import FrameFactory
from scaralang.core.service.disassembler.frame.provides import FrameProvides
from scaralang.core.service.disassembler.idisassembler import IScaraDisassembler
from scaralang.core.service.protocol.iactuator_builder import IBinaryActuatorFrameBuilder
from scaralang.core.service.protocol.ipacker import IBinaryFramePacker
from scaralang.core.service.protocol.iparser import IBinaryFrameParser
from scaralang.core.service.protocol.isystem_builder import IBinarySystemFrameBuilder
from scaralang.infrastructure.protocol.builder.factory import BuilderFactory
from scaralang.infrastructure.protocol.parser.factory import ParserFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestScaraDisassembler(TestCase):
    '''Test suite verifying ScaraDisassembler operations.'''

    def setUp(self) -> None:
        '''Initializes parser, decoder, builder, and disassembler fixtures.'''
        parser_provides = ParserFactory.create()
        self.parser: IBinaryFrameParser = parser_provides.parser
        frame_provides: FrameProvides = FrameFactory.create(
            dependencies=FrameDependencies(
                motion_unpacker=parser_provides.motion_unpacker,
                actuator_unpacker=parser_provides.actuator_unpacker,
            )
        )
        self.disassembler: ScaraDisassembler = ScaraDisassembler(
            parser=self.parser,
            detail_decoder=frame_provides.decoder,
        )
        builder_provides = BuilderFactory.create()
        self.packer: IBinaryFramePacker = builder_provides.packer
        self.system_builder: IBinarySystemFrameBuilder = (
            builder_provides.system
        )
        self.actuator_builder: IBinaryActuatorFrameBuilder = (
            builder_provides.actuator
        )

    def test_implements_protocol(self) -> None:
        '''
            Verifies structural protocol conformance.

            :exceptions: None.
        '''
        self.assertTrue(isinstance(self.disassembler, IScaraDisassembler))

    def test_disassemble_empty(self) -> None:
        '''
            Verifies disassembling empty data returns empty tuple.

            :exceptions: None.
        '''
        frames: tuple[DisassembledFrame, ...] = self.disassembler.disassemble(data=b'')
        self.assertEqual(frames, ())

    def test_disassemble_frame_single(self) -> None:
        '''
            Verifies decoding single frame directly via disassemble_frame.

            :exceptions: None.
        '''
        frame: BinaryFrame = BinaryFrame(
            msg_id=MessageId.CMD_HOME,
            seq_num=7,
            payload=b'',
            crc16=0,
        )
        result: DisassembledFrame = self.disassembler.disassemble_frame(
            frame=frame,
            index=2,
        )
        self.assertEqual(result.index, 2)
        self.assertEqual(result.seq_num, 7)
        self.assertEqual(result.msg_id, int(MessageId.CMD_HOME))
        self.assertEqual(result.msg_name, 'CMD_HOME')
        self.assertEqual(result.detail, 'HOME')

    def test_disassemble_stream_bytes(self) -> None:
        '''
            Verifies disassembling encoded byte stream into multiple frames.

            :exceptions: None.
        '''
        home_frame_model: BinaryFrame = self.system_builder.build_system_cmd(
            msg_id=MessageId.CMD_HOME,
            seq_num=1,
        )
        home_bytes: bytes = self.packer.pack_frame(frame=home_frame_model)

        wait_frame_model: BinaryFrame = self.packer.build_frame(
            msg_id=MessageId.CMD_WAIT,
            seq_num=2,
            payload=(250).to_bytes(4, byteorder='little'),
        )
        wait_bytes: bytes = self.packer.pack_frame(frame=wait_frame_model)

        pump_frame_model: BinaryFrame = self.actuator_builder.build_tool_cmd(
            tool_id=0,
            state=True,
            seq_num=3,
        )
        pump_bytes: bytes = self.packer.pack_frame(frame=pump_frame_model)

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

    def test_get_version(self) -> None:
        '''Verifies disassembler version string retrieval.'''
        self.assertEqual(self.disassembler.get_version(), '1.1.1')


if __name__ == '__main__':
    main()
