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
    Factory instantiating dead zone bypass subsystem components.
'''

from __future__ import annotations

from scaralang.core.service.trajectory.avoidance.bypass.dependencies import BypassDependencies
from scaralang.core.service.trajectory.avoidance.bypass.planner.dependencies import PlannerDependencies
from scaralang.core.service.trajectory.avoidance.bypass.planner.factory import PlannerFactory
from scaralang.core.service.trajectory.avoidance.bypass.provides import BypassProvides

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.9'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class BypassFactory:
    '''
        Factory providing configured bypass subsystem components.

        It defines:

            :methods:
                | create - Builds BypassProvides bundle from dependencies.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(cls, dependencies: BypassDependencies) -> BypassProvides:
        '''
            Builds and returns a BypassProvides container from dependencies.

            :param dependencies: Required BypassDependencies bundle.
            :return: Configured BypassProvides instance.
            :exceptions: None.
        '''
        planner_provides = PlannerFactory.create(
            dependencies=PlannerDependencies(
                validator=dependencies.validator,
                calculator=dependencies.calculator,
                safety_margin_mm=dependencies.safety_margin_mm,
                angular_step_rad=dependencies.angular_step_rad,
            )
        )

        return BypassProvides(
            planner=planner_provides.planner,
            calculator=dependencies.calculator,
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns factory version string representation.

            :return: Version string representation.
            :exceptions: None.
        '''
        return __version__
