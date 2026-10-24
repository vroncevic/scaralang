# -*- coding: UTF-8 -*-

'''
Module
    system.py
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
    Dedicated deserializer decoding system, jog, and override payloads.
'''

from __future__ import annotations

from struct import unpack
from typing import ClassVar

from scaralang.core.model.exceptions.protocol import ScaraProtocolError
from scaralang.core.model.protocol.payload_size import BinaryPayloadSize
from scaralang.infrastructure.protocol.struct_format import BinaryStructFormat

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class BinarySystemPayloadUnpacker:
    '''
        Deserializer decoding jog and speed override command payloads.

        It defines:

            :attributes:
                | DEFAULT_JOG_SPEED - Default stepping rate for jog motion (2000).
                | JOG_FORMAT - Struct format for 9-byte joint jog payload.
                | JOG_SHORT_FORMAT - Struct format for 5-byte joint jog payload.
                | OVERRIDE_FORMAT - Struct format for 1-byte speed override payload.
            :methods:
                | unpack_jog_payload - Deserializes joint jog payload into (joint_id, step, speed).
                | unpack_override - Deserializes speed override payload into percentage integer.
                | get_version - Returns component version string.
    '''

    DEFAULT_JOG_SPEED: ClassVar[int] = 2000
    JOG_FORMAT: ClassVar[str] = str(BinaryStructFormat.JOG)
    JOG_SHORT_FORMAT: ClassVar[str] = str(BinaryStructFormat.JOG_SHORT)
    OVERRIDE_FORMAT: ClassVar[str] = str(BinaryStructFormat.OVERRIDE)

    def unpack_jog_payload(self, data: bytes) -> tuple[int, int, int]:
        '''
            Deserializes a joint jog command payload into joint index, step, and speed.

            :param data: Input raw binary bytes.
            :return: Tuple containing (joint_id, step, speed).
            :exceptions: ScaraProtocolError if data is less than 5 bytes.
        '''
        if len(data) < BinaryPayloadSize.JOG_SHORT:
            raise ScaraProtocolError(
                f'JOG payload too short: expected at least '
                f'{int(BinaryPayloadSize.JOG_SHORT)} bytes, got {len(data)}'
            )

        if len(data) >= BinaryPayloadSize.JOG_FULL:
            values: tuple[int, int, int] = unpack(
                self.JOG_FORMAT, data[:BinaryPayloadSize.JOG_FULL]
            )
            return values[0], values[1], values[2]

        short_values: tuple[int, int] = unpack(
            self.JOG_SHORT_FORMAT, data[:BinaryPayloadSize.JOG_SHORT]
        )
        return short_values[0], short_values[1], self.DEFAULT_JOG_SPEED

    def unpack_override(self, data: bytes) -> int:
        '''
            Deserializes a speed override command payload into percentage integer.

            :param data: Input raw binary bytes.
            :return: Speed override percentage.
            :exceptions: ScaraProtocolError if data is empty.
        '''
        if not data:
            raise ScaraProtocolError('OVERRIDE payload is empty')

        values: tuple[int] = unpack(
            self.OVERRIDE_FORMAT, data[:BinaryPayloadSize.OVERRIDE]
        )
        return values[0]

    def get_version(self) -> str:
        '''
            Returns component version string.

            :return: Version string.
            :exceptions: None.
        '''
        return __version__
