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
    Factory providing default full-stack composition of safe trajectory router subsystem.
'''

from __future__ import annotations

from scaralang.core.service.trajectory.avoidance.bypass.planner.iplanner import IDeadZoneBypassPlanner
from scaralang.core.service.trajectory.avoidance.router.dependencies import RouterDependencies
from scaralang.core.service.trajectory.avoidance.router.factory import RouterFactory
from scaralang.core.service.trajectory.avoidance.router.provides import RouterProvides
from scaralang.core.service.trajectory.avoidance.validation.ivalidator import IDeadZoneValidator
from scaralang.infrastructure.trajectory.avoidance.bypass.dependencies import DefaultBypassDependencies
from scaralang.infrastructure.trajectory.avoidance.bypass.factory import DefaultBypassFactory
from scaralang.infrastructure.trajectory.avoidance.router.dependencies import DefaultRouterDependencies
from scaralang.infrastructure.trajectory.avoidance.validation.dependencies import DefaultValidationDependencies
from scaralang.infrastructure.trajectory.avoidance.validation.factory import DefaultValidationFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DefaultRouterFactory:
    '''
        Factory providing default composed RouterProvides instance.

        It defines:

            :methods:
                | create - Builds and wires default RouterProvides instance from bounds.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(
        cls,
        dependencies: DefaultRouterDependencies,
    ) -> RouterProvides:
        '''
            Builds and wires default RouterProvides instance.

            :param dependencies: Inbound DefaultRouterDependencies parameter bundle.
            :return: Fully configured RouterProvides instance.
            :exceptions: None.
        '''
        valid_deps = DefaultValidationDependencies(bounds=dependencies.bounds)
        zone_validator: IDeadZoneValidator = (
            DefaultValidationFactory.create(dependencies=valid_deps).validator
        )
        byp_deps = DefaultBypassDependencies(
            validator=zone_validator,
            safety_margin_mm=dependencies.safety_margin_mm,
            angular_step_rad=dependencies.angular_step_rad,
        )
        path_bypass: IDeadZoneBypassPlanner = (
            DefaultBypassFactory.create(dependencies=byp_deps).planner
        )
        router_dependencies = RouterDependencies(
            validator=zone_validator,
            bypass_planner=path_bypass,
        )
        return RouterFactory.create(dependencies=router_dependencies)

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns factory version string representation.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return __version__
