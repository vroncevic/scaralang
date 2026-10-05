# -*- coding: UTF-8 -*-

'''
Module
    irepl_command_dispatcher.py
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
    Defines IReplCommandDispatcher protocol for routing REPL input lines.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from scaralang.core.model.repl.repl_dispatch_result import ReplDispatchResult
from scaralang.core.model.repl.repl_session_context import ReplSessionContext

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IReplCommandDispatcher(Protocol):
    '''
        Protocol for identifying and routing REPL commands and instructions.

        It defines:

            :methods:
                | dispatch_line - Routes line to session handlers or flags for DSL.
                | format_help - Returns formatted help text for REPL commands and syntax.
                | format_status - Returns formatted status text for active session state.
                | format_pose - Returns formatted Cartesian pose string.
    '''

    def dispatch_line(
        self,
        *,
        line: str,
        context: ReplSessionContext,
    ) -> ReplDispatchResult:
        '''
            Dispatches line to built-in session handlers or flags for DSL compilation.

            :param line: Input command line string.
            :param context: Active REPL session context model.
            :return: ReplDispatchResult model capturing dispatch outcome.
            :exceptions: None.
        '''

    def format_help(self) -> str:
        '''
            Returns formatted help text for REPL commands and syntax.

            :return: Multiline help string.
            :exceptions: None.
        '''

    def format_status(self, *, context: ReplSessionContext) -> str:
        '''
            Returns formatted status text for active session state.

            :param context: Active REPL session context model.
            :return: Multiline status string.
            :exceptions: None.
        '''

    def format_pose(self, *, context: ReplSessionContext) -> str:
        '''
            Returns formatted Cartesian pose string.

            :param context: Active REPL session context model.
            :return: Single-line Cartesian pose string.
            :exceptions: None.
        '''
