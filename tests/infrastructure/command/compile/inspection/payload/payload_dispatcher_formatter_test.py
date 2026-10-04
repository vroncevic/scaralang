# -*- coding: UTF-8 -*-

'''
Module
    payload_dispatcher_formatter_test.py
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
    Unit tests for PayloadDispatcherFormatter service.
'''

from __future__ import annotations

from struct import pack
from unittest import TestCase, main

from scaralang.core.model.protocol.message_id import MessageId
from scaralang.infrastructure.command.compile.inspection.framing.hex_stream_formatter import HexStreamFormatter
from scaralang.infrastructure.command.compile.inspection.payload.ipayload_dispatcher_formatter import IPayloadDispatcherFormatter
from scaralang.infrastructure.command.compile.inspection.payload.joint_steps_payload_formatter import JointStepsPayloadFormatter
from scaralang.infrastructure.command.compile.inspection.payload.payload_dispatcher_formatter import PayloadDispatcherFormatter
from scaralang.infrastructure.command.compile.inspection.payload.tool_command_payload_formatter import ToolCommandPayloadFormatter
from scaralang.infrastructure.communication.protocol.binary.binary_struct_format import BinaryStructFormat
from scaralang.infrastructure.communication.protocol.binary.parser.binary_payload_unpacker import BinaryPayloadUnpacker

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestPayloadDispatcherFormatter(TestCase):
    '''
        Test suite verifying PayloadDispatcherFormatter routing.

        It defines:

            :methods:
                | setUp - Initializes dispatcher and collaborator fixtures.
                | test_implements_protocol - Verifies structural protocol compliance.
                | test_format_payload_empty - Verifies empty payload formatting.
                | test_format_payload_generic_hex - Verifies generic hex payload dump.
                | test_format_payload_tool - Verifies tool payload dispatch.
                | test_format_payload_joint_steps - Verifies joint steps payload dispatch.
                | test_format_payload_motor_config - Verifies motor config payload dispatch.
    '''

    def setUp(self) -> None:
        '''Initializes dispatcher and collaborator fixtures.'''
        hex_fmt: HexStreamFormatter = HexStreamFormatter()
        self.dispatcher: PayloadDispatcherFormatter = PayloadDispatcherFormatter(
            joint_formatter=JointStepsPayloadFormatter(hex_formatter=hex_fmt),
            tool_formatter=ToolCommandPayloadFormatter(hex_formatter=hex_fmt),
            hex_formatter=hex_fmt,
            unpacker=BinaryPayloadUnpacker(),
        )

    def test_implements_protocol(self) -> None:
        '''Verifies structural protocol compliance.'''
        self.assertTrue(isinstance(self.dispatcher, IPayloadDispatcherFormatter))
        self.assertFalse(isinstance(object(), IPayloadDispatcherFormatter))

    def test_get_version(self) -> None:
        '''Verifies get_version returns valid semantic version.'''
        self.assertEqual(self.dispatcher.get_version(), '1.0.3')

    def test_format_payload_empty(self) -> None:
        '''Verifies empty payload formatting.'''
        result: str = self.dispatcher.format_payload(
            msg_id=MessageId.CMD_HOME,
            payload=b'',
        )
        self.assertEqual(result, '  - Payload:       (None)')

    def test_format_payload_generic_hex(self) -> None:
        '''Verifies generic hex payload dump.'''
        result: str = self.dispatcher.format_payload(
            msg_id=MessageId.CMD_PING,
            payload=b'\x11\x22',
        )
        self.assertIn('Payload Hex:   11 22', result)

    def test_format_payload_tool(self) -> None:
        '''Verifies tool payload dispatch.'''
        result: str = self.dispatcher.format_payload(
            msg_id=MessageId.CMD_TOOL_PUMP,
            payload=bytes([0, 1]),
        )
        self.assertIn('Tool=PUMP', result)

    def test_format_payload_joint_steps(self) -> None:
        '''Verifies joint steps payload dispatch.'''
        raw_steps = pack(str(BinaryStructFormat.JOINT_STEPS), 100, -200, 300, 400, 50000, 100)
        result: str = self.dispatcher.format_payload(
            msg_id=MessageId.CMD_MOVE_JOINT_STEPS,
            payload=raw_steps,
        )
        self.assertIn('J1=+100 steps', result)

    def test_format_payload_motor_config(self) -> None:
        '''Verifies motor config payload dispatch.'''
        raw_motor = pack(str(BinaryStructFormat.CONFIG_MOTOR), 1, 0x0F)
        result: str = self.dispatcher.format_payload(
            msg_id=MessageId.CMD_CONFIG_MOTOR,
            payload=raw_motor,
        )
        self.assertIn('Motor Mode', result)


if __name__ == '__main__':
    main()
