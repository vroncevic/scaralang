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
    Factory instantiating obstacle lint rule subsystem components.
'''

from __future__ import annotations

from scaralang.core.service.linter.rules.obstacle.builder.builder import ZoneBuilder
from scaralang.core.service.linter.rules.obstacle.dependencies import ObstacleDependencies
from scaralang.core.service.linter.rules.obstacle.provides import ObstacleProvides
from scaralang.core.service.linter.rules.obstacle.rule import ObstacleLintRule

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ObstacleFactory:
    '''
        Factory providing configured ObstacleProvides subsystem instances.

        It defines:

            :methods:
                | create - Constructs and wires ObstacleProvides container.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(cls, dependencies: ObstacleDependencies) -> ObstacleProvides:
        '''
            Constructs and wires ObstacleProvides container with cooperating builders.

            :param dependencies: Injected obstacle rule dependencies.
            :return: Fully configured ObstacleProvides container.
            :exceptions: None.
        '''
        zone_builder = ZoneBuilder()
        rule = ObstacleLintRule(
            zone_builder=zone_builder,
            zone_registry=dependencies.zone_registry,
            spatial_checker=dependencies.spatial_checker,
        )

        return ObstacleProvides(rule=rule)

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory version string.

            :return: Factory version string.
            :exceptions: None.
        '''
        return __version__
