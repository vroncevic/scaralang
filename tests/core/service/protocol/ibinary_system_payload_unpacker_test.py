# -*- coding: UTF-8 -*-

'''
Module
    ibinary_system_payload_unpacker_test.py
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
    Unit tests for IBinarySystemPayloadUnpacker protocol compliance.
'''

from __future__ import annotations

from struct import pack
from unittest import TestCase
from unittest import main

from scaralang.core.service.protocol.ibinary_system_payload_unpacker import IBinarySystemPayloadUnpacker
from scaralang.infrastructure.protocol.binary.parser.unpacker.system import BinarySystemPayloadUnpacker
from scaralang.infrastructure.protocol.binary.struct_format import BinaryStructFormat

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.9'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestIBinarySystemPayloadUnpacker(TestCase):
    '''
        Test cases verifying IBinarySystemPayloadUnpacker structural subtyping.

        It defines:

            :methods:
                | test_structural_compliance - Verifies unpacker satisfies protocol.
                | test_unpack_jog_payload - Verifies jog payload deserialization.
                | test_unpack_override - Verifies speed override deserialization.
                | test_get_version - Verifies version retrieval.
    '''

    def test_structural_compliance(self) -> None:
        '''
            Verifies that concrete unpacker satisfies IBinarySystemPayloadUnpacker.

            :exceptions: None.
        '''
        unpacker = BinarySystemPayloadUnpacker()
        self.assertIsInstance(unpacker, IBinarySystemPayloadUnpacker)
        self.assertFalse(isinstance(object(), IBinarySystemPayloadUnpacker))

    def test_unpack_jog_payload(self) -> None:
        '''
            Verifies jog payload unpacking through protocol contract.

            :exceptions: None.
        '''
        unpacker = BinarySystemPayloadUnpacker()
        raw_payload = pack(str(BinaryStructFormat.JOG_SHORT), 2, -150)
        joint_idx, step_delta, speed = unpacker.unpack_jog_payload(data=raw_payload)
        self.assertEqual(joint_idx, 2)
        self.assertEqual(step_delta, -150)
        self.assertEqual(speed, 2000)

    def test_unpack_override(self) -> None:
        '''
            Verifies speed override payload unpacking through protocol contract.

            :exceptions: None.
        '''
        unpacker = BinarySystemPayloadUnpacker()
        raw_payload = pack(str(BinaryStructFormat.OVERRIDE), 75)
        speed = unpacker.unpack_override(data=raw_payload)
        self.assertEqual(speed, 75)

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
