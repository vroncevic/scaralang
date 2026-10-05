# -*- coding: UTF-8 -*-

'''
Module
    executor.py
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
from typing import Final

from scaralang.core.model.dsl.binary.binary_program_telemetry import BinaryProgramTelemetry
from scaralang.core.model.dsl.binary.program import BinaryProgram
from scaralang.core.model.exceptions.scara_error import ScaraError
from scaralang.core.service.compiler.iscara_compiler import IScaraCompiler
from scaralang.infrastructure.command.compile.bundle import CompileCommandBundle
from scaralang.infrastructure.command.compile.error.icompile_error_handler import ICompileErrorHandler
from scaralang.infrastructure.command.compile.telemetry.icompile_telemetry_formatter import ICompileTelemetryFormatter
from scaralang.infrastructure.command.compile.inspection.presentation.iprogram_inspection_presenter import IProgramInspectionPresenter
from scaralang.infrastructure.command.icommand_definition import ICommandDefinition

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.5'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class CompileCommandExecutor:
    '''
        Command executor strategy for compiling .scara scripts into binary frame streams.

        It defines:

            :attributes:
                | _definition - The command CLI metadata definition.
                | _compiler - Injected binary compiler service.
                | _inspection_presenter - Injected binary program inspection presenter.
                | _telemetry_formatter - Injected binary telemetry formatter.
                | _error_handler - Injected compile error handler.
            :methods:
                | execute - Executes the compile command.
                | get_definition - Returns the command definition metadata.
    '''

    _definition: ICommandDefinition
    _compiler: IScaraCompiler
    _inspection_presenter: IProgramInspectionPresenter
    _telemetry_formatter: ICompileTelemetryFormatter
    _error_handler: ICompileErrorHandler

    def __init__(
        self,
        *,
        definition: ICommandDefinition,
        bundle: CompileCommandBundle,
    ) -> None:
        '''
            Initializes the compile command executor.

            :param definition: The command definition metadata.
            :param bundle: Injected collaborator bundle.
            :exceptions: None.
        '''
        self._definition: Final[ICommandDefinition] = definition
        self._compiler: Final[IScaraCompiler] = bundle.compiler
        self._inspection_presenter: Final[IProgramInspectionPresenter] = bundle.inspection_presenter
        self._telemetry_formatter: Final[ICompileTelemetryFormatter] = bundle.telemetry_formatter
        self._error_handler: Final[ICompileErrorHandler] = bundle.error_handler

    def execute(
        self,
        *,
        params: Mapping[str, object],
    ) -> Mapping[str, object]:
        '''
            Executes the compilation subcommand.

            :param params: Subcommand parameters from CLI parser.
            :return: The result of the subcommand execution.
        '''
        try:
            script_path: str = str(params.get('script') or '')

            if not script_path or not exists(script_path):
                return {
                    'returncode': 1,
                    'stdout': '',
                    'stderr': self._error_handler.format_file_missing(path=script_path),
                }

            with open(script_path, 'r', encoding='utf-8') as f:
                source_code: str = f.read()

            program: BinaryProgram = self._compiler.compile_to_binary(source=source_code)
            raw_bytes: bytes = program.raw_bytes
            output_path: str = str(params.get('output') or '').strip()

            if output_path:
                with open(output_path, 'wb') as f_out:
                    f_out.write(raw_bytes)
                msg: str = f'Compiled {len(raw_bytes)} bytes written to {output_path}'
            elif bool(params.get('hex')):
                msg = raw_bytes.hex()
            else:
                msg = f'Successfully compiled {len(raw_bytes)} binary wire bytes'

            if bool(params.get('verbose')):
                telemetry: BinaryProgramTelemetry = self._compiler.get_program_telemetry(
                    program=program
                )
                msg = f'{msg}\n\n{self._telemetry_formatter.format_telemetry(telemetry=telemetry)}'

            if bool(params.get('dump_frames')):
                msg = f'{msg}\n\n{self._inspection_presenter.present_program(program=program)}'

            return {'returncode': 0, 'stdout': msg, 'stderr': ''}

        except (ScaraError, OSError, ValueError, TypeError, KeyError) as exc:
            return {
                'returncode': self._error_handler.resolve_return_code(error=exc),
                'stdout': '',
                'stderr': self._error_handler.format_error(error=exc),
            }

    def get_definition(self) -> ICommandDefinition:
        '''
            Returns the command definition metadata.

            :return: The command definition metadata.
        '''
        return self._definition
