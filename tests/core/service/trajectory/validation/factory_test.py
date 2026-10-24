# -*- coding: UTF-8 -*-

'''
Module
    factory_test.py
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
    Unit tests for ValidationFactory component.
'''

from __future__ import annotations

from unittest import TestCase, main

from scaralang.core.service.trajectory.validation.dependencies import ValidationDependencies
from scaralang.core.service.trajectory.validation.factory import ValidationFactory
from scaralang.core.service.trajectory.validation.feedrate.ivalidator import IFeedrateValidator
from scaralang.core.service.trajectory.validation.plan.ivalidator import ITrajectoryPlanValidator
from scaralang.core.service.trajectory.validation.provides import ValidationProvides
from scaralang.core.service.trajectory.validation.waypoint.ivalidator import IWaypointValidator
from scaralang.infrastructure.kinematics.factory import DefaultKinematicsFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestValidationFactory(TestCase):
    '''
        Test cases for ValidationFactory component creation.

        It defines:

            :methods:
                | test_create - Verifies factory returns ValidationProvides bundle.
                | test_get_version - Verifies factory version string format.
    '''

    def test_create(self) -> None:
        '''Verifies factory instantiates and wires ValidationProvides bundle.'''
        provides = DefaultKinematicsFactory.create()
        deps = ValidationDependencies(
            workspace=provides.workspace,
            envelope=provides.envelope,
        )
        bundle = ValidationFactory.create(dependencies=deps)
        self.assertIsInstance(bundle, ValidationProvides)
        self.assertIsInstance(bundle.waypoint, IWaypointValidator)
        self.assertIsInstance(bundle.feedrate, IFeedrateValidator)
        self.assertIsInstance(bundle.plan, ITrajectoryPlanValidator)

    def test_get_version(self) -> None:
        '''Verifies factory returns valid semantic version string.'''
        version_str = ValidationFactory.get_version()
        self.assertIsInstance(version_str, str)
        self.assertTrue(len(version_str) > 0)


if __name__ == '__main__':
    main()
