# -*- coding: UTF-8 -*-

'''
Module
    compile_command_executor_factory.py
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
    Factory instantiating CompileCommandExecutor instances with injected dependencies.
'''

from __future__ import annotations

from scaralang.core.service.compiler.dsl.iscara_dsl_binary_compiler import IScaraDslBinaryCompiler
from scaralang.core.service.compiler.dsl.scara_dsl_binary_compiler_factory import ScaraDslBinaryCompilerFactory
from scaralang.infrastructure.command.compile.compile_command_definition import CompileCommandDefinition
from scaralang.infrastructure.command.compile.compile_command_executor import CompileCommandExecutor
from scaralang.infrastructure.command.compile.inspection.presentation.iprogram_inspection_presenter import IProgramInspectionPresenter
from scaralang.infrastructure.command.compile.inspection.presentation.program_inspection_presenter_factory import ProgramInspectionPresenterFactory
from scaralang.infrastructure.command.compile.telemetry.compile_telemetry_formatter_factory import CompileTelemetryFormatterFactory
from scaralang.infrastructure.command.compile.telemetry.icompile_telemetry_formatter import ICompileTelemetryFormatter
from scaralang.infrastructure.command.icommand_definition import ICommandDefinition

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class CompileCommandExecutorFactory:
    '''
        Factory providing CompileCommandExecutor instances.

        It defines:

            :methods:
                | create - Builds CompileCommandExecutor with strictly injected collaborators.
                | create_default - Builds CompileCommandExecutor with default collaborators.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(
        cls,
        *,
        definition: ICommandDefinition,
        service: IScaraDslBinaryCompiler,
        inspection_presenter: IProgramInspectionPresenter,
        telemetry_formatter: ICompileTelemetryFormatter,
    ) -> CompileCommandExecutor:
        '''
            Builds and returns a CompileCommandExecutor with strictly injected dependencies.

            :param definition: Required ICommandDefinition protocol instance.
            :param service: Required IScaraDslBinaryCompiler protocol instance.
            :param inspection_presenter: Required IProgramInspectionPresenter protocol instance.
            :param telemetry_formatter: Required ICompileTelemetryFormatter protocol instance.
            :return: Fully wired CompileCommandExecutor instance.
            :exceptions: None.
        '''
        return CompileCommandExecutor(
            definition=definition,
            service=service,
            inspection_presenter=inspection_presenter,
            telemetry_formatter=telemetry_formatter,
        )

    @classmethod
    def create_default(cls) -> CompileCommandExecutor:
        '''
            Builds and returns a CompileCommandExecutor instance with default dependencies.

            :return: Fully wired CompileCommandExecutor instance.
            :exceptions: None.
        '''
        return CompileCommandExecutor(
            definition=CompileCommandDefinition(),
            service=ScaraDslBinaryCompilerFactory.create_default(),
            inspection_presenter=ProgramInspectionPresenterFactory.create(),
            telemetry_formatter=CompileTelemetryFormatterFactory.create(),
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory version string.

            :return: Factory version string.
            :exceptions: None.
        '''
        return __version__
