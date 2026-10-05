# -*- coding: UTF-8 -*-

'''
Module
    idecompile_error_handler.py
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
    Defines structural interface protocol for decompile command error handlers.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IDecompileErrorHandler(Protocol):
    '''
        Structural interface protocol for decompile command error handlers.

        It defines:

            :methods:
                | format_error - Formats structured diagnostic message from an error.
                | format_file_missing - Formats missing binary file error message.
                | resolve_return_code - Resolves CLI return code for an error.
                | get_version - Returns the error handler version string.
    '''

    def format_error(self, *, error: Exception) -> str:
        '''
            Formats structured diagnostic message from a caught exception.

            :param error: The caught exception.
            :return: Formatted error diagnostic string.
        '''

    def format_file_missing(self, *, path: str) -> str:
        '''
            Formats missing binary file error message.

            :param path: The missing binary file path.
            :return: Formatted missing file error string.
        '''

    def resolve_return_code(self, *, error: Exception) -> int:
        '''
            Resolves CLI process exit code for an exception.

            :param error: The caught exception.
            :return: Integer exit code.
        '''

    def get_version(self) -> str:
        '''
            Returns the error handler version string.

            :return: Version string representation.
        '''
