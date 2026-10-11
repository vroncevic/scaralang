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
    Factory providing default full-stack composition of dead zone validation subsystem.
'''

from __future__ import annotations

from math import cos, sqrt

from scaralang.core.service.trajectory.avoidance.validation.factory import ValidationFactory
from scaralang.core.service.trajectory.avoidance.validation.provides import ValidationProvides
from scaralang.infrastructure.trajectory.avoidance.validation.dependencies import DefaultValidationDependencies

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.8'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DefaultValidationFactory:
    '''
        Factory providing default composed ValidationProvides instance.

        It defines:

            :methods:
                | create - Builds and wires default ValidationProvides instance from bounds.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(
        cls,
        dependencies: DefaultValidationDependencies,
    ) -> ValidationProvides:
        '''
            Builds and wires default ValidationProvides instance.

            :param dependencies: Inbound DefaultValidationDependencies parameter bundle.
            :return: Fully configured ValidationProvides instance.
            :exceptions: None.
        '''
        bounds = dependencies.bounds
        l1: float = bounds.links.l1
        l2: float = bounds.links.l2
        j2_max: float = bounds.joints.j2_max_rad
        kinematic_r_sq: float = l1 * l1 + l2 * l2 + 2.0 * l1 * l2 * cos(j2_max)
        kinematic_r_min: float = sqrt(max(0.0, kinematic_r_sq))
        theoretical_r_min: float = abs(l1 - l2)
        effective_r_min: float = max(
            kinematic_r_min,
            theoretical_r_min,
            bounds.singularity.deadzone_r_min,
        )
        return ValidationFactory.create(dead_zone_radius=effective_r_min)

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory version string representation.

            :return: Version string representation.
            :exceptions: None.
        '''
        return __version__
