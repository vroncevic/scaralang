# -*- coding: UTF-8 -*-

'''
Module
    iparser_test.py
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
    Unit tests for IBinaryFrameParser protocol compliance.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.model.protocol.message import MessageId
from scaralang.core.service.protocol.iparser import IBinaryFrameParser
from scaralang.infrastructure.protocol.builder.packer import BinaryFramePacker
from scaralang.infrastructure.protocol.parser.factory import ParserFactory
from scaralang.infrastructure.protocol.parser.parser import BinaryFrameParser

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestIBinaryFrameParser(TestCase):
    '''
        Test cases verifying IBinaryFrameParser structural subtyping.

        It defines:

            :methods:
                | test_structural_compliance - Verifies parser satisfies protocol.
                | test_name_property - Verifies name property returns expected identifier.
                | test_feed_bytes_and_reset - Verifies streaming decoding and parser reset.
    '''

    def test_structural_compliance(self) -> None:
        '''
            Verifies that factory creates an instance satisfying IBinaryFrameParser.

            :exceptions: None.
        '''
        parser = ParserFactory.create().parser
        self.assertIsInstance(parser, IBinaryFrameParser)

    def test_name_property(self) -> None:
        '''
            Verifies that name property returns expected identifier.

            :exceptions: None.
        '''
        parser = ParserFactory.create().parser
        self.assertEqual(parser.name, 'binary_frame_parser')

    def test_feed_bytes_and_reset(self) -> None:
        '''
            Verifies streaming frame decoding and state reset via protocol contract.

            :exceptions: None.
        '''
        packer = BinaryFramePacker()
        parser = BinaryFrameParser(
            assembler=ParserFactory.create().assembler
        )

        frame = packer.build_frame(msg_id=MessageId.CMD_HOME, seq_num=5)
        wire_bytes = packer.pack_frame(frame=frame)

        parsed_frames = parser.feed_bytes(data=wire_bytes)
        self.assertEqual(len(parsed_frames), 1)
        self.assertEqual(parsed_frames[0].msg_id, MessageId.CMD_HOME)
        self.assertEqual(parsed_frames[0].seq_num, 5)

        parser.reset()


if __name__ == '__main__':
    main()
