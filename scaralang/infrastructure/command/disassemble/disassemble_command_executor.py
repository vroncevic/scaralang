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
from typing import Final

from scaralang.core.model.dsl.binary.disassembled_frame import DisassembledFrame
from scaralang.core.model.dsl.binary.disassembly_summary import DisassemblySummary
from scaralang.core.service.dsl.iscara_dsl_disassembler import IScaraDslDisassembler
from scaralang.infrastructure.command.disassemble.format.idisassemble_summary_formatter import IDisassembleSummaryFormatter
from scaralang.infrastructure.command.icommand_definition import ICommandDefinition

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DisassembleCommandExecutor:
    '''
        Command executor strategy for disassembling binary frame files into
        readable instruction listings.

        It defines:

            :attributes:
                | definition - The command CLI metadata definition.
                | _summary_formatter - Injected summary presentation formatter.
            :methods:
                | execute - Executes the disassemble command.
                | get_definition - Returns the command definition metadata.
    '''

    definition: ICommandDefinition
    _summary_formatter: IDisassembleSummaryFormatter

    def __init__(
        self,
        *,
        definition: ICommandDefinition,
        summary_formatter: IDisassembleSummaryFormatter,
    ) -> None:
        '''
            Initializes the disassemble command executor.

            :param definition: The command definition metadata.
            :param summary_formatter: Injected summary presentation formatter.
            :exceptions: None.
        '''
        self.definition: Final[ICommandDefinition] = definition
        self._summary_formatter: Final[IDisassembleSummaryFormatter] = summary_formatter

    def execute(
        self,
        *,
        params: Mapping[str, object],
        service: IScaraDslDisassembler,
    ) -> Mapping[str, object]:
        '''
            Executes the disassemble subcommand.

            :param params: Subcommand parameters from CLI parser.
            :param service: SCARA DSL service instance.
            :return: The result of the subcommand execution.
            :exceptions: None.
        '''
        try:
            raw_file = params.get('file')
            file_path: str = str(raw_file) if isinstance(raw_file, str) else ''

            if not file_path or not exists(file_path):
                return {
                    'returncode': 1,
                    'stdout': '',
                    'stderr': (
                        f'disassemble_command_executor: binary file does not exist: {file_path}'
                    ),
                }

            with open(file_path, 'rb') as f:
                data: bytes = f.read()

            disassembled: tuple[DisassembledFrame, ...] = service.disassemble_bytes(data=data)
            lines: list[str] = [f'Disassembly of {file_path} ({len(disassembled)} frames):']

            for item in disassembled:
                lines.append(
                    f'[{item.index:04d}] SEQ={item.seq_num:03d} '
                    f'MSG={item.msg_name:<20} | {item.detail}'
                )

            if bool(params.get('summary')):
                summary: DisassemblySummary = service.calculate_disassembly_summary(
                    frames=disassembled, byte_count=len(data)
                )
                summary_text: str = self._summary_formatter.format_summary(
                    summary=summary
                )
                lines.append('')
                lines.append(summary_text)

            return {'returncode': 0, 'stdout': '\n'.join(lines), 'stderr': ''}

        except (OSError, ValueError, TypeError, KeyError) as exc:
            return {'returncode': 1, 'stdout': '', 'stderr': f'disassemble error: {exc}'}

    def get_definition(self) -> ICommandDefinition:
        '''
            Returns the command definition metadata.

            :return: The command definition metadata.
            :exceptions: None.
        '''
        return self.definition
