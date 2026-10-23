# -*- coding: UTF-8 -*-

'''
Module
    frame.py
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
from typing import ClassVar, Final, Literal

from scaralang.core.model.dsl.ast.command_type import ScaraCommandType
from scaralang.core.model.dsl.ast.instruction_param import ScaraInstructionParam
from scaralang.core.model.dsl.ast.pneumatic_state import PneumaticState
from scaralang.core.model.kinematics.pose.point_2d import Point2D
from scaralang.core.model.motor.mode import MotorDriveMode
from scaralang.core.model.protocol.frame import BinaryFrame
from scaralang.core.model.protocol.joint_steps import JointSteps
from scaralang.core.model.protocol.message import MessageId
from scaralang.core.service.kinematics.solver.analytical.planar.isolver import IPlanarKinematicsSolver
from scaralang.core.service.kinematics.transmission.iconverter import IJointStepTransmissionConverter
from scaralang.core.service.motor.wire import WireModeConverter
from scaralang.core.service.protocol.iactuator_unpacker import IBinaryActuatorPayloadUnpacker
from scaralang.core.service.protocol.imotion_unpacker import IBinaryMotionPayloadUnpacker

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class FrameDecompiler:
    '''
        Service translating single binary protocol frames into SCARA DSL script commands.

        It defines:

            :attributes:
                | _WAIT_PAYLOAD_SIZE - Slicing length for 32-bit millisecond dwell.
                | _OVERRIDE_PAYLOAD_SIZE - Minimum payload bytes for speed override.
                | _JOG_PAYLOAD_SIZE - Minimum payload bytes for joint jog command.
                | _BYTE_ORDER - Endianness encoding for wire payload integers.
                | _JOINT_INDEX_OFFSET - Index offset translating 0-indexed to 1-indexed joints.
                | _SIMPLE_COMMANDS - Mapping of parameterless MessageIds to DSL commands.
                | _planar - Injected planar kinematics solver.
                | _transmission - Injected joint step conversion strategy.
                | _motion_unpacker - Injected motion payload unpacker strategy.
                | _actuator_unpacker - Injected actuator payload unpacker strategy.
            :methods:
                | __init__ - Initializes frame decompiler with injected collaborators.
                | decompile_frame - Decodes single BinaryFrame into a SCARA DSL command string.
                | get_version - Returns the frame decompiler version string.
    '''

    _WAIT_PAYLOAD_SIZE: ClassVar[int] = 4
    _OVERRIDE_PAYLOAD_SIZE: ClassVar[int] = 1
    _JOG_PAYLOAD_SIZE: ClassVar[int] = 5
    _BYTE_ORDER: ClassVar[Literal['little', 'big']] = 'little'
    _JOINT_INDEX_OFFSET: ClassVar[int] = 1

    _SIMPLE_COMMANDS: ClassVar[dict[int, str]] = {
        MessageId.CMD_HOME: ScaraCommandType.HOME.value,
        MessageId.CMD_ENABLE: ScaraCommandType.ENABLE.value,
        MessageId.CMD_DISABLE: ScaraCommandType.DISABLE.value,
        MessageId.CMD_ESTOP: ScaraCommandType.ESTOP.value,
        MessageId.CMD_HOLD: ScaraCommandType.HOLD.value,
        MessageId.CMD_RESUME: ScaraCommandType.RESUME.value,
    }

    _planar: IPlanarKinematicsSolver
    _transmission: IJointStepTransmissionConverter
    _motion_unpacker: IBinaryMotionPayloadUnpacker
    _actuator_unpacker: IBinaryActuatorPayloadUnpacker

    def __init__(
        self,
        *,
        planar: IPlanarKinematicsSolver,
        transmission: IJointStepTransmissionConverter,
        motion_unpacker: IBinaryMotionPayloadUnpacker,
        actuator_unpacker: IBinaryActuatorPayloadUnpacker,
    ) -> None:
        '''
            Initializes frame decompiler with planar solver, transmission, and unpackers.

            :param planar: Required IPlanarKinematicsSolver implementation.
            :param transmission: Required IJointStepTransmissionConverter implementation.
            :param motion_unpacker: Required IBinaryMotionPayloadUnpacker implementation.
            :param actuator_unpacker: Required IBinaryActuatorPayloadUnpacker implementation.
            :exceptions: None.
        '''
        self._planar: Final[IPlanarKinematicsSolver] = planar
        self._transmission: Final[IJointStepTransmissionConverter] = transmission
        self._motion_unpacker: Final[IBinaryMotionPayloadUnpacker] = motion_unpacker
        self._actuator_unpacker: Final[IBinaryActuatorPayloadUnpacker] = actuator_unpacker

    def decompile_frame(self, *, frame: BinaryFrame) -> str:
        '''
            Decodes a single binary frame into a SCARA DSL command string.

            :param frame: BinaryFrame instance to decompile.
            :return: Formatted SCARA DSL command string or empty string if unmapped.
            :exceptions: None.
        '''
        msg_id: int = int(frame.msg_id)

        if msg_id in self._SIMPLE_COMMANDS:
            return self._SIMPLE_COMMANDS[msg_id]

        result: str = ''

        match msg_id:
            case MessageId.CMD_TOOL_PUMP:
                state: str = (
                    PneumaticState.ON.value
                    if self._actuator_unpacker.unpack_tool_cmd(frame.payload)[1]
                    else PneumaticState.OFF.value
                )
                result = f'{ScaraCommandType.PUMP.value} {state}'

            case MessageId.CMD_TOOL_VALVE:
                state = (
                    PneumaticState.ON.value
                    if self._actuator_unpacker.unpack_tool_cmd(frame.payload)[1]
                    else PneumaticState.OFF.value
                )
                result = f'{ScaraCommandType.VALVE.value} {state}'

            case MessageId.CMD_WAIT:
                delay_ms: int = int.from_bytes(
                    frame.payload[: self._WAIT_PAYLOAD_SIZE],
                    byteorder=self._BYTE_ORDER,
                )
                result = f'{ScaraCommandType.WAIT.value} {delay_ms}'

            case MessageId.CMD_OVERRIDE if len(frame.payload) >= self._OVERRIDE_PAYLOAD_SIZE:
                result = f'{ScaraCommandType.OVERRIDE.value} {int(frame.payload[0])}'

            case MessageId.CMD_CONFIG_MOTOR:
                mode: MotorDriveMode = WireModeConverter.from_wire_mode(
                    self._actuator_unpacker.unpack_motor_config(frame.payload)[0]
                )
                result = f'{ScaraCommandType.CONFIG.value} MOTOR {mode.value}'

            case MessageId.CMD_MOVE_JOINT_STEPS:
                steps: JointSteps = self._motion_unpacker.unpack_joint_steps(frame.payload)
                angles: tuple[float, float, float, float] = self._transmission.steps_to_angles(
                    steps.target_j1_steps,
                    steps.target_j2_steps,
                    steps.target_z_steps,
                    steps.target_j4_steps,
                )
                point2d: Point2D = self._planar.solve_fk_2d(angles[0], angles[1])
                result = (
                    f'{ScaraCommandType.MOVE_L.value} '
                    f'{ScaraInstructionParam.X.value} {point2d.x:.2f} '
                    f'{ScaraInstructionParam.Y.value} {point2d.y:.2f} '
                    f'{ScaraInstructionParam.Z.value} {angles[2]:.2f} '
                    f'{ScaraInstructionParam.PHI.value} {degrees(angles[3]):.2f}'
                )

            case MessageId.CMD_JOG_JOINT if len(frame.payload) >= self._JOG_PAYLOAD_SIZE:
                step_delta: int = int.from_bytes(
                    frame.payload[1:self._JOG_PAYLOAD_SIZE],
                    byteorder=self._BYTE_ORDER,
                    signed=True,
                )
                joint_num: int = int(frame.payload[0]) + self._JOINT_INDEX_OFFSET
                result = f'{ScaraCommandType.JOG_JOINT.value} J{joint_num} {step_delta}'

        return result

    def get_version(self) -> str:
        '''
            Returns the frame decompiler version string.

            :return: Version string.
            :exceptions: None.
        '''
        return __version__
