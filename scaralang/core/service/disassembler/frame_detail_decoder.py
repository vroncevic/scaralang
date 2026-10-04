# -*- coding: UTF-8 -*-

'''
Module
    frame_detail_decoder.py
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
    Defines FrameDetailDecoder decoding binary wire frame payloads and symbolic message names.
'''

from __future__ import annotations

from typing import Final

from scaralang.core.model.dsl.ast.command_type import ScaraCommandType
from scaralang.core.model.dsl.ast.pneumatic_state import PneumaticState
from scaralang.core.model.motor.motor_drive_mode import MotorDriveMode
from scaralang.core.model.protocol.binary_frame import BinaryFrame
from scaralang.core.service.motor.motor_config_factory import MotorConfigFactory
from scaralang.core.model.protocol.joint_steps import JointSteps
from scaralang.core.model.protocol.message_id import MessageId
from scaralang.core.service.protocol.ibinary_payload_unpacker import IBinaryPayloadUnpacker

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class FrameDetailDecoder:
    '''
        Decodes wire protocol frame payloads into structured, human-readable representations.

        It defines:

            :attributes:
                | _unpacker - Injected binary payload unpacker strategy.
                | _system_names - Mapping of system message IDs to command names.
            :methods:
                | __init__ - Initializes decoder with injected unpacker.
                | decode_msg_name - Returns symbolic message identifier name.
                | decode_joint_steps - Decodes joint step displacement payload.
                | decode_tool_command - Decodes pneumatic tool pump/valve payload.
                | decode_wait - Decodes dwell wait delay payload.
                | decode_system - Decodes state change system messages.
                | decode_fallback - Decodes arbitrary payload bytes into hexadecimal string.
                | decode_detail - Routes frame to specific payload decoder.
    '''

    _unpacker: IBinaryPayloadUnpacker
    _system_names: dict[int, str]

    def __init__(self, *, unpacker: IBinaryPayloadUnpacker) -> None:
        '''
            Initializes FrameDetailDecoder with injected payload unpacker.

            :param unpacker: Binary payload unpacker protocol strategy.
        '''
        self._unpacker: Final[IBinaryPayloadUnpacker] = unpacker
        self._system_names: Final[dict[int, str]] = {
            int(MessageId.CMD_HOME): ScaraCommandType.HOME.value,
            int(MessageId.CMD_ENABLE): ScaraCommandType.ENABLE.value,
            int(MessageId.CMD_DISABLE): ScaraCommandType.DISABLE.value,
            int(MessageId.CMD_ESTOP): ScaraCommandType.ESTOP.value,
            int(MessageId.CMD_HOLD): ScaraCommandType.HOLD.value,
            int(MessageId.CMD_RESUME): ScaraCommandType.RESUME.value,
        }

    def decode_msg_name(self, *, msg_id: int) -> str:
        '''
            Decodes integer message identifier into symbolic enum name.

            :param msg_id: Numeric message identifier.
            :return: Symbolic name string or UNKNOWN.
        '''
        try:
            return MessageId(msg_id).name

        except ValueError:
            return 'UNKNOWN'

    def decode_joint_steps(self, *, payload: bytes) -> str:
        '''
            Decodes joint step displacement payload into formatted string.

            :param payload: Packed bytes of joint steps payload.
            :return: Formatted coordinate string.
        '''
        steps: JointSteps = self._unpacker.unpack_joint_steps(payload)

        return (
            f'J1={steps.target_j1_steps} J2={steps.target_j2_steps} '
            f'Z={steps.target_z_steps} J4={steps.target_j4_steps} '
            f'dur={steps.duration_us}us'
        )

    def decode_tool_command(self, *, msg_id: int, payload: bytes) -> str:
        '''
            Decodes pneumatic tool command payload into state description.

            :param msg_id: Tool message identifier integer.
            :param payload: Packed tool command bytes.
            :return: Tool name and activation state string.
        '''
        _, state = self._unpacker.unpack_tool_cmd(payload)
        tool_name: str = (
            ScaraCommandType.PUMP.value
            if msg_id == int(MessageId.CMD_TOOL_PUMP)
            else ScaraCommandType.VALVE.value
        )
        state_str: str = (
            PneumaticState.ON.value if state else PneumaticState.OFF.value
        )

        return f'{tool_name} {state_str}'

    def decode_wait(self, *, payload: bytes) -> str:
        '''
            Decodes wait delay payload into millisecond string.

            :param payload: Packed wait delay bytes.
            :return: Formatted wait duration string.
        '''
        wait_ms: int = (
            int.from_bytes(payload[:4], byteorder='little')
            if len(payload) >= 4 else 0
        )

        return f'{ScaraCommandType.WAIT.value} {wait_ms}ms'

    def decode_motor_config(self, *, payload: bytes) -> str:
        '''
            Decodes motor mode configuration payload into human-readable string.

            :param payload: Packed motor configuration bytes.
            :return: Formatted motor configuration command string.
        '''
        mode_int, _ = self._unpacker.unpack_motor_config(payload)
        mode: MotorDriveMode = MotorConfigFactory.from_wire_mode(mode_int)

        return f'{ScaraCommandType.CONFIG.value} MOTOR {mode.value}'

    def decode_system(self, *, msg_id: int) -> str:
        '''
            Decodes system command message into symbolic command string.

            :param msg_id: System message identifier integer.
            :return: System command name or empty string.
        '''
        return self._system_names.get(msg_id, '')

    def decode_fallback(self, *, payload: bytes) -> str:
        '''
            Decodes unrecognized or raw payloads into hexadecimal string.

            :param payload: Unrecognized binary payload bytes.
            :return: Formatted hex string representation.
        '''
        return f'payload={payload.hex()}' if payload else ''

    def decode_detail(self, *, frame: BinaryFrame) -> str:
        '''
            Dispatches binary frame to dedicated message decoder.

            :param frame: BinaryFrame instance to decode.
            :return: Human-readable decoded detail string.
        '''
        msg_id: int = int(frame.msg_id)

        match msg_id:
            case MessageId.CMD_MOVE_JOINT_STEPS:
                return self.decode_joint_steps(payload=frame.payload)
            case MessageId.CMD_TOOL_PUMP | MessageId.CMD_TOOL_VALVE:
                return self.decode_tool_command(msg_id=msg_id, payload=frame.payload)
            case MessageId.CMD_WAIT:
                return self.decode_wait(payload=frame.payload)
            case MessageId.CMD_CONFIG_MOTOR:
                return self.decode_motor_config(payload=frame.payload)
            case _ if msg_id in self._system_names:
                return self.decode_system(msg_id=msg_id)
            case _:
                return self.decode_fallback(payload=frame.payload)
