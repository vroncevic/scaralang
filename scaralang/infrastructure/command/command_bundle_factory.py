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

from scaralang.infrastructure.command.command_bundle import CommandBundle
from scaralang.infrastructure.command.compile.executor_factory import CompileCommandExecutorFactory
from scaralang.infrastructure.command.decompile.executor_factory import DecompileCommandExecutorFactory
from scaralang.infrastructure.command.disassemble.executor_factory import DisassembleCommandExecutorFactory
from scaralang.infrastructure.command.export.executor_factory import ExportCommandExecutorFactory
from scaralang.infrastructure.command.info.executor_factory import InfoCommandExecutorFactory
from scaralang.infrastructure.command.lint.executor_factory import LintCommandExecutorFactory
from scaralang.infrastructure.command.repl.executor_factory import ReplCommandExecutorFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.7'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class CommandBundleFactory:
    '''
        Factory providing wired CommandBundle instances for CLI subcommands.

        It defines:

            :methods:
                | create_commands - Builds list of all 7 CLI CommandBundle instances.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create_commands(cls) -> list[CommandBundle]:
        '''
            Builds and returns all CLI command bundles wired with their executors.

            :return: List of configured CommandBundle instances.
            :exceptions: None.
        '''
        compile_exec = CompileCommandExecutorFactory.create_default()
        decompile_exec = DecompileCommandExecutorFactory.create_default()
        lint_exec = LintCommandExecutorFactory.create_default()
        disasm_exec = DisassembleCommandExecutorFactory.create_default()
        info_exec = InfoCommandExecutorFactory.create_default()
        export_exec = ExportCommandExecutorFactory.create_default()
        repl_exec = ReplCommandExecutorFactory.create_default()

        return [
            CommandBundle(definition=compile_exec.get_definition(), executor=compile_exec),
            CommandBundle(definition=decompile_exec.get_definition(), executor=decompile_exec),
            CommandBundle(definition=lint_exec.get_definition(), executor=lint_exec),
            CommandBundle(definition=disasm_exec.get_definition(), executor=disasm_exec),
            CommandBundle(definition=info_exec.get_definition(), executor=info_exec),
            CommandBundle(definition=export_exec.get_definition(), executor=export_exec),
            CommandBundle(definition=repl_exec.get_definition(), executor=repl_exec),
        ]

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory version string.

            :return: Factory version string.
            :exceptions: None.
        '''
        return __version__
