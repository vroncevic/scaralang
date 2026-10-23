# -*- coding: UTF-8 -*-

'''
Module
    system_decoder.py
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
    Decoder for system state and motor configuration binary frame payloads.
'''

from __future__ import annotations

from types import MappingProxyType
from typing import ClassVar, Final

from scaralang.core.model.dsl.ast.command_type import ScaraCommandType
from scaralang.core.model.motor.mode import MotorDriveMode
from scaralang.core.model.protocol.frame import BinaryFrame
from scaralang.core.model.protocol.message import MessageId
from scaralang.core.service.motor.wire import WireModeConverter
from scaralang.core.service.protocol.iactuator_unpacker import IBinaryActuatorPayloadUnpacker

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class SystemDecoder:
    '''
        Decodes motor configuration and system state change payloads.

        It defines:

            :attributes:
                | _CONFIG_MOTOR_ID - Message identifier for motor configuration command.
                | _SYSTEM_NAMES - Immutable mapping of system message IDs to command names.
                | _unpacker - Injected actuator payload unpacker protocol strategy.
            :methods:
                | __init__ - Initializes decoder with injected unpacker.
                | can_decode - Checks if message ID matches system or motor config command.
                | decode - Decodes system or motor config frame into detail string.
                | get_version - Returns decoder version string.
    '''

    _CONFIG_MOTOR_ID: ClassVar[int] = int(MessageId.CMD_CONFIG_MOTOR)
    _SYSTEM_NAMES: ClassVar[MappingProxyType[int, str]] = MappingProxyType({
        int(MessageId.CMD_HOME): ScaraCommandType.HOME.value,
        int(MessageId.CMD_ENABLE): ScaraCommandType.ENABLE.value,
        int(MessageId.CMD_DISABLE): ScaraCommandType.DISABLE.value,
        int(MessageId.CMD_ESTOP): ScaraCommandType.ESTOP.value,
        int(MessageId.CMD_HOLD): ScaraCommandType.HOLD.value,
        int(MessageId.CMD_RESUME): ScaraCommandType.RESUME.value,
    })

    _unpacker: IBinaryActuatorPayloadUnpacker

    def __init__(self, *, unpacker: IBinaryActuatorPayloadUnpacker) -> None:
        '''
            Initializes SystemDecoder with required payload unpacker.

            :param unpacker: Injected IBinaryActuatorPayloadUnpacker protocol strategy.
            :exceptions: None.
        '''
        self._unpacker: Final[IBinaryActuatorPayloadUnpacker] = unpacker

    def can_decode(self, *, msg_id: int) -> bool:
        '''
            Evaluates whether this decoder handles system state or motor config commands.

            :param msg_id: Numeric message identifier.
            :return: True if system command or motor config; False otherwise.
            :exceptions: None.
        '''
        return msg_id == self._CONFIG_MOTOR_ID or msg_id in self._SYSTEM_NAMES

    def decode(self, *, frame: BinaryFrame) -> str:
        '''
            Decodes system command or motor config frame into formatted string.

            :param frame: BinaryFrame instance containing system payload.
            :return: Formatted detail string.
            :exceptions: None.
        '''
        msg_id: int = int(frame.msg_id)

        if msg_id == self._CONFIG_MOTOR_ID:
            mode_int, _ = self._unpacker.unpack_motor_config(frame.payload)
            mode: MotorDriveMode = WireModeConverter.from_wire_mode(mode_int)

            return f'{ScaraCommandType.CONFIG.value} MOTOR {mode.value}'

        return self._SYSTEM_NAMES.get(msg_id, '')

    def get_version(self) -> str:
        '''
            Returns the decoder version string representation.

            :return: Version string representation.
            :exceptions: None.
        '''
        return __version__
