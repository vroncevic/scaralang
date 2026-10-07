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
    Command executor for decompiling binary frames into SCARA DSL scripts.
'''

from __future__ import annotations

from collections.abc import Mapping
from os.path import exists
from typing import Final

from scaralang.core.model.exceptions.scara_error import ScaraError
from scaralang.core.service.decompiler.iscara_decompiler import IScaraDecompiler
from scaralang.infrastructure.command.decompile.error.idecompile_error_handler import IDecompileErrorHandler
from scaralang.infrastructure.command.icommand_definition import ICommandDefinition

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.7'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DecompileCommandExecutor:
    '''
        Command executor strategy for decompiling binary frame streams into
        high-level SCARA DSL scripts.

        It defines:

            :attributes:
                | _definition - The command CLI metadata definition.
                | _service - Injected SCARA decompiler service protocol.
                | _error_handler - Injected decompile error handler protocol.
            :methods:
                | execute - Executes the decompile command.
                | get_definition - Returns the command definition metadata.
    '''

    _definition: ICommandDefinition
    _service: IScaraDecompiler
    _error_handler: IDecompileErrorHandler

    def __init__(
        self,
        *,
        definition: ICommandDefinition,
        service: IScaraDecompiler,
        error_handler: IDecompileErrorHandler,
    ) -> None:
        '''
            Initializes the decompile command executor.

            :param definition: The command definition metadata.
            :param service: Injected SCARA decompiler service protocol.
            :param error_handler: Injected decompile error handler protocol.
            :exceptions: None.
        '''
        self._definition: Final[ICommandDefinition] = definition
        self._service: Final[IScaraDecompiler] = service
        self._error_handler: Final[IDecompileErrorHandler] = error_handler

    def execute(
        self,
        *,
        params: Mapping[str, object],
    ) -> Mapping[str, object]:
        '''
            Executes the decompile subcommand.

            :param params: Subcommand parameters from CLI parser.
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
                    'stderr': self._error_handler.format_file_missing(path=file_path),
                }

            with open(file_path, 'rb') as bin_file:
                data: bytes = bin_file.read()

            dsl_script: str = self._service.decompile(data=data)

            raw_output = params.get('output')
            output_path: str = str(raw_output) if isinstance(raw_output, str) else ''

            if output_path:
                with open(output_path, 'w', encoding='utf-8') as out_file:
                    out_file.write(dsl_script)
                return {
                    'returncode': 0,
                    'stdout': f'Decompiled {len(data)} bytes to {output_path}',
                    'stderr': '',
                }

            return {'returncode': 0, 'stdout': dsl_script, 'stderr': ''}

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
