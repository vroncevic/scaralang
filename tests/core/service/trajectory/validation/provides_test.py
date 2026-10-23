# -*- coding: UTF-8 -*-

'''
Module
    provides_test.py
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
    Unit tests for ValidationProvides dataclass.
'''

from __future__ import annotations

from dataclasses import FrozenInstanceError
from unittest import TestCase, main

from scaralang.core.service.trajectory.validation.feedrate.factory import FeedrateFactory
from scaralang.core.service.trajectory.validation.plan.dependencies import PlanDependencies
from scaralang.core.service.trajectory.validation.plan.factory import PlanFactory
from scaralang.core.service.trajectory.validation.provides import ValidationProvides
from scaralang.core.service.trajectory.validation.waypoint.factory import WaypointFactory
from scaralang.infrastructure.kinematics.factory import DefaultKinematicsFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestValidationProvides(TestCase):
    '''
        Test cases for ValidationProvides output bundle.

        It defines:

            :methods:
                | test_bundle_initialization - Verifies attributes initialized correctly.
                | test_bundle_immutability - Verifies FrozenInstanceError on modification.
    '''

    def test_bundle_initialization(self) -> None:
        '''Verifies bundle holds provided role validator instances.'''
        kinematics = DefaultKinematicsFactory.create()
        wp_val = WaypointFactory.create(workspace=kinematics.workspace).validator
        fr_val = FeedrateFactory.create(bounds=kinematics.envelope.bounds).validator
        plan_deps = PlanDependencies(
            waypoint_validator=wp_val,
            feedrate_validator=fr_val,
        )
        plan_val = PlanFactory.create(dependencies=plan_deps).validator
        bundle = ValidationProvides(
            waypoint=wp_val,
            feedrate=fr_val,
            plan=plan_val,
        )
        self.assertIs(bundle.waypoint, wp_val)
        self.assertIs(bundle.feedrate, fr_val)
        self.assertIs(bundle.plan, plan_val)

    def test_bundle_immutability(self) -> None:
        '''Verifies frozen dataclass rejects attribute mutations.'''
        kinematics = DefaultKinematicsFactory.create()
        wp_val = WaypointFactory.create(workspace=kinematics.workspace).validator
        fr_val = FeedrateFactory.create(bounds=kinematics.envelope.bounds).validator
        plan_deps = PlanDependencies(
            waypoint_validator=wp_val,
            feedrate_validator=fr_val,
        )
        plan_val = PlanFactory.create(dependencies=plan_deps).validator
        bundle = ValidationProvides(
            waypoint=wp_val,
            feedrate=fr_val,
            plan=plan_val,
        )
        with self.assertRaises(FrozenInstanceError):
            bundle.waypoint = wp_val  # type: ignore[misc]


if __name__ == '__main__':
    main()
