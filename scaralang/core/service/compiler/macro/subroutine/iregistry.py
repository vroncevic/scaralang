# -*- coding: UTF-8 -*-

'''
Module
    iregistry.py
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
    Structural protocol defining subroutine definition registry contract.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from scaralang.core.model.dsl.macro.subroutine import SubroutineDefinition

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class ISubroutineRegistry(Protocol):
    '''
        Structural protocol defining storage and lookup contract for macro subroutines.

        It defines:

            :methods:
                | register - Registers a parsed SubroutineDefinition by name.
                | lookup - Retrieves a SubroutineDefinition by name.
                | has - Checks if a subroutine name is registered.
                | get_version - Returns registry component version string.
    '''

    def register(self, *, definition: SubroutineDefinition) -> None:
        '''
            Registers a new subroutine definition.

            :param definition: SubroutineDefinition domain entity.
        '''

    def lookup(self, *, name: str) -> SubroutineDefinition:
        '''
            Retrieves a registered subroutine definition.

            :param name: Subroutine identifier name.
            :return: Stored SubroutineDefinition.
        '''

    def has(self, *, name: str) -> bool:
        '''
            Checks whether a subroutine identifier is registered.

            :param name: Subroutine identifier name.
            :return: True if registered, False otherwise.
        '''

    def get_version(self) -> str:
        '''
            Returns component version string representation.

            :return: Semantic version string.
        '''
