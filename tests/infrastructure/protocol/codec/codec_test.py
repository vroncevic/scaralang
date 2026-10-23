# -*- coding: UTF-8 -*-

'''
Module
    codec_test.py
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
    Unit tests for BinaryFrameCodec stream codec.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.model.protocol.frame import BinaryFrame
from scaralang.core.model.protocol.message import MessageId
from scaralang.infrastructure.protocol.builder.factory import BuilderFactory
from scaralang.infrastructure.protocol.builder.provides import BuilderProvides
from scaralang.infrastructure.protocol.codec.codec import BinaryFrameCodec
from scaralang.core.service.protocol.icodec import IBinaryFrameCodec
from scaralang.infrastructure.protocol.parser.factory import ParserFactory
from scaralang.infrastructure.protocol.parser.provides import ParserProvides

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestBinaryFrameCodec(TestCase):
    '''
        Unit test suite verifying BinaryFrameCodec stream parsing and packing.

        It defines:

            :methods:
                | setUp - Initializes BinaryFrameCodec with real parser and builder.
                | test_pack_and_feed_roundtrip - Verifies serialization and parsing roundtrip.
                | test_reset - Verifies resetting decoder state.
                | test_structural_typing - Verifies instance satisfies IBinaryFrameCodec.
                | test_get_version - Verifies semantic version string.
    '''

    _codec: BinaryFrameCodec

    def setUp(self) -> None:
        '''
            Constructs BinaryFrameCodec instance before each test method.
        '''
        parser_provides: ParserProvides = ParserFactory.create()
        builder_provides: BuilderProvides = BuilderFactory.create()
        self._codec = BinaryFrameCodec(
            parser=parser_provides.parser,
            packer=builder_provides.packer,
        )

    def test_pack_and_feed_roundtrip(self) -> None:
        '''
            Verifies packing a BinaryFrame and feeding resulting bytes yields matching frame.
        '''
        builder_provides: BuilderProvides = BuilderFactory.create()
        original_frame: BinaryFrame = builder_provides.packer.build_frame(
            msg_id=MessageId.CMD_PING,
            seq_num=42,
            payload=b'\x01\x02\x03\x04',
        )
        packed_bytes: bytes = self._codec.pack_frame(frame=original_frame)
        self.assertGreater(len(packed_bytes), 0)

        frames: tuple[BinaryFrame, ...] = self._codec.feed_bytes(packed_bytes)
        self.assertEqual(len(frames), 1)
        decoded: BinaryFrame = frames[0]
        self.assertEqual(decoded.msg_id, original_frame.msg_id)
        self.assertEqual(decoded.seq_num, original_frame.seq_num)
        self.assertEqual(decoded.payload, original_frame.payload)

    def test_reset(self) -> None:
        '''
            Verifies reset clears decoder state after partial byte delivery.
        '''
        partial_data = b'\xaa\x55\x01'
        frames: tuple[BinaryFrame, ...] = self._codec.feed_bytes(partial_data)
        self.assertEqual(len(frames), 0)
        self._codec.reset()
        frames_after_reset: tuple[BinaryFrame, ...] = self._codec.feed_bytes(b'')
        self.assertEqual(len(frames_after_reset), 0)

    def test_structural_typing(self) -> None:
        '''
            Verifies BinaryFrameCodec satisfies IBinaryFrameCodec protocol.
        '''
        self.assertIsInstance(self._codec, IBinaryFrameCodec)

    def test_get_version(self) -> None:
        '''
            Verifies get_version returns a valid string.
        '''
        version: str = self._codec.get_version()
        self.assertIsInstance(version, str)
        self.assertGreater(len(version), 0)


if __name__ == '__main__':
    main()
