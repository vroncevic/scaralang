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
    Command executor for exporting SCARA DSL trajectories to external formats.
'''

from __future__ import annotations

from collections.abc import Mapping
from os.path import exists
from typing import Final

from scaralang.core.model.dsl.exporter.export_format import ExportFormat
from scaralang.core.model.exceptions.scara_error import ScaraError
from scaralang.core.service.compiler.plan.iscara_plan_compiler import IScaraPlanCompiler
from scaralang.core.service.exporter.iscara_exporter import IScaraExporter
from scaralang.infrastructure.command.export.error.iexport_error_handler import IExportErrorHandler
from scaralang.infrastructure.command.icommand_definition import ICommandDefinition

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.5'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ExportCommandExecutor:
    '''
        Command executor for exporting trajectories into external formats.

        It defines:

            :attributes:
                | _definition - The command CLI metadata definition.
                | _service - SCARA plan compiler service protocol instance.
                | _dispatcher - Trajectory export target dispatcher protocol instance.
                | _error_handler - Trajectory export error handler protocol instance.
            :methods:
                | __init__ - Initializes the export command executor.
                | execute - Executes the export command.
                | get_definition - Returns the command definition metadata.
    '''

    _definition: ICommandDefinition
    _service: IScaraPlanCompiler
    _dispatcher: IScaraExporter
    _error_handler: IExportErrorHandler

    def __init__(
        self,
        *,
        definition: ICommandDefinition,
        service: IScaraPlanCompiler,
        dispatcher: IScaraExporter,
        error_handler: IExportErrorHandler,
    ) -> None:
        '''
            Initializes the export command executor.

            :param definition: The command definition metadata.
            :param service: SCARA plan compiler service protocol instance.
            :param dispatcher: Trajectory export target dispatcher protocol instance.
            :param error_handler: Trajectory export error handler protocol instance.
            :exceptions: None.
        '''
        self._definition: Final[ICommandDefinition] = definition
        self._service: Final[IScaraPlanCompiler] = service
        self._dispatcher: Final[IScaraExporter] = dispatcher
        self._error_handler: Final[IExportErrorHandler] = error_handler

    def execute(
        self,
        *,
        params: Mapping[str, object],
    ) -> Mapping[str, object]:
        '''
            Executes the export subcommand.

            :param params: Subcommand parameters from CLI parser.
            :return: The result of the subcommand execution.
            :exceptions: None.
        '''
        try:
            raw_script = params.get('script')
            script_path: str = str(raw_script) if isinstance(raw_script, str) else ''

            if not script_path or not exists(script_path):
                return {
                    'returncode': 1,
                    'stdout': '',
                    'stderr': self._error_handler.format_file_missing(path=script_path),
                }

            with open(script_path, 'r', encoding='utf-8') as f:
                source_code: str = f.read()

            format_str: str = str(params.get('format', 'gcode')).upper()
            target_format: ExportFormat = ExportFormat[format_str]

            plan = self._service.compile_script(source=source_code)
            exported_content: str = self._dispatcher.export(
                plan=plan, target_format=target_format
            )

            raw_output = params.get('output')
            output_path: str | None = (
                str(raw_output) if isinstance(raw_output, str) and raw_output.strip()
                else None
            )

            if output_path is not None:
                with open(output_path, 'w', encoding='utf-8') as f_out:
                    f_out.write(exported_content)
                msg: str = f'Exported {target_format.value} written to {output_path}'
            else:
                msg = exported_content

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
            :exceptions: None.
        '''
        return self._definition
