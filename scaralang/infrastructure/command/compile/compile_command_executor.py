# -*- coding: UTF-8 -*-

'''
Module
    compile_command_executor.py
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
    Command executor for compiling SCARA DSL scripts into binary frames.
'''

from __future__ import annotations

from collections.abc import Mapping
from os.path import exists

from scaralang.core.model.dsl.binary.binary_program_telemetry import BinaryProgramTelemetry
from scaralang.core.model.dsl.binary.program import BinaryProgram
from scaralang.core.service.dsl.iscara_dsl_binary_compiler import IScaraDslBinaryCompiler
from scaralang.infrastructure.command.compile.telemetry.icompile_telemetry_formatter import ICompileTelemetryFormatter
from scaralang.infrastructure.command.compile.inspection.presentation.iprogram_inspection_presenter import IProgramInspectionPresenter
from scaralang.infrastructure.command.icommand_definition import ICommandDefinition

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class CompileCommandExecutor:
    '''
        Command executor strategy for compiling .scara scripts into binary frame streams.

        It defines:

            :attributes:
                | definition - The command CLI metadata definition.
                | _inspection_presenter - Injected binary program inspection presenter.
                | _telemetry_formatter - Injected binary telemetry formatter.
            :methods:
                | execute - Executes the compile command.
                | get_definition - Returns the command definition metadata.
    '''

    definition: ICommandDefinition
    _inspection_presenter: IProgramInspectionPresenter
    _telemetry_formatter: ICompileTelemetryFormatter

    def __init__(
        self,
        *,
        definition: ICommandDefinition,
        inspection_presenter: IProgramInspectionPresenter,
        telemetry_formatter: ICompileTelemetryFormatter,
    ) -> None:
        '''
            Initializes the compile command executor.

            :param definition: The command definition metadata.
            :param inspection_presenter: Injected binary inspection presenter.
            :param telemetry_formatter: Injected binary telemetry formatter.
            :exceptions: None.
        '''
        self.definition = definition
        self._inspection_presenter = inspection_presenter
        self._telemetry_formatter = telemetry_formatter

    def execute(
        self,
        *,
        params: Mapping[str, object],
        service: IScaraDslBinaryCompiler
    ) -> Mapping[str, object]:
        '''
            Executes the compilation subcommand.

            :param params: Subcommand parameters from CLI parser.
            :param service: SCARA DSL service instance.
            :return: The result of the subcommand execution.
        '''
        try:
            raw_script = params.get('script')
            script_path: str = str(raw_script) if isinstance(raw_script, str) else ''

            if not script_path or not exists(script_path):
                return {
                    'returncode': 1,
                    'stdout': '',
                    'stderr': (
                        f'compile_command_executor: script file does not exist: {script_path}'
                    ),
                }

            with open(script_path, 'r', encoding='utf-8') as f:
                source_code: str = f.read()

            program: BinaryProgram = service.compile_to_binary(source=source_code)
            binary_bytes: bytes = program.raw_bytes
            raw_output = params.get('output')
            output_path: str | None = (
                str(raw_output) if isinstance(raw_output, str) and raw_output.strip()
                else None
            )

            if output_path is not None:
                with open(output_path, 'wb') as f_out:
                    f_out.write(binary_bytes)
                msg: str = f'Compiled {len(binary_bytes)} bytes written to {output_path}'
            elif bool(params.get('hex')):
                msg = binary_bytes.hex()
            else:
                msg = f'Successfully compiled {len(binary_bytes)} binary wire bytes'

            if bool(params.get('verbose')):
                telemetry: BinaryProgramTelemetry = service.get_program_telemetry(
                    program=program
                )
                formatted_telemetry: str = self._telemetry_formatter.format_telemetry(
                    telemetry=telemetry
                )
                msg = f'{msg}\n\n{formatted_telemetry}'

            if bool(params.get('dump_frames')):
                inspection: str = self._inspection_presenter.present_program(program=program)
                msg = f'{msg}\n\n{inspection}'

            return {'returncode': 0, 'stdout': msg, 'stderr': ''}

        except (OSError, ValueError, TypeError, KeyError) as exc:
            return {'returncode': 1, 'stdout': '', 'stderr': f'compile error: {exc}'}

    def get_definition(self) -> ICommandDefinition:
        '''
            Returns the command definition metadata.

            :return: The command definition metadata.
        '''
        return self.definition
