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

from scaralang.core.service.dsl.iscara_dsl_service import IScaraDslService
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
            :methods:
                | execute - Executes the compile command.
                | get_definition - Returns the command definition metadata.
    '''

    definition: ICommandDefinition

    def __init__(self, definition: ICommandDefinition) -> None:
        '''
            Initializes the compile command executor.

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
            Executes the compilation subcommand.

            :param params: Subcommand parameters from CLI parser.
            :param service: SCARA DSL service instance.
            :return: The result of the subcommand execution.
            :exceptions: None.
        '''
        try:
            script_path: str | None = params.get('script')  # type: ignore[assignment]
            if not script_path or not isinstance(script_path, str) or not exists(script_path):
                return {
                    'returncode': 1,
                    'stdout': '',
                    'stderr': f'compile_command_executor: script file does not exist: {script_path}'
                }

            with open(script_path, 'r', encoding='utf-8') as f:
                source_code: str = f.read()

            binary_bytes: bytes = service.compile_to_bytes(source=source_code)
            output_path: str | None = params.get('output')  # type: ignore[assignment]

            if output_path and isinstance(output_path, str) and output_path.strip():
                with open(output_path, 'wb') as f_out:
                    f_out.write(binary_bytes)
                msg: str = f'Compiled {len(binary_bytes)} bytes written to {output_path}'
            elif bool(params.get('hex')):
                msg = binary_bytes.hex()
            else:
                msg = f'Successfully compiled {len(binary_bytes)} binary wire bytes'

            return {'returncode': 0, 'stdout': msg, 'stderr': ''}

        except Exception as exc:
            return {'returncode': 1, 'stdout': '', 'stderr': f'compile error: {exc}'}

    def get_definition(self) -> ICommandDefinition:
        '''
            Returns the command definition metadata.

            :return: The command definition metadata.
            :exceptions: None.
        '''
        return self.definition
