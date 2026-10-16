# -*- coding: UTF-8 -*-

'''
Module
    formatter.py
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
    Defines PayloadDispatcherFormatter dispatching payload formatting to domain formatters.
'''

from __future__ import annotations

from typing import Final

from scaralang.core.model.motor.motor_drive_mode import MotorDriveMode
from scaralang.core.model.protocol.joint_steps import JointSteps
from scaralang.core.model.protocol.message_id import MessageId
from scaralang.core.service.motor.wire_mode_converter import WireModeConverter
from scaralang.core.service.protocol.ibinary_actuator_payload_unpacker import IBinaryActuatorPayloadUnpacker
from scaralang.core.service.protocol.ibinary_motion_payload_unpacker import IBinaryMotionPayloadUnpacker
from scaralang.infrastructure.command.compile.inspection.hex.iformatter import IHexStreamFormatter
from scaralang.infrastructure.command.compile.inspection.payload.dispatch.dependencies import DispatchDependencies
from scaralang.infrastructure.command.compile.inspection.payload.joint.iformatter import IJointStepsPayloadFormatter
from scaralang.infrastructure.command.compile.inspection.payload.tool.iformatter import IToolCommandPayloadFormatter

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.9'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class PayloadDispatcherFormatter:
    '''
        Routes payload formatting to specialized formatters or emits generic hex dump.

        It defines:

            :attributes:
                | _joint_formatter - Injected motion joint steps formatter.
                | _tool_formatter - Injected pneumatic tool command formatter.
                | _hex_formatter - Injected raw hex stream formatter.
                | _motion_unpacker - Injected motion payload unpacker.
                | _actuator_unpacker - Injected actuator payload unpacker.
            :methods:
                | __init__ - Initializes dispatcher with injected collaborating formatters.
                | format_payload - Dispatches payload to specialized formatter.
                | get_version - Returns the component version string.
    '''

    _joint_formatter: IJointStepsPayloadFormatter
    _tool_formatter: IToolCommandPayloadFormatter
    _hex_formatter: IHexStreamFormatter
    _motion_unpacker: IBinaryMotionPayloadUnpacker
    _actuator_unpacker: IBinaryActuatorPayloadUnpacker

    def __init__(self, *, dependencies: DispatchDependencies) -> None:
        '''
            Initializes PayloadDispatcherFormatter with injected dependency bundle.

            :param dependencies: Required DispatchDependencies bundle.
        '''
        self._joint_formatter: Final[IJointStepsPayloadFormatter] = (
            dependencies.joint_formatter
        )
        self._tool_formatter: Final[IToolCommandPayloadFormatter] = (
            dependencies.tool_formatter
        )
        self._hex_formatter: Final[IHexStreamFormatter] = (
            dependencies.hex_formatter
        )
        self._motion_unpacker: Final[IBinaryMotionPayloadUnpacker] = (
            dependencies.motion_unpacker
        )
        self._actuator_unpacker: Final[IBinaryActuatorPayloadUnpacker] = (
            dependencies.actuator_unpacker
        )

    def format_payload(self, *, msg_id: MessageId, payload: bytes) -> str:
        '''
            Routes payload formatting to specialized formatters or emits generic hex dump.

            :param msg_id: Message type identifier.
            :param payload: Raw wire payload bytes.
            :return: Formatted presentation string.
        '''
        if msg_id == MessageId.CMD_MOVE_JOINT_STEPS:
            steps: JointSteps = self._motion_unpacker.unpack_joint_steps(payload)
            return self._joint_formatter.format_joint_steps(steps=steps, raw_payload=payload)

        if msg_id in (MessageId.CMD_TOOL_PUMP, MessageId.CMD_TOOL_VALVE):
            tool_id, state = self._actuator_unpacker.unpack_tool_cmd(payload)
            return self._tool_formatter.format_tool_cmd(
                tool_id=tool_id,
                state=state,
                raw_payload=payload,
            )

        if msg_id == MessageId.CMD_CONFIG_MOTOR:
            mode_int, axes = self._actuator_unpacker.unpack_motor_config(payload)
            mode: MotorDriveMode = WireModeConverter.from_wire_mode(mode_int)
            return f'  - Motor Mode:    {mode.value} (axes=0x{axes:02X})'

        if payload:
            hex_str: str = self._hex_formatter.format_bytes(data=payload)
            return f'  - Payload Hex:   {hex_str}'

        return '  - Payload:       (None)'

    def get_version(self) -> str:
        '''
            Returns the component version string.

            :return: The version string.
        '''
        return __version__
