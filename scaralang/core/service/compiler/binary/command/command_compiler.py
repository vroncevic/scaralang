# -*- coding: UTF-8 -*-

'''
Module
    command_compiler.py
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
from scaralang.core.model.dsl.binary.parsed_command_token import ParsedCommandToken
from scaralang.core.model.dsl.binary.step import Step
from scaralang.core.model.protocol.binary_frame import BinaryFrame
from scaralang.core.model.protocol.message_id import MessageId
from scaralang.core.model.protocol.tool_id import ToolId
from scaralang.core.service.compiler.binary.command.motor.imotor_frame_builder import IMotorFrameBuilder
from scaralang.core.service.compiler.binary.command.tokens.icommand_token_parser import ICommandTokenParser
from scaralang.core.service.compiler.binary.command.tool.itool_frame_builder import IToolFrameBuilder
from scaralang.core.service.protocol.ibinary_frame_builder import IBinaryFrameBuilder

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class CommandCompiler:
    '''
        Compiles semantic hardware commands into binary wire frames and binary steps.

        It defines:

            :attributes:
                | _frame_builder - Binary frame assembler protocol.
                | _tool_frame_builder - Tool frame builder protocol.
                | _motor_frame_builder - Motor frame builder protocol.
                | _token_parser - Waypoint command token parser protocol.
            :methods:
                | __init__ - Initializes command step compiler with injected builders.
                | compile_command_step - Compiles a single hardware command into a binary step.
    '''

    _DEFAULT_WAIT_MS: ClassVar[int] = 100
    _DEFAULT_STEP_DURATION_US: ClassVar[int] = 50000
    _ZERO_TARGET_STEPS: ClassVar[tuple[int, int, int, int]] = (0, 0, 0, 0)

    _SYSTEM_MSG_IDS: ClassVar[dict[str, MessageId]] = {
        ScaraCommandType.HOME: MessageId.CMD_HOME,
        ScaraCommandType.ENABLE: MessageId.CMD_ENABLE,
        ScaraCommandType.DISABLE: MessageId.CMD_DISABLE,
        ScaraCommandType.HOLD: MessageId.CMD_HOLD,
        ScaraCommandType.RESUME: MessageId.CMD_RESUME,
        ScaraCommandType.ESTOP: MessageId.CMD_ESTOP,
    }

    _frame_builder: IBinaryFrameBuilder
    _tool_frame_builder: IToolFrameBuilder
    _motor_frame_builder: IMotorFrameBuilder
    _token_parser: ICommandTokenParser

    def __init__(
        self,
        *,
        frame_builder: IBinaryFrameBuilder,
        tool_frame_builder: IToolFrameBuilder,
        motor_frame_builder: IMotorFrameBuilder,
        token_parser: ICommandTokenParser,
    ) -> None:
        '''
            Initializes command step compiler with injected builders and parser.

            :param frame_builder: Injected IBinaryFrameBuilder protocol.
            :param tool_frame_builder: Injected IToolFrameBuilder protocol.
            :param motor_frame_builder: Injected IMotorFrameBuilder protocol.
            :param token_parser: Injected ICommandTokenParser protocol.
            :exceptions: None.
        '''
        self._frame_builder: Final[IBinaryFrameBuilder] = frame_builder
        self._tool_frame_builder: Final[IToolFrameBuilder] = tool_frame_builder
        self._motor_frame_builder: Final[IMotorFrameBuilder] = motor_frame_builder
        self._token_parser: Final[ICommandTokenParser] = token_parser

    def compile_command_step(
        self,
        *,
        command: str,
        seq_num: int,
        line_num: int,
    ) -> Step:
        '''
            Compiles a semantic command string into a binary command step.

            :param command: Command text (e.g. PUMP, VALVE, WAIT, HOME, MOTOR).
            :param seq_num: Cyclic sequence counter.
            :param line_num: Source line index.
            :return: Compiled Step.
            :exceptions: None.
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
                frame = self._motor_frame_builder.build_motor_frame(
                    arg=token.arg,
                    seq_num=seq_num,
                )

            case name if name in self._SYSTEM_MSG_IDS:
                frame = self._frame_builder.build_system_cmd(
                    msg_id=self._SYSTEM_MSG_IDS[name],
                    seq_num=seq_num,
                )

            case _:
                frame = self._frame_builder.build_system_cmd(
                    msg_id=MessageId.CMD_PING,
                    seq_num=seq_num,
                )

        raw_bytes: bytes = self._frame_builder.pack_frame(frame=frame)

        return Step(
            frame=frame,
            raw_bytes=raw_bytes,
            duration_us=self._DEFAULT_STEP_DURATION_US,
            target_steps=self._ZERO_TARGET_STEPS,
            description=f'COMMAND: {command}',
            line_number=line_num,
        )
