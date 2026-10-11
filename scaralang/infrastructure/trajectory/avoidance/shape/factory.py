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
    Factory providing default full-stack composition of shape avoidance subsystem.
'''

from __future__ import annotations

from scaralang.core.service.trajectory.avoidance.bypass.planner.iplanner import IDeadZoneBypassPlanner
from scaralang.core.service.trajectory.avoidance.shape.dependencies import ShapeDependencies
from scaralang.core.service.trajectory.avoidance.shape.factory import ShapeFactory
from scaralang.core.service.trajectory.avoidance.shape.provides import ShapeProvides
from scaralang.core.service.trajectory.avoidance.validation.ivalidator import IDeadZoneValidator
from scaralang.infrastructure.trajectory.avoidance.bypass.dependencies import DefaultBypassDependencies
from scaralang.infrastructure.trajectory.avoidance.bypass.factory import DefaultBypassFactory
from scaralang.infrastructure.trajectory.avoidance.shape.dependencies import DefaultShapeDependencies
from scaralang.infrastructure.trajectory.avoidance.validation.dependencies import DefaultValidationDependencies
from scaralang.infrastructure.trajectory.avoidance.validation.factory import DefaultValidationFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.8'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DefaultShapeFactory:
    '''
        Factory providing default composed ShapeProvides instance.

        It defines:

            :methods:
                | create - Builds and wires default ShapeProvides instance from bounds.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(
        cls,
        dependencies: DefaultShapeDependencies,
    ) -> ShapeProvides:
        '''
            Builds and wires default ShapeProvides instance.

            :param dependencies: Inbound DefaultShapeDependencies parameter bundle.
            :return: Fully configured ShapeProvides instance.
            :exceptions: None.
        '''
        validation_bundle = DefaultValidationDependencies(bounds=dependencies.bounds)
        validator: IDeadZoneValidator = (
            DefaultValidationFactory.create(dependencies=validation_bundle).validator
        )
        bypass_bundle = DefaultBypassDependencies(
            validator=validator,
            safety_margin_mm=dependencies.safety_margin_mm,
            angular_step_rad=dependencies.angular_step_rad,
        )
        bypass_planner: IDeadZoneBypassPlanner = (
            DefaultBypassFactory.create(dependencies=bypass_bundle).planner
        )
        shape_deps = ShapeDependencies(
            validator=validator,
            bypass_planner=bypass_planner,
        )
        return ShapeFactory.create(dependencies=shape_deps)

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory version string representation.

            :return: Version string representation.
            :exceptions: None.
        '''
        return __version__
