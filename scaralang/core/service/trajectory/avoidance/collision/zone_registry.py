# -*- coding: UTF-8 -*-

'''
Module
    zone_registry.py
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
    Implementation of in-memory registry storing declared obstacle zones.
'''

from __future__ import annotations

from scaralang.core.model.exceptions.semantic import ScaraSemanticError
from scaralang.core.model.trajectory.obstacle.zone import ObstacleZone

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ZoneRegistry:
    '''
        Registry managing declared obstacle zones during compilation and linting.

        It defines:

            :attributes:
                | _zones - Dictionary mapping zone name to ObstacleZone instance.
            :methods:
                | __init__ - Initializes empty ZoneRegistry.
                | register_zone - Registers an obstacle zone definition.
                | get_zone - Retrieves obstacle zone by unique name.
                | get_all_zones - Returns all registered obstacle zones.
                | has_zone - Checks if obstacle zone exists by name.
                | get_version - Gets implementation version string.
    '''

    def __init__(self) -> None:
        '''Initializes empty ZoneRegistry instance.'''
        self._zones: dict[str, ObstacleZone] = {}

    def register_zone(self, zone: ObstacleZone) -> None:
        '''
            Registers an obstacle zone definition in the registry.

            :param zone: Obstacle zone instance to register.
            :exceptions:
                | ScaraSemanticError: If zone with same name already registered.
        '''
        if zone.name in self._zones:
            raise ScaraSemanticError(
                f'Duplicate obstacle zone definition: {zone.name}'
            )
        self._zones[zone.name] = zone

    def get_zone(self, name: str) -> ObstacleZone:
        '''
            Retrieves an obstacle zone definition by its name.

            :param name: Unique obstacle zone identifier string.
            :return: Registered ObstacleZone instance.
            :exceptions:
                | ScaraSemanticError: If zone is not found.
        '''
        if name not in self._zones:
            raise ScaraSemanticError(
                f'Obstacle zone not found: {name}'
            )
        return self._zones[name]

    def get_all_zones(self) -> tuple[ObstacleZone, ...]:
        '''
            Returns all registered obstacle zone definitions.

            :return: Tuple of registered ObstacleZone instances.
            :exceptions: None.
        '''
        return tuple(self._zones.values())

    def has_zone(self, name: str) -> bool:
        '''
            Checks if an obstacle zone definition exists.

            :param name: Unique obstacle zone identifier string.
            :return: True if zone exists, False otherwise.
            :exceptions: None.
        '''
        return name in self._zones

    def get_version(self) -> str:
        '''
            Gets implementation version string.

            :return: Version string.
            :exceptions: None.
        '''
        return __version__
