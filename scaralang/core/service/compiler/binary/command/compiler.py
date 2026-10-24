# -*- coding: UTF-8 -*-

'''
Module
    compiler.py
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
    Compiles auxiliary hardware commands (PUMP, VALVE, WAIT, HOME, MOTOR) into binary frames and steps.
'''

from __future__ import annotations

from typing import ClassVar, Final

from scaralang.core.model.dsl.ast.command_type import ScaraCommandType
from scaralang.core.model.dsl.binary.step import BinaryStep
from scaralang.core.model.dsl.compiler.command_token import ParsedCommandToken
from scaralang.core.model.exceptions.semantic import ScaraSemanticError
from scaralang.core.model.kinematics.pose.steps import JointStepCoordinates
from scaralang.core.model.protocol.frame import BinaryFrame
from scaralang.core.model.protocol.message import MessageId
from scaralang.core.model.protocol.tool import ToolId
from scaralang.core.service.compiler.binary.command.actuator.ibuilder import IActuatorFrameBuilder
from scaralang.core.service.compiler.binary.command.compiler_dependencies import CommandCompilerDependencies
from scaralang.core.service.compiler.binary.command.tokens.iparser import ITokenParser
from scaralang.core.service.compiler.binary.command.tool.ibuilder import IToolFrameBuilder
from scaralang.core.service.protocol.ipacker import IBinaryFramePacker
from scaralang.core.service.protocol.isystem_builder import IBinarySystemFrameBuilder

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class CommandCompiler:
    '''
        Compiles semantic hardware commands into binary wire frames and binary steps.

        It defines:

            :attributes:
                | _frame_builder - Binary system frame builder protocol.
                | _frame_packer - Binary wire frame packer protocol.
                | _tool_frame_builder - Tool frame builder protocol.
                | _actuator_frame_builder - Actuator frame builder protocol.
                | _token_parser - Waypoint command token parser protocol.
            :methods:
                | __init__ - Initializes command step compiler with injected builders and packer.
                | compile_command_step - Compiles a single hardware command into a binary step.
                | get_version - Gets implementation version string.
    '''

    _DEFAULT_WAIT_MS: ClassVar[int] = 100
    _DEFAULT_STEP_DURATION_US: ClassVar[int] = 50000
    _ZERO_TARGET_STEPS: ClassVar[JointStepCoordinates] = JointStepCoordinates(
        j1=0, j2=0, z=0, j4=0
    )

    _SYSTEM_MSG_IDS: ClassVar[dict[str, MessageId]] = {
        ScaraCommandType.HOME: MessageId.CMD_HOME,
        ScaraCommandType.ENABLE: MessageId.CMD_ENABLE,
        ScaraCommandType.DISABLE: MessageId.CMD_DISABLE,
        ScaraCommandType.HOLD: MessageId.CMD_HOLD,
        ScaraCommandType.RESUME: MessageId.CMD_RESUME,
        ScaraCommandType.ESTOP: MessageId.CMD_ESTOP,
    }

    _frame_builder: IBinarySystemFrameBuilder
    _frame_packer: IBinaryFramePacker
    _tool_frame_builder: IToolFrameBuilder
    _actuator_frame_builder: IActuatorFrameBuilder
    _token_parser: ITokenParser

    def __init__(self, *, dependencies: CommandCompilerDependencies) -> None:
        '''
            Initializes command step compiler with injected dependencies bundle.

            :param dependencies: Injected CommandCompilerDependencies parameter bundle.
            :exceptions: None.
        '''
        self._frame_builder: Final[IBinarySystemFrameBuilder] = dependencies.frame_builder
        self._frame_packer: Final[IBinaryFramePacker] = dependencies.frame_packer
        self._tool_frame_builder: Final[IToolFrameBuilder] = dependencies.tool_frame_builder
        self._actuator_frame_builder: Final[IActuatorFrameBuilder] = dependencies.actuator_frame_builder
        self._token_parser: Final[ITokenParser] = dependencies.token_parser

    def compile_command_step(
        self,
        *,
        command: str,
        seq_num: int,
        line_num: int,
    ) -> BinaryStep:
        '''
            Compiles a semantic command string into a binary command step.

            :param command: Command text (e.g. PUMP, VALVE, WAIT, HOME, MOTOR).
            :param seq_num: Cyclic sequence counter.
            :param line_num: Source line index.
            :return: Compiled BinaryStep.
            :exceptions: ScaraSemanticError on unsupported command name.
        '''
        token: ParsedCommandToken = self._token_parser.parse(command=command)
        frame: BinaryFrame

        match token.cmd_name:
            case ScaraCommandType.PUMP:
                frame = self._tool_frame_builder.build_tool_frame(
                    tool_id=ToolId.PUMP,
                    arg=token.arg,
                    clean=token.clean,
                    seq_num=seq_num,
                )

            case ScaraCommandType.VALVE:
                frame = self._tool_frame_builder.build_tool_frame(
                    tool_id=ToolId.VALVE,
                    arg=token.arg,
                    clean=token.clean,
                    seq_num=seq_num,
                )

            case ScaraCommandType.WAIT | ScaraCommandType.WAIT_MS:
                ms: int = self._DEFAULT_WAIT_MS

                for part in token.parts[1:]:
                    if part.isdigit():
                        ms = int(part)
                        break

                frame = self._frame_builder.build_wait_cmd(
                    delay_ms=ms,
                    seq_num=seq_num,
                )

            case ScaraCommandType.CONFIG_MOTOR:
                frame = self._actuator_frame_builder.build_actuator_frame(
                    arg=token.arg,
                    seq_num=seq_num,
                )

            case name if name in self._SYSTEM_MSG_IDS:
                frame = self._frame_builder.build_system_cmd(
                    msg_id=self._SYSTEM_MSG_IDS[name],
                    seq_num=seq_num,
                )

            case _:
                raise ScaraSemanticError(
                    f'Unsupported command: {token.cmd_name} at line {line_num}'
                )

        raw_bytes: bytes = self._frame_packer.pack_frame(frame=frame)

        return BinaryStep(
            frame=frame,
            raw_bytes=raw_bytes,
            duration_us=self._DEFAULT_STEP_DURATION_US,
            target_steps=self._ZERO_TARGET_STEPS,
            description=f'COMMAND: {command}',
            line_number=line_num,
        )

    def get_version(self) -> str:
        '''
            Gets implementation version string.

            :return: Version string.
            :exceptions: None.
        '''
        return __version__
