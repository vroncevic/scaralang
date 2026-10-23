# -*- coding: UTF-8 -*-

'''
Module
    irouter_test.py
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
    Unit tests for ISafeTrajectoryRouter structural protocol.
'''

from __future__ import annotations

from unittest import TestCase, main

from scaralang.core.service.trajectory.avoidance.bypass.arc.factory import ArcFactory
from scaralang.core.service.trajectory.avoidance.bypass.dependencies import BypassDependencies
from scaralang.core.service.trajectory.avoidance.bypass.factory import BypassFactory
from scaralang.core.service.trajectory.avoidance.router.dependencies import RouterDependencies
from scaralang.core.service.trajectory.avoidance.router.factory import RouterFactory
from scaralang.core.service.trajectory.avoidance.router.irouter import ISafeTrajectoryRouter
from scaralang.core.service.trajectory.avoidance.router.router import SafeTrajectoryRouter
from scaralang.core.service.trajectory.avoidance.validation.factory import ValidationFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestISafeTrajectoryRouter(TestCase):
    '''
        Test cases for ISafeTrajectoryRouter structural protocol conformance.

        It defines:

            :methods:
                | test_structural_conformance - Verifies SafeTrajectoryRouter satisfies protocol.
                | test_factory_return_conformance - Verifies factory returns protocol instance.
    '''

    def test_structural_conformance(self) -> None:
        '''Verifies concrete SafeTrajectoryRouter satisfies ISafeTrajectoryRouter protocol.'''
        validator = ValidationFactory.create(dead_zone_radius=86.0).validator
        calculator = ArcFactory.create().calculator
        deps = BypassDependencies(validator=validator, calculator=calculator)
        bypass_planner = BypassFactory.create(dependencies=deps).planner
        router_deps = RouterDependencies(
            validator=validator,
            bypass_planner=bypass_planner,
        )
        router = SafeTrajectoryRouter(dependencies=router_deps)
        self.assertIsInstance(router, ISafeTrajectoryRouter)

    def test_factory_return_conformance(self) -> None:
        '''Verifies factory returns instance satisfying ISafeTrajectoryRouter.'''
        validator = ValidationFactory.create(dead_zone_radius=86.0).validator
        calculator = ArcFactory.create().calculator
        deps = BypassDependencies(validator=validator, calculator=calculator)
        bypass_planner = BypassFactory.create(dependencies=deps).planner
        router_deps = RouterDependencies(
            validator=validator,
            bypass_planner=bypass_planner,
        )
        provides = RouterFactory.create(dependencies=router_deps)
        self.assertIsInstance(provides.router, ISafeTrajectoryRouter)


if __name__ == '__main__':
    main()
