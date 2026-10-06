# -*- coding: UTF-8 -*-

'''
Module
    export_error_handler_factory.py
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
    Defines ExportErrorHandlerFactory for instantiating ExportErrorHandler.
'''

from __future__ import annotations

from scaralang.infrastructure.command.export.error.export_error_handler import ExportErrorHandler

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.6'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ExportErrorHandlerFactory:
    '''
        Factory instantiating ExportErrorHandler instances.

        It defines:

            :methods:
                | create - Instantiates a new ExportErrorHandler instance.
                | create_default - Instantiates default ExportErrorHandler.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(cls) -> ExportErrorHandler:
        '''
            Creates a new ExportErrorHandler instance.

            :return: Configured ExportErrorHandler instance.
            :exceptions: None.
        '''
        return ExportErrorHandler()

    @classmethod
    def create_default(cls) -> ExportErrorHandler:
        '''
            Creates a default ExportErrorHandler instance.

            :return: Default ExportErrorHandler instance.
            :exceptions: None.
        '''
        return cls.create()

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns factory version string.

            :return: Factory version string.
            :exceptions: None.
        '''
        return __version__
