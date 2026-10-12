# -*- coding: UTF-8 -*-

'''
Module
    factory.py
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

from scaralang.infrastructure.command.bundle import CommandBundle
from scaralang.infrastructure.command.compile.factory import CompileFactory
from scaralang.infrastructure.command.compile.provides import CompileProvides
from scaralang.infrastructure.command.decompile.factory import DecompileFactory
from scaralang.infrastructure.command.decompile.provides import DecompileProvides
from scaralang.infrastructure.command.disassemble.factory import DisassembleFactory
from scaralang.infrastructure.command.disassemble.provides import DisassembleProvides
from scaralang.infrastructure.command.export.factory import ExportFactory
from scaralang.infrastructure.command.export.provides import ExportProvides
from scaralang.infrastructure.command.info.factory import InfoFactory
from scaralang.infrastructure.command.info.provides import InfoProvides
from scaralang.infrastructure.command.lint.factory import LintFactory
from scaralang.infrastructure.command.lint.provides import LintProvides
from scaralang.infrastructure.command.provides import CommandProvides
from scaralang.infrastructure.command.repl.factory import ReplFactory
from scaralang.infrastructure.command.repl.provides import ReplProvides

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.8'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class CommandFactory:
    '''
        Factory providing wired CommandProvides instances for CLI subcommands.

        It defines:

            :methods:
                | create - Builds and returns CommandProvides container with all 7 CLI bundles.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(cls) -> CommandProvides:
        '''
            Builds and returns all CLI command bundles wired with their executors.

            :return: Configured CommandProvides container.
            :exceptions: None.
        '''
        compile_provides: CompileProvides = CompileFactory.create()
        decompile_provides: DecompileProvides = DecompileFactory.create()
        disassemble_provides: DisassembleProvides = DisassembleFactory.create()
        export_provides: ExportProvides = ExportFactory.create()
        info_provides: InfoProvides = InfoFactory.create()
        lint_provides: LintProvides = LintFactory.create()
        repl_provides: ReplProvides = ReplFactory.create()

        commands: tuple[CommandBundle, ...] = (
            CommandBundle(
                definition=compile_provides.definition,
                executor=compile_provides.executor,
            ),
            CommandBundle(
                definition=decompile_provides.definition,
                executor=decompile_provides.executor,
            ),
            CommandBundle(
                definition=lint_provides.definition,
                executor=lint_provides.executor,
            ),
            CommandBundle(
                definition=disassemble_provides.definition,
                executor=disassemble_provides.executor,
            ),
            CommandBundle(
                definition=info_provides.definition,
                executor=info_provides.executor,
            ),
            CommandBundle(
                definition=export_provides.definition,
                executor=export_provides.executor,
            ),
            CommandBundle(
                definition=repl_provides.definition,
                executor=repl_provides.executor,
            ),
        )

        return CommandProvides(commands=commands)

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory version string.

            :return: Factory version string.
            :exceptions: None.
        '''
        return __version__
