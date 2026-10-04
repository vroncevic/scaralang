# -*- coding: UTF-8 -*-

'''
Module
    repl_command_bundle.py
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
    Defines collaborator bundle dataclass for ReplCommandExecutor.
'''

from __future__ import annotations

from dataclasses import dataclass

from scaralang.infrastructure.cli.repl.compiler.irepl_single_command_compiler import IReplSingleCommandCompiler
from scaralang.infrastructure.cli.repl.dispatch.irepl_command_dispatcher import IReplCommandDispatcher
from scaralang.infrastructure.cli.repl.input.irepl_line_reader import IReplLineReader
from scaralang.infrastructure.cli.repl.output.irepl_output_writer import IReplOutputWriter
from scaralang.infrastructure.cli.repl.presentation.irepl_response_presenter import IReplResponsePresenter
from scaralang.infrastructure.cli.repl.transmission.irepl_frame_transmitter import IReplFrameTransmitter

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(frozen=True, slots=True, kw_only=True)
class ReplCommandBundle:
    '''
        Bundle containing collaborators required by ReplCommandExecutor.

        It defines:

            :attributes:
                | reader - Injected IReplLineReader protocol instance.
                | writer - Injected IReplOutputWriter protocol instance.
                | dispatcher - Injected IReplCommandDispatcher protocol instance.
                | compiler - Injected IReplSingleCommandCompiler protocol instance.
                | transmitter - Injected IReplFrameTransmitter protocol instance.
                | presenter - Injected IReplResponsePresenter protocol instance.
            :methods: None.
    '''

    reader: IReplLineReader
    writer: IReplOutputWriter
    dispatcher: IReplCommandDispatcher
    compiler: IReplSingleCommandCompiler
    transmitter: IReplFrameTransmitter
    presenter: IReplResponsePresenter
