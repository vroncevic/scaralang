# -*- coding: UTF-8 -*-

'''
Module
    iresponse_unpacker_test.py
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
    Unit tests for IBinaryResponsePayloadUnpacker protocol compliance.
'''

from __future__ import annotations

from struct import pack
from unittest import TestCase
from unittest import main

from scaralang.core.service.protocol.iresponse_unpacker import IBinaryResponsePayloadUnpacker
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


class TestIBinaryResponsePayloadUnpacker(TestCase):
    '''
        Test cases verifying IBinaryResponsePayloadUnpacker structural subtyping.

        It defines:

            :methods:
                | test_structural_compliance - Verifies unpacker satisfies protocol.
                | test_unpack_ack - Verifies ACK payload deserialization.
                | test_unpack_nack - Verifies NACK payload deserialization.
                | test_get_version - Verifies version retrieval.
    '''

    def test_structural_compliance(self) -> None:
        '''
            Verifies that concrete unpacker satisfies IBinaryResponsePayloadUnpacker.

            :exceptions: None.
        '''
        unpacker = BinaryResponsePayloadUnpacker()
        self.assertIsInstance(unpacker, IBinaryResponsePayloadUnpacker)
        self.assertFalse(isinstance(object(), IBinaryResponsePayloadUnpacker))

    def test_unpack_ack(self) -> None:
        '''
            Verifies ACK payload unpacking through protocol contract.

            :exceptions: None.
        '''
        unpacker = BinaryResponsePayloadUnpacker()
        raw_payload = pack(str(BinaryStructFormat.ACK), 10, 4)
        msg_id, queue_depth = unpacker.unpack_ack(data=raw_payload)
        self.assertEqual(msg_id, 10)
        self.assertEqual(queue_depth, 4)

    def test_unpack_nack(self) -> None:
        '''
            Verifies NACK payload unpacking through protocol contract.

            :exceptions: None.
        '''
        unpacker = BinaryResponsePayloadUnpacker()
        raw_payload = pack(str(BinaryStructFormat.NACK), 20, 2)
        msg_id, error_code = unpacker.unpack_nack(data=raw_payload)
        self.assertEqual(msg_id, 20)
        self.assertEqual(error_code, 2)

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
