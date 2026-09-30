# -*- coding: UTF-8 -*-

'''
Module
    export_command_executor_factory.py
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
    Factory instantiating ExportCommandExecutor instances.
'''

from __future__ import annotations

from scaralang.core.service.exporter.export_target_dispatcher_factory import ExportTargetDispatcherFactory
from scaralang.core.service.exporter.iexport_target_dispatcher import IExportTargetDispatcher
from scaralang.infrastructure.command.export.export_command_definition import ExportCommandDefinition
from scaralang.infrastructure.command.export.export_command_executor import ExportCommandExecutor
from scaralang.infrastructure.command.icommand_definition import ICommandDefinition

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ExportCommandExecutorFactory:
    '''
        Factory providing ExportCommandExecutor instances.

        It defines:

            :methods:
                | create - Builds ExportCommandExecutor with strictly injected collaborators.
                | create_default - Builds ExportCommandExecutor with default collaborators.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(
        cls,
        *,
        definition: ICommandDefinition,
        dispatcher: IExportTargetDispatcher,
    ) -> ExportCommandExecutor:
        '''
            Builds and returns an ExportCommandExecutor with strictly injected dependencies.

            :param definition: Required ICommandDefinition protocol instance.
            :param dispatcher: Required IExportTargetDispatcher protocol instance.
            :return: Fully wired ExportCommandExecutor instance.
            :exceptions: None.
        '''
        return ExportCommandExecutor(
            definition=definition,
            dispatcher=dispatcher,
        )

    @classmethod
    def create_default(cls) -> ExportCommandExecutor:
        '''
            Builds and returns an ExportCommandExecutor instance with default dependencies.

            :return: Fully wired ExportCommandExecutor instance.
            :exceptions: None.
        '''
        return ExportCommandExecutor(
            definition=ExportCommandDefinition(),
            dispatcher=ExportTargetDispatcherFactory.create_default(),
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory version string.

            :return: Factory version string.
            :exceptions: None.
        '''
        return __version__
