# -*- coding: UTF-8 -*-

'''
Module
    system_test.py
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
    Unit tests for BinarySystemPayloadUnpacker implementation.
'''

from __future__ import annotations

from struct import pack
from unittest import TestCase, main

from scaralang.core.model.exceptions.protocol import ScaraProtocolError
from scaralang.infrastructure.protocol.parser.unpacker.system import BinarySystemPayloadUnpacker
from scaralang.infrastructure.protocol.struct_format import BinaryStructFormat

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestBinarySystemPayloadUnpacker(TestCase):
    '''
        Test cases verifying BinarySystemPayloadUnpacker implementation.

        It defines:

            :methods:
                | test_unpack_jog_payload - Verifies jog payload deserialization.
                | test_unpack_override - Verifies speed override deserialization.
                | test_get_version - Verifies version string retrieval.
    '''

    def test_unpack_jog_payload(self) -> None:
        '''
            Verifies jog payload deserialization.

            :exceptions: None.
        '''
        unpacker = BinarySystemPayloadUnpacker()
        raw_payload = pack(str(BinaryStructFormat.JOG_SHORT), 1, 200)
        joint_idx, step_delta, speed = unpacker.unpack_jog_payload(data=raw_payload)
        self.assertEqual(joint_idx, 1)
        self.assertEqual(step_delta, 200)
        self.assertEqual(speed, 2000)

        full_payload = pack(str(BinaryStructFormat.JOG), 2, 500, 1500)
        j_idx, s_delta, spd = unpacker.unpack_jog_payload(data=full_payload)
        self.assertEqual(j_idx, 2)
        self.assertEqual(s_delta, 500)
        self.assertEqual(spd, 1500)

        with self.assertRaises(ScaraProtocolError):
            unpacker.unpack_jog_payload(data=b'')

    def test_unpack_override(self) -> None:
        '''
            Verifies speed override deserialization.

            :exceptions: None.
        '''
        unpacker = BinarySystemPayloadUnpacker()
        raw_payload = pack(str(BinaryStructFormat.OVERRIDE), 50)
        speed = unpacker.unpack_override(data=raw_payload)
        self.assertEqual(speed, 50)

        with self.assertRaises(ScaraProtocolError):
            unpacker.unpack_override(data=b'')

    def test_get_version(self) -> None:
        '''
            Verifies semantic version string retrieval.

            :exceptions: None.
        '''
        unpacker = BinarySystemPayloadUnpacker()
        version: str = unpacker.get_version()
        self.assertIsInstance(version, str)
        self.assertTrue(len(version) > 0)


if __name__ == '__main__':
    main()
