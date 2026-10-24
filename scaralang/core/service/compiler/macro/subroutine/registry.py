# -*- coding: UTF-8 -*-

'''
Module
    registry.py
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
    Implementation of subroutine definition registry.
'''

from __future__ import annotations

from typing import Final

from scaralang.core.model.dsl.macro.subroutine import SubroutineDefinition
from scaralang.core.model.exceptions.semantic import ScaraSemanticError

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class SubroutineRegistry:
    '''
        In-memory registry storing and retrieving declared SubroutineDefinition entities.

        It defines:

            :attributes:
                | _subroutines - Dictionary mapping normalized subroutine name to SubroutineDefinition.
            :methods:
                | __init__ - Initializes registry with empty storage.
                | register - Registers a subroutine definition.
                | lookup - Retrieves a registered subroutine definition.
                | has - Checks if a subroutine is registered.
                | get_version - Returns registry component version string.
    '''

    _subroutines: dict[str, SubroutineDefinition]

    def __init__(self) -> None:
        '''
            Initializes SubroutineRegistry constructor.

            :exceptions: None.
        '''
        self._subroutines: Final[dict[str, SubroutineDefinition]] = {}

    def register(self, *, definition: SubroutineDefinition) -> None:
        '''
            Registers a subroutine definition into storage.

            :param definition: SubroutineDefinition domain entity.
            :exceptions:
                | ScaraSemanticError: If subroutine is already defined.
        '''
        normalized_name: str = definition.name.upper()

        if normalized_name in self._subroutines:
            raise ScaraSemanticError(
                f'Duplicate subroutine definition {definition.name!r} at line {definition.line_number}'
            )

        self._subroutines[normalized_name] = definition

    def lookup(self, *, name: str) -> SubroutineDefinition:
        '''
            Retrieves a registered subroutine definition.

            :param name: Subroutine identifier name.
            :return: Stored SubroutineDefinition.
            :exceptions:
                | ScaraSemanticError: If subroutine name is not defined.
        '''
        normalized_name: str = name.upper()

        if normalized_name not in self._subroutines:
            raise ScaraSemanticError(f'Undefined subroutine {name!r}')

        return self._subroutines[normalized_name]

    def has(self, *, name: str) -> bool:
        '''
            Checks whether a subroutine identifier is registered.

            :param name: Subroutine identifier name.
            :return: True if registered, False otherwise.
            :exceptions: None.
        '''
        return name.upper() in self._subroutines

    def get_version(self) -> str:
        '''
            Returns component version string representation.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return __version__
