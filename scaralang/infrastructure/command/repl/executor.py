# -*- coding: UTF-8 -*-

'''
Module
    executor.py
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
    Command executor for launching the interactive SCARA DSL REPL console.
'''

from __future__ import annotations

from collections.abc import Mapping
from typing import Final

from scaralang.core.model.exceptions.scara_error import ScaraError
from scaralang.core.model.repl.repl_session_context import ReplSessionContext
from scaralang.infrastructure.cli.repl.compiler.irepl_single_command_compiler import IReplSingleCommandCompiler
from scaralang.infrastructure.cli.repl.dispatch.irepl_command_dispatcher import IReplCommandDispatcher
from scaralang.infrastructure.cli.repl.input.irepl_line_reader import IReplLineReader
from scaralang.infrastructure.cli.repl.output.irepl_output_writer import IReplOutputWriter
from scaralang.infrastructure.cli.repl.presentation.irepl_response_presenter import IReplResponsePresenter
from scaralang.infrastructure.cli.repl.transmission.irepl_frame_transmitter import IReplFrameTransmitter
from scaralang.infrastructure.command.icommand_definition import ICommandDefinition
from scaralang.infrastructure.command.repl.bundle import ReplCommandBundle

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ReplCommandExecutor:
    '''
        Command executor orchestrating the interactive REPL event loop.

        It defines:

            :attributes:
                | _definition - The command CLI metadata definition.
                | _reader - Line reader protocol instance.
                | _writer - Output writer protocol instance.
                | _dispatcher - Command dispatcher protocol instance.
                | _compiler - Single-instruction compiler protocol instance.
                | _transmitter - Wire frame transmitter protocol instance.
                | _presenter - Terminal response presenter protocol instance.
            :methods:
                | __init__ - Initializes the REPL command executor.
                | execute - Executes the REPL command from CLI arguments.
                | run_session - Executes the REPL read-eval-print loop.
                | emit - Emits text to output writer.
                | get_definition - Returns the command definition metadata.
    '''

    _definition: ICommandDefinition
    _reader: IReplLineReader
    _writer: IReplOutputWriter
    _dispatcher: IReplCommandDispatcher
    _compiler: IReplSingleCommandCompiler
    _transmitter: IReplFrameTransmitter
    _presenter: IReplResponsePresenter

    def __init__(
        self,
        *,
        definition: ICommandDefinition,
        bundle: ReplCommandBundle,
    ) -> None:
        '''
            Initializes the REPL command executor with injected collaborators.

            :param definition: Injected command definition metadata.
            :param bundle: Injected collaborator bundle container.
            :exceptions: None.
        '''
        self._definition: Final[ICommandDefinition] = definition
        self._reader: Final[IReplLineReader] = bundle.reader
        self._writer: Final[IReplOutputWriter] = bundle.writer
        self._dispatcher: Final[IReplCommandDispatcher] = bundle.dispatcher
        self._compiler: Final[IReplSingleCommandCompiler] = bundle.compiler
        self._transmitter: Final[IReplFrameTransmitter] = bundle.transmitter
        self._presenter: Final[IReplResponsePresenter] = bundle.presenter

    def execute(
        self,
        *,
        params: Mapping[str, object],
    ) -> Mapping[str, object]:
        '''
            Executes the REPL subcommand.

            :param params: Subcommand parameters from CLI parser.
            :return: The result mapping of the subcommand execution.
            :exceptions: None.
        '''
        raw_endpoint = params.get('endpoint')

        if isinstance(raw_endpoint, str) and raw_endpoint.strip():
            dry_run: bool = bool(params.get('dry_run', False))
            self._transmitter.configure(
                endpoint=raw_endpoint.strip(), dry_run=dry_run
            )

        context: ReplSessionContext = ReplSessionContext()
        code, lines = self.run_session(initial_context=context)

        return {'returncode': code, 'stdout': '\n'.join(lines), 'stderr': ''}

    def run_session(
        self,
        *,
        initial_context: ReplSessionContext,
    ) -> tuple[int, list[str]]:
        '''
            Executes the REPL read-eval-print loop with injected components.

            :param initial_context: Initial session context.
            :return: Tuple of (exit code, output lines).
            :exceptions: None.
        '''
        output_lines: list[str] = []
        banner: str = self._presenter.present_banner()
        self.emit(banner)
        output_lines.append(banner)
        context: ReplSessionContext = initial_context

        while True:
            line: str | None = self._reader.read_line(prompt='scaralang> ')

            if line is None:
                break

            if not line:
                continue

            dispatch = self._dispatcher.dispatch_line(line=line, context=context)

            if dispatch.is_exit:
                break

            if dispatch.is_handled:
                if dispatch.message:
                    self.emit(dispatch.message)
                    output_lines.append(dispatch.message)

                continue

            try:
                _, step, context = self._compiler.compile_instruction(
                    line=line, context=context
                )
                self._transmitter.transmit_frame(raw_bytes=step.raw_bytes)
                msg: str = self._presenter.present_success(step=step, context=context)
                self.emit(msg)
                output_lines.append(msg)

            except (ScaraError, ValueError, TypeError, KeyError) as exc:
                err_msg: str = self._presenter.present_error(error=str(exc))
                self.emit(err_msg)
                output_lines.append(err_msg)

        exit_msg: str = self._presenter.present_exit()
        self.emit(exit_msg)
        output_lines.append(exit_msg)

        return 0, output_lines

    def emit(self, text: str) -> None:
        '''
            Emits output text to configured output writer.

            :param text: Output text to emit.
            :exceptions: None.
        '''
        self._writer.write(text)

    def get_definition(self) -> ICommandDefinition:
        '''
            Returns the command definition metadata.

            :return: The command definition metadata.
            :exceptions: None.
        '''
        return self._definition
