# -*- coding: UTF-8 -*-

'''
Module
    itemplates.py
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
    Defines ICommandTemplates structural protocol for ASCII command template catalogs.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.9'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class ICommandTemplates(Protocol):
    '''
        Structural protocol defining command template retrieval operations.

        It defines:

            :methods:
                | get_template - Retrieves command template string by action key.
                | list_actions - Returns tuple of supported command action keys.
                | get_version - Returns template catalog version string.
    '''

    def get_template(self, action: str) -> str:
        '''
            Retrieves command template by action identifier.

            :param action: Action name string.
            :return: Template string or empty string if not found.
            :exceptions: None.
        '''

    def list_actions(self) -> tuple[str, ...]:
        '''
            Returns tuple of supported command action keys.

            :return: Tuple of action key strings.
            :exceptions: None.
        '''

    def get_version(self) -> str:
        '''
            Returns the template catalog version string.

            :return: Semantic version string.
            :exceptions: None.
        '''
