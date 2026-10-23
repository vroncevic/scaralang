# -*- coding: UTF-8 -*-

'''
Module
    response_test.py
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
    Unit tests for BinaryResponsePayloadUnpacker implementation.
'''

from __future__ import annotations

from struct import pack
from unittest import TestCase, main

from scaralang.core.model.exceptions.protocol import ScaraProtocolError
from scaralang.infrastructure.protocol.parser.unpacker.response import BinaryResponsePayloadUnpacker
from scaralang.infrastructure.protocol.struct_format import BinaryStructFormat

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestBinaryResponsePayloadUnpacker(TestCase):
    '''
        Test cases verifying BinaryResponsePayloadUnpacker implementation.

        It defines:

            :methods:
                | test_unpack_ack - Verifies ACK deserialization.
                | test_unpack_nack - Verifies NACK deserialization.
                | test_get_version - Verifies version string retrieval.
    '''

    def test_unpack_ack(self) -> None:
        '''
            Verifies ACK deserialization.

            :exceptions: None.
        '''
        unpacker = BinaryResponsePayloadUnpacker()
        raw_payload = pack(str(BinaryStructFormat.ACK), 5, 2)
        msg_id, queue_depth = unpacker.unpack_ack(data=raw_payload)
        self.assertEqual(msg_id, 5)
        self.assertEqual(queue_depth, 2)

        with self.assertRaises(ScaraProtocolError):
            unpacker.unpack_ack(data=b'')

    def test_unpack_nack(self) -> None:
        '''
            Verifies NACK deserialization.

            :exceptions: None.
        '''
        unpacker = BinaryResponsePayloadUnpacker()
        raw_payload = pack(str(BinaryStructFormat.NACK), 12, 1)
        msg_id, error_code = unpacker.unpack_nack(data=raw_payload)
        self.assertEqual(msg_id, 12)
        self.assertEqual(error_code, 1)

        with self.assertRaises(ScaraProtocolError):
            unpacker.unpack_nack(data=b'')

    def test_get_version(self) -> None:
        '''
            Verifies semantic version string retrieval.

            :exceptions: None.
        '''
        unpacker = BinaryResponsePayloadUnpacker()
        version: str = unpacker.get_version()
        self.assertIsInstance(version, str)
        self.assertTrue(len(version) > 0)


if __name__ == '__main__':
    main()
