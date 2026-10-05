# -*- coding: UTF-8 -*-

'''
Module
    step_test.py
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
    Unit tests for Step binary model.
'''

from __future__ import annotations

from dataclasses import FrozenInstanceError
from unittest import TestCase, main

from scaralang.core.model.dsl.binary.step import Step
from scaralang.core.model.protocol.binary_frame import BinaryFrame
from scaralang.core.model.protocol.message_id import MessageId

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.5'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class StepTest(TestCase):
    '''Unit tests validating Step model purity, immutability, and attribute values.'''

    def test_instantiation_and_attributes(self) -> None:
        '''Verify proper initialization and access of Step attributes.'''
        frame = BinaryFrame(
            msg_id=MessageId.CMD_MOVE_JOINT_STEPS,
            seq_num=1,
            payload=b'\x00' * 16,
            crc16=0x1234,
        )
        step = Step(
            frame=frame,
            raw_bytes=b'\x01\x02\x03\x04',
            duration_us=5000,
            target_steps=(100, 200, 300, 400),
            description='MOVE_J 100 200 300 400',
            line_number=3,
        )
        self.assertEqual(step.frame, frame)
        self.assertEqual(step.raw_bytes, b'\x01\x02\x03\x04')
        self.assertEqual(step.duration_us, 5000)
        self.assertEqual(step.target_steps, (100, 200, 300, 400))
        self.assertEqual(step.description, 'MOVE_J 100 200 300 400')
        self.assertEqual(step.line_number, 3)

    def test_frozen_immutability(self) -> None:
        '''Verify that modifying attributes on Step raises FrozenInstanceError.'''
        frame = BinaryFrame(
            msg_id=MessageId.CMD_HOME,
            seq_num=0,
            payload=b'',
            crc16=0x0000,
        )
        step = Step(
            frame=frame,
            raw_bytes=b'',
            duration_us=0,
            target_steps=(0, 0, 0, 0),
            description='HOME',
            line_number=1,
        )
        with self.assertRaises(FrozenInstanceError):
            setattr(step, 'duration_us', 1000)


if __name__ == '__main__':
    main()
