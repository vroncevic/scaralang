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
    Factory instantiating repl command subsystem components.
'''

from __future__ import annotations

from scaralang.infrastructure.cli.repl.compiler.repl_single_command_compiler_factory import ReplSingleCommandCompilerFactory
from scaralang.infrastructure.cli.repl.dispatch.repl_command_dispatcher_factory import ReplCommandDispatcherFactory
from scaralang.infrastructure.cli.repl.input.repl_line_reader_factory import ReplLineReaderFactory
from scaralang.infrastructure.cli.repl.output.repl_output_writer_factory import ReplOutputWriterFactory
from scaralang.infrastructure.cli.repl.presentation.repl_response_presenter_factory import ReplResponsePresenterFactory
from scaralang.infrastructure.cli.repl.transmission.repl_frame_transmitter_factory import ReplFrameTransmitterFactory
from scaralang.infrastructure.command.repl.definition import ReplCommandDefinition
from scaralang.infrastructure.command.repl.dependencies import ReplDependencies
from scaralang.infrastructure.command.repl.executor import ReplCommandExecutor
from scaralang.infrastructure.command.repl.provides import ReplProvides

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ReplFactory:
    '''
        Factory providing Repl command subsystem instances.

        It defines:

            :methods:
                | create - Constructs and wires ReplProvides container.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(cls) -> ReplProvides:
        '''
            Constructs and wires ReplProvides container with configured collaborators.

            :return: Fully configured ReplProvides container.
            :exceptions: None.
        '''
        definition: ReplCommandDefinition = ReplCommandDefinition()
        deps: ReplDependencies = ReplDependencies(
            reader=ReplLineReaderFactory.create_default(),
            writer=ReplOutputWriterFactory.create_default(),
            dispatcher=ReplCommandDispatcherFactory.create_default(),
            compiler=ReplSingleCommandCompilerFactory.create_default(),
            transmitter=ReplFrameTransmitterFactory.create(),
            presenter=ReplResponsePresenterFactory.create(),
        )
        executor: ReplCommandExecutor = ReplCommandExecutor(
            definition=definition,
            dependencies=deps,
        )

        return ReplProvides(
            executor=executor,
            definition=definition,
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory version string.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return __version__
