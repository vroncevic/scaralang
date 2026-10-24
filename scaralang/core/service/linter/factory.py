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
    Factory instantiating and wiring root linter subsystem.
'''

from __future__ import annotations

from scaralang.core.service.linter.linter import Linter
from scaralang.core.service.linter.provides import LinterProvides
from scaralang.core.service.linter.rules.motion.factory import MotionFactory
from scaralang.core.service.linter.rules.obstacle.dependencies import ObstacleDependencies
from scaralang.core.service.linter.rules.obstacle.factory import ObstacleFactory
from scaralang.core.service.linter.rules.pneumatic.factory import PneumaticFactory
from scaralang.core.service.linter.rules.state.factory import StateFactory
from scaralang.core.service.linter.rules.timing.factory import TimingFactory
from scaralang.core.service.trajectory.avoidance.collision.factory import CollisionFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class LinterFactory:
    '''
        Factory providing configured ILinter subsystem instances.

        It defines:

            :methods:
                | create - Constructs and wires LinterProvides container.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(cls) -> LinterProvides:
        '''
            Constructs and wires LinterProvides container with cooperating rule validators.

            :return: Fully configured LinterProvides container.
            :exceptions: None.
        '''
        collision = CollisionFactory.create()
        obstacle_rule = ObstacleFactory.create(
            dependencies=ObstacleDependencies(
                zone_registry=collision.registry,
                spatial_checker=collision.spatial_checker,
            )
        ).rule

        rules = (
            StateFactory.create().rule,
            MotionFactory.create().rule,
            PneumaticFactory.create().rule,
            TimingFactory.create().rule,
            obstacle_rule,
        )
        linter = Linter(rules=rules)

        return LinterProvides(linter=linter)

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory version string.

            :return: Factory version string.
            :exceptions: None.
        '''
        return __version__
