# -*- coding: UTF-8 -*-

'''
Module
    izone_registry.py
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
    Defines structural protocol IZoneRegistry for managing declared obstacle zones.
'''

from __future__ import annotations

from typing import Protocol
from typing import runtime_checkable

from scaralang.core.model.trajectory.obstacle.zone import ObstacleZone

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IZoneRegistry(Protocol):
    '''
        Structural protocol defining storage and lookup of declared obstacle zones.

        It defines:

            :methods:
                | register_zone - Registers an obstacle zone definition.
                | get_zone - Retrieves obstacle zone by unique name.
                | get_all_zones - Returns all registered obstacle zones.
                | has_zone - Checks if obstacle zone exists by name.
                | get_version - Gets implementation version string.
    '''

    def register_zone(self, zone: ObstacleZone) -> None:
        '''
            Registers an obstacle zone definition in the registry.

            :param zone: Obstacle zone instance to register.
        '''

    def get_zone(self, name: str) -> ObstacleZone:
        '''
            Retrieves an obstacle zone definition by its name.

            :param name: Unique obstacle zone identifier string.
            :return: Registered ObstacleZone instance.
        '''

    def get_all_zones(self) -> tuple[ObstacleZone, ...]:
        '''
            Returns all registered obstacle zone definitions.

            :return: Tuple of registered ObstacleZone instances.
        '''

    def has_zone(self, name: str) -> bool:
        '''
            Checks if an obstacle zone definition exists.

            :param name: Unique obstacle zone identifier string.
            :return: True if zone exists, False otherwise.
        '''

    def get_version(self) -> str:
        '''
            Gets implementation version string.

            :return: Version string.
        '''
