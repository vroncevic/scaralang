# -*- coding: UTF-8 -*-

'''
Module
    ibinary_motion_payload_unpacker_test.py
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
    Unit tests for IBinaryMotionPayloadUnpacker protocol compliance.
'''

from __future__ import annotations

from struct import pack
from unittest import TestCase
from unittest import main

from scaralang.core.model.protocol.joint_steps import JointSteps
from scaralang.core.service.protocol.ibinary_motion_payload_unpacker import IBinaryMotionPayloadUnpacker
from scaralang.infrastructure.protocol.binary.parser.unpacker.motion import BinaryMotionPayloadUnpacker
from scaralang.infrastructure.protocol.binary.struct_format import BinaryStructFormat

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.9'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestIBinaryMotionPayloadUnpacker(TestCase):
    '''
        Test cases verifying IBinaryMotionPayloadUnpacker structural subtyping.

        It defines:

            :methods:
                | test_structural_compliance - Verifies unpacker satisfies protocol.
                | test_unpack_joint_steps - Verifies joint steps payload deserialization.
                | test_get_version - Verifies version retrieval.
    '''

    def test_structural_compliance(self) -> None:
        '''
            Verifies that concrete unpacker satisfies IBinaryMotionPayloadUnpacker.

            :exceptions: None.
        '''
        unpacker = BinaryMotionPayloadUnpacker()
        self.assertIsInstance(unpacker, IBinaryMotionPayloadUnpacker)
        self.assertFalse(isinstance(object(), IBinaryMotionPayloadUnpacker))

    def test_unpack_joint_steps(self) -> None:
        '''
            Verifies joint steps payload unpacking through protocol contract.

            :exceptions: None.
        '''
        unpacker = BinaryMotionPayloadUnpacker()
        raw_payload = pack(
            str(BinaryStructFormat.JOINT_STEPS),
            100, 200, 300, 400, 500, 600,
        )
        steps = unpacker.unpack_joint_steps(data=raw_payload)
        self.assertIsInstance(steps, JointSteps)
        self.assertEqual(steps.target_j1_steps, 100)
        self.assertEqual(steps.target_j2_steps, 200)
        self.assertEqual(steps.target_z_steps, 300)
        self.assertEqual(steps.target_j4_steps, 400)
        self.assertEqual(steps.duration_us, 500)
        self.assertEqual(steps.feedrate_scale, 600)

    def test_get_version(self) -> None:
        '''
            Verifies semantic version string retrieval.

            :exceptions: None.
        '''
        unpacker = BinaryMotionPayloadUnpacker()
        version: str = unpacker.get_version()
        self.assertIsInstance(version, str)
        self.assertTrue(len(version) > 0)


if __name__ == '__main__':
    main()
