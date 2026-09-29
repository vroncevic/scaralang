# -*- coding: UTF-8 -*-

'''
Module
    repl_command_executor_factory.py
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
    Factory instantiating ReplCommandExecutor instances with sub-factory DI.
'''

from __future__ import annotations

from collections.abc import Callable

from scaralang.core.service.dsl.iscara_dsl_service import IScaraDslService
from scaralang.infrastructure.cli.repl.compiler.irepl_single_command_compiler import IReplSingleCommandCompiler
from scaralang.infrastructure.cli.repl.compiler.repl_single_command_compiler_factory import ReplSingleCommandCompilerFactory
from scaralang.infrastructure.cli.repl.dispatch.irepl_command_dispatcher import IReplCommandDispatcher
from scaralang.infrastructure.cli.repl.dispatch.repl_command_dispatcher_factory import ReplCommandDispatcherFactory
from scaralang.infrastructure.cli.repl.input.irepl_line_reader import IReplLineReader
from scaralang.infrastructure.cli.repl.input.repl_line_reader_factory import ReplLineReaderFactory
from scaralang.infrastructure.cli.repl.presentation.irepl_response_presenter import IReplResponsePresenter
from scaralang.infrastructure.cli.repl.presentation.repl_response_presenter_factory import ReplResponsePresenterFactory
from scaralang.infrastructure.cli.repl.transmission.irepl_frame_transmitter import IReplFrameTransmitter
from scaralang.infrastructure.cli.repl.transmission.repl_frame_transmitter_factory import ReplFrameTransmitterFactory
from scaralang.infrastructure.command.icommand_definition import ICommandDefinition
from scaralang.infrastructure.command.repl.repl_command_executor import ReplCommandExecutor

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ReplCommandExecutorFactory:
    '''
        Factory providing ReplCommandExecutor instances.

        It defines:

            :methods:
                | create - Builds ReplCommandExecutor with strictly injected collaborators.
                | create_default - Builds ReplCommandExecutor with default collaborators.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(
        cls,
        *,
        definition: ICommandDefinition,
        reader: IReplLineReader,
        dispatcher: IReplCommandDispatcher,
        compiler: IReplSingleCommandCompiler,
        transmitter: IReplFrameTransmitter,
        presenter: IReplResponsePresenter,
        output_func: Callable[[str], None],
    ) -> ReplCommandExecutor:
        '''
            Builds and returns a ReplCommandExecutor with strictly injected dependencies.

            :param definition: Required command definition metadata.
            :param reader: Required line reader protocol instance.
            :param dispatcher: Required command dispatcher protocol instance.
            :param compiler: Required single-instruction compiler protocol instance.
            :param transmitter: Required wire frame transmitter protocol instance.
            :param presenter: Required terminal presenter protocol instance.
            :param output_func: Required output emission callable.
            :return: Fully wired ReplCommandExecutor instance.
            :exceptions: None.
        '''
        return ReplCommandExecutor(
            definition=definition,
            reader=reader,
            dispatcher=dispatcher,
            compiler=compiler,
            transmitter=transmitter,
            presenter=presenter,
            output_func=output_func,
        )

    @classmethod
    def create_default(
        cls,
        *,
        service: IScaraDslService,
        definition: ICommandDefinition,
    ) -> ReplCommandExecutor:
        '''
            Builds and returns a ReplCommandExecutor instance with default dependencies.

            :param service: SCARA DSL service instance.
            :param definition: Injected command definition metadata.
            :return: Fully wired ReplCommandExecutor instance.
            :exceptions: None.
        '''
        return ReplCommandExecutor(
            definition=definition,
            reader=ReplLineReaderFactory.create_default(),
            dispatcher=ReplCommandDispatcherFactory.create(),
            compiler=ReplSingleCommandCompilerFactory.create(service=service),
            transmitter=ReplFrameTransmitterFactory.create(),
            presenter=ReplResponsePresenterFactory.create(),
            output_func=print,
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory version string.

            :return: Factory version string.
            :exceptions: None.
        '''
        return __version__
