# -*- coding: UTF-8 -*-

'''
Module
    repl_command_dispatcher.py
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
    Concrete implementation of REPL command dispatcher.
'''

from __future__ import annotations

from typing import Final

from scaralang.core.model.repl.result import ReplDispatchResult
from scaralang.core.model.repl.context import ReplSessionContext
from scaralang.core.service.info.iinfo import IScaraInfoProvider
from scaralang.infrastructure.cli.repl.presentation.irepl_status_presenter import IReplStatusPresenter

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ReplCommandDispatcher:
    '''
        Command dispatcher routing user inputs between built-in commands and DSL compilation.

        It defines:

            :attributes:
                | _info_provider - Injected toolchain metadata and instruction catalog provider.
                | _status_presenter - Injected presenter for status, manual and pose output.
            :methods:
                | __init__ - Initializes dispatcher with injected info provider and presenter.
                | dispatch_line - Dispatches line to built-in session handlers or flags for DSL.
                | get_version - Returns dispatcher version string.
    '''

    _info_provider: IScaraInfoProvider
    _status_presenter: IReplStatusPresenter

    def __init__(
        self,
        *,
        info_provider: IScaraInfoProvider,
        status_presenter: IReplStatusPresenter,
    ) -> None:
        '''
            Initializes REPL command dispatcher with injected collaborators.

            :param info_provider: Injected toolchain metadata and instruction provider.
            :param status_presenter: Injected presenter for status, help and pose formatting.
            :exceptions: None.
        '''
        self._info_provider: Final[IScaraInfoProvider] = info_provider
        self._status_presenter: Final[IReplStatusPresenter] = status_presenter

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
        tokens: list[str] = [token.lower() for token in line.strip().split()]
        result: ReplDispatchResult

        match tokens:
            case []:
                result = ReplDispatchResult(
                    is_exit=False,
                    is_handled=True,
                    message='',
                )
            case ['exit' | 'quit' | ':q', *_]:
                result = ReplDispatchResult(
                    is_exit=True,
                    is_handled=True,
                    message='Session terminated.',
                )
            case ['help' | '?', *_]:
                result = ReplDispatchResult(
                    is_exit=False,
                    is_handled=True,
                    message=self._status_presenter.present_help(),
                )
            case ['clear' | 'cls', *_]:
                result = ReplDispatchResult(
                    is_exit=False,
                    is_handled=True,
                    message='\033[H\033[2J',
                )
            case ['info' | 'specs' | 'catalog', *args]:
                is_verbose: bool = any(
                    flag in ('-v', '--verbose', 'verbose') for flag in args
                )
                info_lines: tuple[str, ...] = self._info_provider.get_info(
                    verbose=is_verbose
                )
                result = ReplDispatchResult(
                    is_exit=False,
                    is_handled=True,
                    message='\n'.join(info_lines),
                )
            case ['status' | 'state', *_]:
                result = ReplDispatchResult(
                    is_exit=False,
                    is_handled=True,
                    message=self._status_presenter.present_status(context=context),
                )
            case ['pose' | 'pos', *_]:
                result = ReplDispatchResult(
                    is_exit=False,
                    is_handled=True,
                    message=self._status_presenter.present_pose(context=context),
                )
            case _:
                result = ReplDispatchResult(
                    is_exit=False,
                    is_handled=False,
                    message='',
                )

        return result

    def get_version(self) -> str:
        '''
            Returns dispatcher version string.

            :return: Dispatcher version string.
            :exceptions: None.
        '''
        return __version__
