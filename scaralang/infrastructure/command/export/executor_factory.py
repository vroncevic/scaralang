# -*- coding: UTF-8 -*-

'''
Module
    executor_factory.py
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

from scaralang.core.service.compiler.plan.iscara_plan_compiler import IScaraPlanCompiler
from scaralang.core.service.compiler.plan.scara_plan_compiler_factory import ScaraPlanCompilerFactory
from scaralang.core.service.exporter.iscara_exporter import IScaraExporter
from scaralang.core.service.exporter.scara_exporter_factory import ScaraExporterFactory
from scaralang.infrastructure.command.export.definition import ExportCommandDefinition
from scaralang.infrastructure.command.export.error.export_error_handler_factory import ExportErrorHandlerFactory
from scaralang.infrastructure.command.export.error.iexport_error_handler import IExportErrorHandler
from scaralang.infrastructure.command.export.executor import ExportCommandExecutor
from scaralang.infrastructure.command.icommand_definition import ICommandDefinition

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.6'
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
        service: IScaraPlanCompiler,
        dispatcher: IScaraExporter,
        error_handler: IExportErrorHandler,
    ) -> ExportCommandExecutor:
        '''
            Builds and returns an ExportCommandExecutor with strictly injected dependencies.

            :param definition: Required ICommandDefinition protocol instance.
            :param service: Required IScaraPlanCompiler protocol instance.
            :param dispatcher: Required IScaraExporter protocol instance.
            :param error_handler: Required IExportErrorHandler protocol instance.
            :return: Fully wired ExportCommandExecutor instance.
            :exceptions: None.
        '''
        return ExportCommandExecutor(
            definition=definition,
            service=service,
            dispatcher=dispatcher,
            error_handler=error_handler,
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
            service=ScaraPlanCompilerFactory.create_default(),
            dispatcher=ScaraExporterFactory.create_default(),
            error_handler=ExportErrorHandlerFactory.create(),
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory version string.

            :return: Factory version string.
            :exceptions: None.
        '''
        return __version__
