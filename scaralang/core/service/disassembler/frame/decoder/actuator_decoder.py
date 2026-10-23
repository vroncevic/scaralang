# -*- coding: UTF-8 -*-

'''
Module
    actuator_decoder.py
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
    Decoder for pneumatic tool and dwell wait binary frame payloads.
'''

from __future__ import annotations

from typing import ClassVar, Final, Literal

from scaralang.core.model.dsl.ast.command_type import ScaraCommandType
from scaralang.core.model.dsl.ast.pneumatic_state import PneumaticState
from scaralang.core.model.protocol.frame import BinaryFrame
from scaralang.core.model.protocol.payload_size import BinaryPayloadSize
from scaralang.core.model.protocol.message import MessageId
from scaralang.core.service.protocol.iactuator_unpacker import IBinaryActuatorPayloadUnpacker

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ActuatorDecoder:
    '''
        Decodes pneumatic tool pump, valve, and dwell wait payloads.

        It defines:

            :attributes:
                | _SUPPORTED_IDS - Frozenset of handled numeric message identifiers.
                | WAIT_PAYLOAD_SIZE - Expected byte length for delay duration payload.
                | BYTE_ORDER - Byte ordering standard for binary deserialization.
                | DEFAULT_WAIT_MS - Default fallback delay in milliseconds.
                | _unpacker - Injected actuator payload unpacker protocol strategy.
            :methods:
                | __init__ - Initializes decoder with injected unpacker.
                | can_decode - Checks if message ID matches tool or wait command.
                | decode - Decodes tool or wait payload into human-readable detail string.
                | get_version - Returns decoder version string.
    '''

    _SUPPORTED_IDS: ClassVar[frozenset[int]] = frozenset({
        int(MessageId.CMD_TOOL_PUMP),
        int(MessageId.CMD_TOOL_VALVE),
        int(MessageId.CMD_WAIT),
    })
    WAIT_PAYLOAD_SIZE: ClassVar[int] = int(BinaryPayloadSize.WAIT)
    BYTE_ORDER: ClassVar[Literal['little', 'big']] = 'little'
    DEFAULT_WAIT_MS: ClassVar[int] = 0

    _unpacker: IBinaryActuatorPayloadUnpacker

    def __init__(self, *, unpacker: IBinaryActuatorPayloadUnpacker) -> None:
        '''
            Initializes ActuatorDecoder with required payload unpacker.

            :param unpacker: Injected IBinaryActuatorPayloadUnpacker protocol strategy.
            :exceptions: None.
        '''
        self._unpacker: Final[IBinaryActuatorPayloadUnpacker] = unpacker

    def can_decode(self, *, msg_id: int) -> bool:
        '''
            Evaluates whether this decoder handles tool or wait commands.

            :param msg_id: Numeric message identifier.
            :return: True if tool pump, valve, or wait; False otherwise.
            :exceptions: None.
        '''
        return msg_id in self._SUPPORTED_IDS

    def decode(self, *, frame: BinaryFrame) -> str:
        '''
            Decodes tool or wait command payload into formatted string.

            :param frame: BinaryFrame instance containing tool or wait payload.
            :return: Formatted detail string.
            :exceptions: None.
        '''
        msg_id: int = int(frame.msg_id)

        if msg_id == int(MessageId.CMD_WAIT):
            payload = frame.payload
            wait_ms: int = (
                int.from_bytes(
                    payload[:self.WAIT_PAYLOAD_SIZE], byteorder=self.BYTE_ORDER
                )
                if len(payload) >= self.WAIT_PAYLOAD_SIZE
                else self.DEFAULT_WAIT_MS
            )

            return f'{ScaraCommandType.WAIT.value} {wait_ms}ms'

        _, state = self._unpacker.unpack_tool_cmd(frame.payload)
        tool_name: str = (
            ScaraCommandType.PUMP.value
            if msg_id == int(MessageId.CMD_TOOL_PUMP)
            else ScaraCommandType.VALVE.value
        )
        state_str: str = (
            PneumaticState.ON.value if state else PneumaticState.OFF.value
        )

        return f'{tool_name} {state_str}'

    def get_version(self) -> str:
        '''
            Returns the decoder version string representation.

            :return: Version string representation.
            :exceptions: None.
        '''
        return __version__
