# -*- coding: UTF-8 -*-

'''
Module
    disassemble_command_executor.py
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
    Command executor for disassembling binary frames.
'''

from __future__ import annotations

from collections.abc import Mapping
from os.path import exists

from scaralang.core.model.protocol.binary_frame import BinaryFrame
from scaralang.core.model.protocol.message_id import MessageId
from scaralang.core.model.protocol.tool_id import ToolId
from scaralang.core.service.dsl.iscara_dsl_service import IScaraDslService
from scaralang.core.service.protocol.ibinary_frame_parser import IBinaryFrameParser
from scaralang.infrastructure.command.icommand_definition import ICommandDefinition
from scaralang.infrastructure.communication.protocol.binary.parser.binary_frame_parser_factory import BinaryFrameParserFactory
from scaralang.infrastructure.communication.protocol.binary.parser.binary_payload_unpacker import BinaryPayloadUnpacker

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DisassembleCommandExecutor:
    '''
        Command executor strategy for disassembling binary frame files into readable instruction listings.

        It defines:

            :attributes:
                | definition - The command CLI metadata definition.
            :methods:
                | execute - Executes the disassemble command.
                | get_definition - Returns the command definition metadata.
    '''

    definition: ICommandDefinition

    def __init__(self, definition: ICommandDefinition) -> None:
        '''
            Initializes the disassemble command executor.

            :param definition: The command definition metadata.
            :exceptions: None.
        '''
        self.definition = definition

    def execute(
        self,
        *,
        params: Mapping[str, object],
        service: IScaraDslService
    ) -> Mapping[str, object]:
        '''
            Executes the disassemble subcommand.

            :param params: Subcommand parameters from CLI parser.
            :param service: SCARA DSL service instance.
            :return: The result of the subcommand execution.
            :exceptions: None.
        '''
        try:
            file_path: str | None = params.get('file')  # type: ignore[assignment]
            if not file_path or not isinstance(file_path, str) or not exists(file_path):
                return {
                    'returncode': 1,
                    'stdout': '',
                    'stderr': f'disassemble_command_executor: binary file does not exist: {file_path}'
                }

            with open(file_path, 'rb') as f:
                data: bytes = f.read()

            parser: IBinaryFrameParser = BinaryFrameParserFactory.create()
            frames: list[BinaryFrame] = list(parser.feed_bytes(data))

            lines: list[str] = [f'Disassembly of {file_path} ({len(frames)} frames):']
            for i, frame in enumerate(frames):
                msg_name = 'UNKNOWN'
                try:
                    msg_name = MessageId(frame.msg_id).name
                except ValueError:
                    pass

                detail = ''
                if frame.msg_id == int(MessageId.CMD_MOVE_JOINT_STEPS):
                    steps = BinaryPayloadUnpacker.unpack_joint_steps(frame.payload)
                    detail = (
                        f'J1={steps.target_j1_steps} J2={steps.target_j2_steps} '
                        f'Z={steps.target_z_steps} J4={steps.target_j4_steps} '
                        f'dur={steps.duration_us}us'
                    )
                elif frame.msg_id in (int(MessageId.CMD_TOOL_PUMP), int(MessageId.CMD_TOOL_VALVE)):
                    _, state = BinaryPayloadUnpacker.unpack_tool_cmd(frame.payload)
                    tool_name = 'PUMP' if frame.msg_id == int(MessageId.CMD_TOOL_PUMP) else 'VALVE'
                    detail = f'{tool_name} {"ON" if state else "OFF"}'
                elif frame.msg_id == int(MessageId.CMD_WAIT):
                    wait_ms = int.from_bytes(frame.payload[:4], byteorder='little') if len(frame.payload) >= 4 else 0
                    detail = f'WAIT {wait_ms}ms'
                elif frame.msg_id == int(MessageId.CMD_HOME):
                    detail = 'HOME'
                else:
                    detail = f'payload={frame.payload.hex()}'

                lines.append(f'[{i:04d}] SEQ={frame.seq_num:03d} MSG={msg_name:<20} | {detail}')

            return {'returncode': 0, 'stdout': '\n'.join(lines), 'stderr': ''}

        except Exception as exc:
            return {'returncode': 1, 'stdout': '', 'stderr': f'disassemble error: {exc}'}

    def get_definition(self) -> ICommandDefinition:
        '''
            Returns the command definition metadata.

            :return: The command definition metadata.
            :exceptions: None.
        '''
        return self.definition
