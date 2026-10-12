# -*- coding: UTF-8 -*-

'''
Module
    factory_test.py
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
    Unit tests for ParserFactory.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.service.protocol.ibinary_frame_parser import IBinaryFrameParser
from scaralang.core.service.protocol.ibinary_payload_unpacker import IBinaryPayloadUnpacker
from scaralang.infrastructure.communication.protocol.binary.parser.assembler.iassembler import IBinaryFrameAssembler
from scaralang.infrastructure.communication.protocol.binary.parser.factory import ParserFactory
from scaralang.infrastructure.communication.protocol.binary.parser.parser import BinaryFrameParser
from scaralang.infrastructure.communication.protocol.binary.parser.provides import ParserProvides

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.8'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestParserFactory(TestCase):
    '''
        Test suite verifying ParserFactory instantiation and versioning.

        It defines:

            :methods:
                | test_create - Verifies ParserProvides creation.
                | test_structural_typing - Verifies instance satisfies protocol contracts.
                | test_get_version - Verifies version string retrieval.
    '''

    def test_create(self) -> None:
        '''
            Verifies factory creates a valid ParserProvides instance.
        '''
        provides: ParserProvides = ParserFactory.create()
        self.assertIsInstance(provides, ParserProvides)
        self.assertIsInstance(provides.parser, BinaryFrameParser)

    def test_structural_typing(self) -> None:
        '''
            Verifies created components satisfy structural protocols.
        '''
        provides: ParserProvides = ParserFactory.create()
        self.assertIsInstance(provides.parser, IBinaryFrameParser)
        self.assertIsInstance(provides.unpacker, IBinaryPayloadUnpacker)
        self.assertIsInstance(provides.assembler, IBinaryFrameAssembler)

    def test_get_version(self) -> None:
        '''
            Verifies factory returns a valid semantic version string.
        '''
        version: str = ParserFactory.get_version()
        self.assertIsInstance(version, str)
        self.assertGreater(len(version), 0)


if __name__ == '__main__':
    main()
