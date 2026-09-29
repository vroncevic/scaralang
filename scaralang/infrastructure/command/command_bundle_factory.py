# -*- coding: UTF-8 -*-

'''
Module
    command_bundle_factory.py
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
    Factory instantiating and wiring CLI CommandBundle instances.
'''

from __future__ import annotations

from scaralang.core.service.dsl.iscara_dsl_service import IScaraDslService
from scaralang.core.service.exporter.export_target_dispatcher_factory import ExportTargetDispatcherFactory
from scaralang.core.service.linter.diagnostic.scara_diagnostic_formatter_factory import ScaraDiagnosticFormatterFactory
from scaralang.infrastructure.command.command_bundle import CommandBundle
from scaralang.infrastructure.command.compile.compile_command_definition import CompileCommandDefinition
from scaralang.infrastructure.command.compile.compile_command_executor_factory import CompileCommandExecutorFactory
from scaralang.infrastructure.command.compile.inspection.presentation.program_inspection_presenter_factory import ProgramInspectionPresenterFactory
from scaralang.infrastructure.command.compile.telemetry.compile_telemetry_formatter_factory import CompileTelemetryFormatterFactory
from scaralang.infrastructure.command.disassemble.disassemble_command_definition import DisassembleCommandDefinition
from scaralang.infrastructure.command.disassemble.disassemble_command_executor_factory import DisassembleCommandExecutorFactory
from scaralang.infrastructure.command.disassemble.format.disassemble_summary_formatter_factory import DisassembleSummaryFormatterFactory
from scaralang.infrastructure.command.export.export_command_definition import ExportCommandDefinition
from scaralang.infrastructure.command.export.export_command_executor_factory import ExportCommandExecutorFactory
from scaralang.infrastructure.command.info.info_command_definition import InfoCommandDefinition
from scaralang.infrastructure.command.info.info_command_executor_factory import InfoCommandExecutorFactory
from scaralang.infrastructure.command.lint.lint_command_definition import LintCommandDefinition
from scaralang.infrastructure.command.lint.lint_command_executor_factory import LintCommandExecutorFactory
from scaralang.infrastructure.command.repl.repl_command_definition import ReplCommandDefinition
from scaralang.infrastructure.command.repl.repl_command_executor_factory import ReplCommandExecutorFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class CommandBundleFactory:
    '''
        Factory providing wired CommandBundle instances for CLI subcommands.

        It defines:

            :methods:
                | create_commands - Builds list of all 6 CLI CommandBundle instances.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create_commands(cls, *, service: IScaraDslService) -> list[CommandBundle]:
        '''
            Builds and returns all CLI command bundles wired with their executors.

            :param service: Injected IScaraDslService domain service facade.
            :return: List of configured CommandBundle instances.
            :exceptions: None.
        '''
        compile_def = CompileCommandDefinition()
        compile_exec = CompileCommandExecutorFactory.create(
            definition=compile_def,
            inspection_presenter=ProgramInspectionPresenterFactory.create(),
            telemetry_formatter=CompileTelemetryFormatterFactory.create(),
        )

        lint_def = LintCommandDefinition()
        lint_exec = LintCommandExecutorFactory.create(
            definition=lint_def,
            diagnostic_formatter=ScaraDiagnosticFormatterFactory.create(),
        )

        disasm_def = DisassembleCommandDefinition()
        disasm_exec = DisassembleCommandExecutorFactory.create(
            definition=disasm_def,
            summary_formatter=DisassembleSummaryFormatterFactory.create(),
        )

        info_def = InfoCommandDefinition()
        info_exec = InfoCommandExecutorFactory.create(definition=info_def)

        export_def = ExportCommandDefinition()
        export_exec = ExportCommandExecutorFactory.create(
            definition=export_def,
            dispatcher=ExportTargetDispatcherFactory.create_default(),
        )

        repl_def = ReplCommandDefinition()
        repl_exec = ReplCommandExecutorFactory.create_default(
            service=service, definition=repl_def
        )

        return [
            CommandBundle(definition=compile_def, executor=compile_exec),
            CommandBundle(definition=lint_def, executor=lint_exec),
            CommandBundle(definition=disasm_def, executor=disasm_exec),
            CommandBundle(definition=info_def, executor=info_exec),
            CommandBundle(definition=export_def, executor=export_exec),
            CommandBundle(definition=repl_def, executor=repl_exec),
        ]

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory version string.

            :return: Factory version string.
            :exceptions: None.
        '''
        return __version__
