# -*- coding: UTF-8 -*-

'''
Module
    factory.py
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
    Factory instantiating and wiring spatial collision avoidance subsystem.
'''

from __future__ import annotations

from scaralang.core.service.trajectory.avoidance.collision.box_checker import BoxCollisionChecker
from scaralang.core.service.trajectory.avoidance.collision.circle_checker import CircleCollisionChecker
from scaralang.core.service.trajectory.avoidance.collision.provides import CollisionProvides
from scaralang.core.service.trajectory.avoidance.collision.spatial_checker import SpatialCollisionChecker
from scaralang.core.service.trajectory.avoidance.collision.zone_registry import ZoneRegistry

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class CollisionFactory:
    '''
        Factory constructing and wiring CollisionProvides subsystem instances.

        It defines:

            :methods:
                | create - Constructs and wires CollisionProvides container.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(cls) -> CollisionProvides:
        '''
            Constructs and wires CollisionProvides container with checkers and registry.

            :return: Fully configured CollisionProvides container.
            :exceptions: None.
        '''
        box_checker = BoxCollisionChecker()
        circle_checker = CircleCollisionChecker()
        spatial_checker = SpatialCollisionChecker(
            box_checker=box_checker,
            circle_checker=circle_checker,
        )
        registry = ZoneRegistry()

        return CollisionProvides(
            registry=registry,
            spatial_checker=spatial_checker,
            box_checker=box_checker,
            circle_checker=circle_checker,
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory version string.

            :return: Factory version string.
            :exceptions: None.
        '''
        return __version__
