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
    Factory instantiating and wiring trajectory validation root subsystem.
'''

from __future__ import annotations

from scaralang.core.service.trajectory.validation.dependencies import ValidationDependencies
from scaralang.core.service.trajectory.validation.feedrate.factory import FeedrateFactory
from scaralang.core.service.trajectory.validation.feedrate.provides import FeedrateProvides
from scaralang.core.service.trajectory.validation.plan.dependencies import PlanDependencies
from scaralang.core.service.trajectory.validation.plan.factory import PlanFactory
from scaralang.core.service.trajectory.validation.plan.provides import PlanProvides
from scaralang.core.service.trajectory.validation.provides import ValidationProvides
from scaralang.core.service.trajectory.validation.validator import TrajectoryValidator
from scaralang.core.service.trajectory.validation.waypoint.factory import WaypointFactory
from scaralang.core.service.trajectory.validation.waypoint.provides import WaypointProvides

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.8'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ValidationFactory:
    '''
        Subsystem factory assembling and coordinating trajectory validators.

        It defines:

            :methods:
                | create - Builds and wires trajectory validation subsystem.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(
        cls,
        *,
        dependencies: ValidationDependencies,
    ) -> ValidationProvides:
        '''
            Builds and wires trajectory validation subsystem with injected dependencies.

            :param dependencies: Injected ValidationDependencies bundle.
            :return: ValidationProvides bundle containing validation services.
            :exceptions: None.
        '''
        waypoint_provides: WaypointProvides = WaypointFactory.create(
            kinematics=dependencies.kinematics
        )
        feedrate_provides: FeedrateProvides = FeedrateFactory.create(
            bounds=dependencies.kinematics.bounds
        )
        plan_provides: PlanProvides = PlanFactory.create(
            dependencies=PlanDependencies(
                waypoint_validator=waypoint_provides.validator,
                feedrate_validator=feedrate_provides.validator,
            )
        )

        validator = TrajectoryValidator(
            kinematics=dependencies.kinematics,
            waypoint_validator=waypoint_provides.validator,
            feedrate_validator=feedrate_provides.validator,
            plan_validator=plan_provides.validator,
        )

        return ValidationProvides(validator=validator)

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory version string.

            :return: Factory version string.
            :exceptions: None.
        '''
        return __version__
