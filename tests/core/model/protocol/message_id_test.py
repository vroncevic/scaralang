# -*- coding: UTF-8 -*-

'''
Module
    message_id_test.py
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
    Unit tests for MessageId protocol enumeration model.
'''

from __future__ import annotations

from unittest import TestCase, main

from scaralang.core.model.protocol.message_id import MessageId

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.6'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class MessageIdTest(TestCase):
    '''Unit tests validating MessageId enumeration members, integer values, and lookups.'''

    def test_enumeration_members_count(self) -> None:
        '''Verify total number of defined binary protocol message IDs.'''
        self.assertEqual(len(MessageId), 30)

    def test_command_message_values(self) -> None:
        '''Verify integer opcodes for primary command messages.'''
        self.assertEqual(MessageId.CMD_NONE, 0x00)
        self.assertEqual(MessageId.CMD_MOVE_JOINT_STEPS, 0x01)
        self.assertEqual(MessageId.CMD_ENABLE, 0x03)
        self.assertEqual(MessageId.CMD_DISABLE, 0x04)
        self.assertEqual(MessageId.CMD_ESTOP, 0x05)
        self.assertEqual(MessageId.CMD_HOME, 0x06)
        self.assertEqual(MessageId.CMD_HOLD, 0x07)
        self.assertEqual(MessageId.CMD_RESUME, 0x08)
        self.assertEqual(MessageId.CMD_JOG_JOINT, 0x09)
        self.assertEqual(MessageId.CMD_SETPOS_STEPS, 0x0A)
        self.assertEqual(MessageId.CMD_TOOL_PUMP, 0x0B)
        self.assertEqual(MessageId.CMD_TOOL_VALVE, 0x0C)
        self.assertEqual(MessageId.CMD_WAIT, 0x0D)
        self.assertEqual(MessageId.CMD_OVERRIDE, 0x0E)
        self.assertEqual(MessageId.CMD_CONFIG_MOTOR, 0x0F)

    def test_query_and_maintenance_message_values(self) -> None:
        '''Verify integer opcodes for query and maintenance messages.'''
        self.assertEqual(MessageId.CMD_GET_STATUS, 0x20)
        self.assertEqual(MessageId.CMD_GET_STEPS, 0x21)
        self.assertEqual(MessageId.CMD_GET_DIAGNOSTICS, 0x22)
        self.assertEqual(MessageId.CMD_CLEAR_FAULT, 0x23)
        self.assertEqual(MessageId.CMD_PING, 0x24)
        self.assertEqual(MessageId.CMD_BOOTLOADER, 0x30)

    def test_response_message_values(self) -> None:
        '''Verify integer opcodes for response and notification messages.'''
        self.assertEqual(MessageId.RESP_ACK, 0x80)
        self.assertEqual(MessageId.RESP_NACK, 0x81)
        self.assertEqual(MessageId.RESP_STATUS, 0x82)
        self.assertEqual(MessageId.RESP_STEPS, 0x83)
        self.assertEqual(MessageId.RESP_PONG, 0x84)
        self.assertEqual(MessageId.RESP_MOVE_EVENT, 0x85)
        self.assertEqual(MessageId.RESP_HOMING_EVENT, 0x86)
        self.assertEqual(MessageId.RESP_DIAGNOSTICS, 0x88)
        self.assertEqual(MessageId.RESP_FAULT_EVENT, 0x89)

    def test_lookup_by_value(self) -> None:
        '''Verify member lookup from integer values.'''
        self.assertIs(MessageId(0x01), MessageId.CMD_MOVE_JOINT_STEPS)
        self.assertIs(MessageId(0x80), MessageId.RESP_ACK)
        self.assertIs(MessageId(0x81), MessageId.RESP_NACK)

    def test_invalid_value_raises_value_error(self) -> None:
        '''Verify that undefined integer opcode raises ValueError.'''
        with self.assertRaises(ValueError):
            MessageId(0xFF)


if __name__ == '__main__':
    main()
