# -*- coding: UTF-8 -*-

'''
Module
    calculator_test.py
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
    Unit tests for DisassemblySummaryCalculator implementation.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.model.disassembler.disassembled_frame import DisassembledFrame
from scaralang.core.model.disassembler.disassembly_summary import DisassemblySummary
from scaralang.core.model.protocol.message import MessageId
from scaralang.core.service.disassembler.summary.calculator import DisassemblySummaryCalculator
from scaralang.core.service.disassembler.summary.icalculator import IDisassemblySummaryCalculator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestDisassemblySummaryCalculator(TestCase):
    '''
        Test cases verifying DisassemblySummaryCalculator implementation.

        It defines:

            :methods:
                | setUp - Initializes test environment and calculator instance.
                | test_structural_protocol_compliance - Verifies protocol adherence.
                | test_calculate_summary - Verifies summary statistics computation.
                | test_get_version - Verifies version string retrieval.
    '''

    def setUp(self) -> None:
        '''
            Sets up calculator test fixture.

            :exceptions: None.
        '''
        self.calculator: DisassemblySummaryCalculator = DisassemblySummaryCalculator()

    def test_structural_protocol_compliance(self) -> None:
        '''
            Verifies calculator implements IDisassemblySummaryCalculator protocol.

            :exceptions: None.
        '''
        self.assertTrue(isinstance(self.calculator, IDisassemblySummaryCalculator))

    def test_calculate_summary(self) -> None:
        '''
            Verifies calculating disassembly summary statistics.

            :exceptions: None.
        '''
        home_frame: DisassembledFrame = DisassembledFrame(
            index=0,
            seq_num=1,
            msg_id=int(MessageId.CMD_HOME),
            msg_name='CMD_HOME',
            detail='HOME',
        )
        move_frame: DisassembledFrame = DisassembledFrame(
            index=1,
            seq_num=2,
            msg_id=int(MessageId.CMD_MOVE_JOINT_STEPS),
            msg_name='CMD_MOVE_JOINT_STEPS',
            detail='MOVE',
        )
        pump_frame: DisassembledFrame = DisassembledFrame(
            index=2,
            seq_num=3,
            msg_id=int(MessageId.CMD_TOOL_PUMP),
            msg_name='CMD_TOOL_PUMP',
            detail='PUMP ON',
        )
        wait_frame: DisassembledFrame = DisassembledFrame(
            index=3,
            seq_num=4,
            msg_id=int(MessageId.CMD_WAIT),
            msg_name='CMD_WAIT',
            detail='WAIT 250ms',
        )
        summary: DisassemblySummary = self.calculator.calculate_summary(
            frames=(home_frame, move_frame, pump_frame, wait_frame),
            byte_count=48,
        )
        self.assertEqual(summary.total_bytes, 48)
        self.assertEqual(summary.decoded_frames, 4)
        self.assertEqual(summary.motion_frames, 1)
        self.assertEqual(summary.tool_commands, 1)
        self.assertEqual(summary.wait_delays, 1)
        self.assertEqual(summary.system_frames, 1)

    def test_get_version(self) -> None:
        '''
            Verifies calculator version string retrieval.

            :exceptions: None.
        '''
        self.assertEqual(self.calculator.get_version(), '1.1.1')


if __name__ == '__main__':
    main()
