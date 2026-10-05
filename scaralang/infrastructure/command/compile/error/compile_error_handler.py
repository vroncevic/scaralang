# -*- coding: UTF-8 -*-

'''
Module
    compile_error_handler.py
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
    Defines CompileErrorHandler providing structured error reporting and exit codes.
'''

from __future__ import annotations

from scaralang.core.model.exceptions.scara_error import ScaraError
from scaralang.core.model.exceptions.scara_export_error import ScaraExportError
from scaralang.core.model.exceptions.scara_kinematics_error import ScaraKinematicsError
from scaralang.core.model.exceptions.scara_protocol_error import ScaraProtocolError
from scaralang.core.model.exceptions.scara_semantic_error import ScaraSemanticError
from scaralang.core.model.exceptions.scara_syntax_error import ScaraSyntaxError

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.5'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class CompileErrorHandler:
    '''
        Handles diagnostic formatting and exit code resolution for compilation errors.

        It defines:

            :methods:
                | format_error - Formats structured diagnostic message from an error.
                | format_file_missing - Formats missing script error message.
                | resolve_return_code - Resolves CLI return code for an error.
                | get_version - Returns the error handler version string.
    '''

    def format_error(self, *, error: Exception) -> str:
        '''
            Formats structured diagnostic message from a caught exception.

            :param error: The caught exception.
            :return: Formatted error diagnostic string.
            :exceptions: None.
        '''
        tag: str = ''
        if isinstance(error, ScaraSyntaxError):
            tag = '[SYNTAX] '
        elif isinstance(error, ScaraSemanticError):
            tag = '[SEMANTIC] '
        elif isinstance(error, ScaraKinematicsError):
            tag = '[KINEMATICS] '
        elif isinstance(error, ScaraProtocolError):
            tag = '[PROTOCOL] '
        elif isinstance(error, ScaraExportError):
            tag = '[EXPORT] '
        elif isinstance(error, ScaraError):
            tag = '[DOMAIN] '
        elif isinstance(error, OSError):
            tag = '[IO] '
        return f'compile error: {tag}{error}'

    def format_file_missing(self, *, path: str) -> str:
        '''
            Formats missing script file error message.

            :param path: The missing script file path.
            :return: Formatted missing file error string.
            :exceptions: None.
        '''
        return f'compile_command_executor: script file does not exist: {path}'

    def resolve_return_code(self, *, error: Exception) -> int:
        '''
            Resolves CLI process exit code for an exception.

            :param error: The caught exception.
            :return: Integer exit code.
            :exceptions: None.
        '''
        _ = error
        return 1

    def get_version(self) -> str:
        '''
            Returns the error handler version string.

            :return: Version string representation.
            :exceptions: None.
        '''
        return __version__
