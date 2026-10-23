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
    Factory providing default full-stack composition of dead zone bypass subsystem.
'''

from __future__ import annotations

from scaralang.core.service.trajectory.avoidance.bypass.arc.factory import ArcFactory
from scaralang.core.service.trajectory.avoidance.bypass.dependencies import BypassDependencies
from scaralang.core.service.trajectory.avoidance.bypass.factory import BypassFactory
from scaralang.core.service.trajectory.avoidance.bypass.provides import BypassProvides
from scaralang.infrastructure.trajectory.avoidance.bypass.dependencies import DefaultBypassDependencies

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DefaultBypassFactory:
    '''
        Factory providing default composed BypassProvides instance.

        It defines:

            :methods:
                | create - Builds and wires default BypassProvides instance.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(
        cls,
        dependencies: DefaultBypassDependencies,
    ) -> BypassProvides:
        '''
            Builds and wires default BypassProvides instance.

            :param dependencies: Inbound DefaultBypassDependencies parameter bundle.
            :return: Fully configured BypassProvides instance.
            :exceptions: None.
        '''
        calculator = ArcFactory.create().calculator
        bypass_dependencies = BypassDependencies(
            validator=dependencies.validator,
            calculator=calculator,
            safety_margin_mm=dependencies.safety_margin_mm,
            angular_step_rad=dependencies.angular_step_rad,
        )
        return BypassFactory.create(dependencies=bypass_dependencies)

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory version string.

            :return: Factory version string.
            :exceptions: None.
        '''
        return __version__
