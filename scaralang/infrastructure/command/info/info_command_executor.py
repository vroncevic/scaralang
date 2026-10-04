# -*- coding: UTF-8 -*-

'''
Module
    info_command_executor.py
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
    Command executor for displaying SCARA DSL toolchain information.
'''

from __future__ import annotations

from collections.abc import Mapping
from typing import Final

from scaralang.core.service.info.itoolchain_info_provider import IToolchainInfoProvider
from scaralang.infrastructure.command.icommand_definition import ICommandDefinition

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class InfoCommandExecutor:
    '''
        Command executor strategy for displaying toolchain and grammar info.

        It defines:

            :attributes:
                | _definition - The command CLI metadata definition.
                | _service - The toolchain info provider service.
            :methods:
                | execute - Executes the info command.
                | get_definition - Returns the command definition metadata.
    '''

    _definition: ICommandDefinition
    _service: IToolchainInfoProvider

    def __init__(
        self,
        *,
        definition: ICommandDefinition,
        service: IToolchainInfoProvider,
    ) -> None:
        '''
            Initializes the info command executor.

            :param definition: The command definition metadata.
            :param service: The toolchain info provider service.
            :exceptions: None.
        '''
        self._definition: Final[ICommandDefinition] = definition
        self._service: Final[IToolchainInfoProvider] = service

    def execute(
        self,
        *,
        params: Mapping[str, object],
    ) -> Mapping[str, object]:
        '''
            Executes the info subcommand.

            :param params: Subcommand parameters from CLI parser.
            :return: The result of the subcommand execution.
            :exceptions: None.
        '''
        verbose: bool = bool(params.get('verbose'))
        lines: tuple[str, ...] = self._service.get_toolchain_info(verbose=verbose)

        return {'returncode': 0, 'stdout': '\n'.join(lines), 'stderr': ''}

    def get_definition(self) -> ICommandDefinition:
        '''
            Returns the command definition metadata.

            :return: The command definition metadata.
            :exceptions: None.
        '''
        return self._definition
