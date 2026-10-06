# -*- coding: UTF-8 -*-

'''
Module
    frame_decompiler.py
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
    Service translating single binary wire frames into SCARA DSL command text.
'''

from __future__ import annotations

from math import degrees
from typing import Final

from scaralang.core.model.kinematics.point_2d import Point2D
from scaralang.core.model.motor.motor_drive_mode import MotorDriveMode
from scaralang.core.model.protocol.binary_frame import BinaryFrame
from scaralang.core.model.protocol.joint_steps import JointSteps
from scaralang.core.model.protocol.message_id import MessageId
from scaralang.core.service.kinematics.ikinematics_service import IKinematicsService
from scaralang.core.service.kinematics.transmission.ijoint_step_transmission_converter import IJointStepTransmissionConverter
from scaralang.core.service.motor.motor_config_factory import MotorConfigFactory
from scaralang.core.service.protocol.ibinary_payload_unpacker import IBinaryPayloadUnpacker

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.6'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class FrameDecompiler:
    '''
        Service translating single binary protocol frames into SCARA DSL script commands.

        It defines:

            :attributes:
                | _kinematics - Injected kinematics calculation service.
                | _transmission - Injected joint step conversion strategy.
                | _unpacker - Injected binary payload deserialization adapter.
            :methods:
                | __init__ - Initializes frame decompiler with injected collaborators.
                | decompile_frame - Decodes single BinaryFrame into a SCARA DSL command string.
                | get_version - Returns the frame decompiler version string.
    '''

    _kinematics: IKinematicsService
    _transmission: IJointStepTransmissionConverter
    _unpacker: IBinaryPayloadUnpacker

    def __init__(
        self,
        *,
        kinematics: IKinematicsService,
        transmission: IJointStepTransmissionConverter,
        unpacker: IBinaryPayloadUnpacker,
    ) -> None:
        '''
            Initializes frame decompiler with kinematics, transmission, and unpacker.

            :param kinematics: Required IKinematicsService implementation.
            :param transmission: Required IJointStepTransmissionConverter implementation.
            :param unpacker: Required IBinaryPayloadUnpacker implementation.
            :exceptions: None.
        '''
        self._kinematics: Final[IKinematicsService] = kinematics
        self._transmission: Final[IJointStepTransmissionConverter] = transmission
        self._unpacker: Final[IBinaryPayloadUnpacker] = unpacker

    def decompile_frame(self, *, frame: BinaryFrame) -> str:
        '''
            Decodes a single binary frame into a SCARA DSL command string.

            :param frame: BinaryFrame instance to decompile.
            :return: Formatted SCARA DSL command string or empty string if unmapped.
            :exceptions: None.
        '''
        msg_id: int = int(frame.msg_id)
        result: str = ''

        match msg_id:
            case MessageId.CMD_HOME:
                result = 'HOME'
            case MessageId.CMD_ENABLE:
                result = 'ENABLE'
            case MessageId.CMD_DISABLE:
                result = 'DISABLE'
            case MessageId.CMD_ESTOP:
                result = 'ESTOP'
            case MessageId.CMD_HOLD:
                result = 'HOLD'
            case MessageId.CMD_RESUME:
                result = 'RESUME'
            case MessageId.CMD_TOOL_PUMP:
                result = 'PUMP ON' if self._unpacker.unpack_tool_cmd(frame.payload)[1] else 'PUMP OFF'
            case MessageId.CMD_TOOL_VALVE:
                result = 'VALVE ON' if self._unpacker.unpack_tool_cmd(frame.payload)[1] else 'VALVE OFF'
            case MessageId.CMD_WAIT:
                delay_ms: int = int.from_bytes(frame.payload[:4], byteorder='little')
                result = f'WAIT {delay_ms}'
            case MessageId.CMD_OVERRIDE if len(frame.payload) >= 1:
                result = f'OVERRIDE {int(frame.payload[0])}'
            case MessageId.CMD_CONFIG_MOTOR:
                mode: MotorDriveMode = MotorConfigFactory.from_wire_mode(
                    self._unpacker.unpack_motor_config(frame.payload)[0]
                )
                result = f'CONFIG MOTOR {mode.value}'
            case MessageId.CMD_MOVE_JOINT_STEPS:
                steps: JointSteps = self._unpacker.unpack_joint_steps(frame.payload)
                angles: tuple[float, float, float, float] = self._transmission.steps_to_angles(
                    steps.target_j1_steps,
                    steps.target_j2_steps,
                    steps.target_z_steps,
                    steps.target_j4_steps,
                )
                point2d: Point2D = self._kinematics.solve_fk(angles[0], angles[1])
                result = (
                    f'MOVE_L X {point2d.x:.2f} Y {point2d.y:.2f} Z {angles[2]:.2f} '
                    f'PHI {degrees(angles[3]):.2f}'
                )
            case MessageId.CMD_JOG_JOINT if len(frame.payload) >= 5:
                step_delta: int = int.from_bytes(
                    frame.payload[1:5], byteorder='little', signed=True
                )
                result = f'JOG_JOINT J{int(frame.payload[0]) + 1} {step_delta}'

        return result

    def get_version(self) -> str:
        '''
            Returns the frame decompiler version string.

            :return: Version string.
            :exceptions: None.
        '''
        return __version__
