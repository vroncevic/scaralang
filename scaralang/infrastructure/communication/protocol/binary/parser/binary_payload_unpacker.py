# -*- coding: UTF-8 -*-

'''
Module
    binary_payload_unpacker.py
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
    Dedicated deserializer decoding binary packet payloads into typed domain models.
'''

from __future__ import annotations

from struct import unpack
from typing import ClassVar

from scaralang.core.model.exceptions.scara_protocol_error import ScaraProtocolError
from scaralang.core.model.motor.axis_mask import AxisMask
from scaralang.core.model.protocol.joint_steps import JointSteps
from scaralang.infrastructure.communication.protocol.binary.binary_struct_format import BinaryStructFormat

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.6'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class BinaryPayloadUnpacker:
    '''
        Deserializer decoding raw binary frame payloads into structured domain models.

        It defines:

            :attributes:
                | name - Identifier name of the payload unpacker.
                | JOINT_STEPS_FORMAT - Struct format for 22-byte joint step payload.
                | TOOL_CMD_FORMAT - Struct format for 2-byte tool command payload.
                | ACK_FORMAT - Struct format for 2-byte ACK payload.
                | NACK_FORMAT - Struct format for 2-byte NACK payload.
                | CONFIG_MOTOR_FORMAT - Struct format for 2-byte motor config payload.
            :methods:
                | unpack_tool_cmd - Deserializes 2-byte tool command into (tool_id, state).
                | unpack_joint_steps - Deserializes 22-byte joint steps into JointSteps.
                | unpack_ack - Deserializes 2-byte ACK into (acked_msg_id, queue_depth).
                | unpack_nack - Deserializes 2-byte NACK into (rejected_msg_id, error_code).
                | unpack_motor_config - Deserializes 2-byte motor config into (mode, axis_mask).
    '''

    JOINT_STEPS_FORMAT: ClassVar[str] = str(BinaryStructFormat.JOINT_STEPS)
    TOOL_CMD_FORMAT: ClassVar[str] = str(BinaryStructFormat.TOOL_CMD)
    ACK_FORMAT: ClassVar[str] = str(BinaryStructFormat.ACK)
    NACK_FORMAT: ClassVar[str] = str(BinaryStructFormat.NACK)
    CONFIG_MOTOR_FORMAT: ClassVar[str] = str(BinaryStructFormat.CONFIG_MOTOR)

    @property
    def name(self) -> str:
        '''
            Gets the payload unpacker identifier name.

            :return: Payload unpacker name string.
        '''
        return 'binary_payload_unpacker'

    @classmethod
    def unpack_tool_cmd(cls, data: bytes) -> tuple[int, bool]:
        '''
            Deserializes a 2-byte binary payload into tool ID and boolean state.

            :param data: Input raw binary bytes.
            :return: Tuple containing (tool_id, state).
            :exceptions: ScaraProtocolError if data is less than 2 bytes.
        '''
        if len(data) < 2:
            raise ScaraProtocolError(
                f'TOOL_CMD payload too short: expected at least 2 bytes, got {len(data)}'
            )

        values: tuple[int, int] = unpack(cls.TOOL_CMD_FORMAT, data[:2])

        return values[0], bool(values[1])


    @classmethod
    def unpack_joint_steps(cls, data: bytes) -> JointSteps:
        '''
            Deserializes a 22-byte binary payload into a JointSteps instance.

            :param data: Input raw binary bytes.
            :return: JointSteps instance.
            :exceptions: ScaraProtocolError if data is less than 22 bytes.
        '''
        if len(data) < 22:
            raise ScaraProtocolError(
                f'JOINT_STEPS payload too short: expected at least 22 bytes, got {len(data)}'
            )

        values: tuple[int, int, int, int, int, int] = unpack(
            cls.JOINT_STEPS_FORMAT, data[:22]
        )

        return JointSteps(
            target_j1_steps=values[0],
            target_j2_steps=values[1],
            target_z_steps=values[2],
            target_j4_steps=values[3],
            duration_us=values[4],
            feedrate_scale=values[5]
        )

    @classmethod
    def unpack_ack(cls, data: bytes) -> tuple[int, int]:
        '''
            Deserializes a 2-byte binary payload into ACK message ID and queue depth.

            :param data: Input raw binary bytes.
            :return: Tuple containing (acked_message_id, queue_depth).
            :exceptions: ScaraProtocolError if data is less than 2 bytes.
        '''
        if len(data) < 2:
            raise ScaraProtocolError(
                f'ACK payload too short: expected at least 2 bytes, got {len(data)}'
            )

        values: tuple[int, int] = unpack(cls.ACK_FORMAT, data[:2])

        return values[0], values[1]

    @classmethod
    def unpack_nack(cls, data: bytes) -> tuple[int, int]:
        '''
            Deserializes a 2-byte binary payload into NACK message ID and error code.

            :param data: Input raw binary bytes.
            :return: Tuple containing (rejected_message_id, error_code).
            :exceptions: ScaraProtocolError if data is less than 2 bytes.
        '''
        if len(data) < 2:
            raise ScaraProtocolError(
                f'NACK payload too short: expected at least 2 bytes, got {len(data)}'
            )

        values: tuple[int, int] = unpack(cls.NACK_FORMAT, data[:2])

        return values[0], values[1]

    @classmethod
    def unpack_motor_config(cls, data: bytes) -> tuple[int, int]:
        '''
            Deserializes a binary payload into motor drive mode and axis mask.

            :param data: Input raw binary bytes.
            :return: Tuple containing (mode, axis_mask).
        '''
        if len(data) >= 2:
            values: tuple[int, int] = unpack(cls.CONFIG_MOTOR_FORMAT, data[:2])
            return values[0], values[1]

        if len(data) == 1:
            return data[0], AxisMask.ALL.value

        return 0, AxisMask.ALL.value
