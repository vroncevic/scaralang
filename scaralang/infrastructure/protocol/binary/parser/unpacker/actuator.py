# -*- coding: UTF-8 -*-

'''
Module
    actuator.py
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
    Dedicated deserializer decoding tool and motor configuration payloads.
'''

from __future__ import annotations

from struct import unpack
from typing import ClassVar

from scaralang.core.model.exceptions.scara_protocol_error import ScaraProtocolError
from scaralang.core.model.motor.axis_mask import AxisMask
from scaralang.core.model.protocol.binary_payload_size import BinaryPayloadSize
from scaralang.infrastructure.protocol.binary.struct_format import BinaryStructFormat

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.9'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class BinaryActuatorPayloadUnpacker:
    '''
        Deserializer decoding raw actuator command payloads into typed values.

        It defines:

            :attributes:
                | DEFAULT_MOTOR_MODE - Default motor mode when payload is empty (0).
                | TOOL_CMD_FORMAT - Struct format for 2-byte tool command payload.
                | CONFIG_MOTOR_FORMAT - Struct format for 2-byte motor config payload.
            :methods:
                | unpack_tool_cmd - Deserializes 2-byte tool command into (tool_id, state).
                | unpack_motor_config - Deserializes 2-byte motor config into (mode, axis_mask).
                | get_version - Returns component version string.
    '''

    DEFAULT_MOTOR_MODE: ClassVar[int] = 0
    TOOL_CMD_FORMAT: ClassVar[str] = str(BinaryStructFormat.TOOL_CMD)
    CONFIG_MOTOR_FORMAT: ClassVar[str] = str(BinaryStructFormat.CONFIG_MOTOR)

    def unpack_tool_cmd(self, data: bytes) -> tuple[int, bool]:
        '''
            Deserializes a 2-byte binary payload into tool ID and boolean state.

            :param data: Input raw binary bytes.
            :return: Tuple containing (tool_id, state).
            :exceptions: ScaraProtocolError if data is less than 2 bytes.
        '''
        if len(data) < BinaryPayloadSize.TOOL_CMD:
            raise ScaraProtocolError(
                f'TOOL_CMD payload too short: expected at least '
                f'{int(BinaryPayloadSize.TOOL_CMD)} bytes, got {len(data)}'
            )

        values: tuple[int, int] = unpack(
            self.TOOL_CMD_FORMAT, data[:BinaryPayloadSize.TOOL_CMD]
        )

        return values[0], bool(values[1])

    def unpack_motor_config(self, data: bytes) -> tuple[int, int]:
        '''
            Deserializes a binary payload into motor drive mode and axis mask.

            :param data: Input raw binary bytes.
            :return: Tuple containing (mode, axis_mask).
            :exceptions: None.
        '''
        if len(data) >= BinaryPayloadSize.CONFIG_MOTOR:
            values: tuple[int, int] = unpack(
                self.CONFIG_MOTOR_FORMAT, data[:BinaryPayloadSize.CONFIG_MOTOR]
            )
            return values[0], values[1]

        if len(data) == BinaryPayloadSize.OVERRIDE:
            return data[0], AxisMask.ALL.value

        return self.DEFAULT_MOTOR_MODE, AxisMask.ALL.value

    def get_version(self) -> str:
        '''
            Returns component version string.

            :return: Version string.
            :exceptions: None.
        '''
        return __version__
