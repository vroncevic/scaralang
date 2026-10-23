# -*- coding: UTF-8 -*-

'''
Module
    iactuator_unpacker_test.py
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
    Unit tests for IBinaryActuatorPayloadUnpacker protocol compliance.
'''

from __future__ import annotations

from struct import pack
from unittest import TestCase
from unittest import main

from scaralang.core.service.protocol.iactuator_unpacker import IBinaryActuatorPayloadUnpacker
from scaralang.infrastructure.protocol.parser.unpacker.actuator import BinaryActuatorPayloadUnpacker
from scaralang.infrastructure.protocol.struct_format import BinaryStructFormat

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestIBinaryActuatorPayloadUnpacker(TestCase):
    '''
        Test cases verifying IBinaryActuatorPayloadUnpacker structural subtyping.

        It defines:

            :methods:
                | test_structural_compliance - Verifies unpacker satisfies protocol.
                | test_unpack_tool_cmd - Verifies tool command deserialization.
                | test_unpack_motor_config - Verifies motor configuration deserialization.
                | test_get_version - Verifies version retrieval.
    '''

    def test_structural_compliance(self) -> None:
        '''
            Verifies that concrete unpacker satisfies IBinaryActuatorPayloadUnpacker.

            :exceptions: None.
        '''
        unpacker = BinaryActuatorPayloadUnpacker()
        self.assertIsInstance(unpacker, IBinaryActuatorPayloadUnpacker)
        self.assertFalse(isinstance(object(), IBinaryActuatorPayloadUnpacker))

    def test_unpack_tool_cmd(self) -> None:
        '''
            Verifies tool command payload unpacking through protocol contract.

            :exceptions: None.
        '''
        unpacker = BinaryActuatorPayloadUnpacker()
        raw_payload = pack(str(BinaryStructFormat.TOOL_CMD), 1, 1)
        tool_id, state = unpacker.unpack_tool_cmd(data=raw_payload)
        self.assertEqual(tool_id, 1)
        self.assertTrue(state)

    def test_unpack_motor_config(self) -> None:
        '''
            Verifies motor config payload unpacking through protocol contract.

            :exceptions: None.
        '''
        unpacker = BinaryActuatorPayloadUnpacker()
        raw_payload = pack(str(BinaryStructFormat.CONFIG_MOTOR), 1, 0x0F)
        mode, axis_mask = unpacker.unpack_motor_config(data=raw_payload)
        self.assertEqual(mode, 1)
        self.assertEqual(axis_mask, 0x0F)

    def test_get_version(self) -> None:
        '''
            Verifies semantic version string retrieval.

            :exceptions: None.
        '''
        unpacker = BinaryActuatorPayloadUnpacker()
        version: str = unpacker.get_version()
        self.assertIsInstance(version, str)
        self.assertTrue(len(version) > 0)


if __name__ == '__main__':
    main()
