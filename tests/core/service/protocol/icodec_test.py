# -*- coding: UTF-8 -*-

'''
Module
    icodec_test.py
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
    Unit tests for IBinaryFrameCodec protocol compliance.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.model.protocol.frame import BinaryFrame
from scaralang.core.model.protocol.message import MessageId
from scaralang.core.service.protocol.icodec import IBinaryFrameCodec
from scaralang.infrastructure.protocol.builder.factory import BuilderFactory
from scaralang.infrastructure.protocol.builder.provides import BuilderProvides
from scaralang.infrastructure.protocol.codec.dependencies import CodecDependencies
from scaralang.infrastructure.protocol.codec.factory import CodecFactory
from scaralang.infrastructure.protocol.parser.factory import ParserFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestIBinaryFrameCodec(TestCase):
    '''
        Test cases verifying IBinaryFrameCodec structural subtyping.

        It defines:

            :methods:
                | setUp - Initializes codec fixture satisfying protocol.
                | test_structural_compliance - Verifies codec satisfies protocol.
                | test_pack_and_feed_roundtrip - Verifies frame packing and feed decoding.
                | test_reset_and_version - Verifies decoder reset and version retrieval.
    '''

    def setUp(self) -> None:
        '''Sets up codec fixture through CodecFactory.'''
        parser_provides = ParserFactory.create()
        builder_provides = BuilderFactory.create()
        deps = CodecDependencies(
            parser=parser_provides.parser,
            packer=builder_provides.packer,
        )
        self.codec: IBinaryFrameCodec = CodecFactory.create(dependencies=deps).codec

    def test_structural_compliance(self) -> None:
        '''Verifies instance satisfies IBinaryFrameCodec structural protocol.'''
        self.assertIsInstance(self.codec, IBinaryFrameCodec)

    def test_pack_and_feed_roundtrip(self) -> None:
        '''Verifies packing a frame and feeding bytes back produces valid frames.'''
        builder_provides: BuilderProvides = BuilderFactory.create()
        frame: BinaryFrame = builder_provides.packer.build_frame(
            msg_id=MessageId.CMD_PING,
            seq_num=1,
            payload=b'',
        )
        packed: bytes = self.codec.pack_frame(frame)
        self.assertIsInstance(packed, bytes)
        self.assertTrue(len(packed) > 0)
        frames: tuple[BinaryFrame, ...] = self.codec.feed_bytes(packed)
        self.assertEqual(len(frames), 1)
        self.assertEqual(frames[0].msg_id, MessageId.CMD_PING)

    def test_reset_and_version(self) -> None:
        '''Verifies reset clears decoder state and get_version returns string.'''
        self.codec.reset()
        version: str = self.codec.get_version()
        self.assertIsInstance(version, str)
        self.assertTrue(len(version) > 0)


if __name__ == '__main__':
    main()
