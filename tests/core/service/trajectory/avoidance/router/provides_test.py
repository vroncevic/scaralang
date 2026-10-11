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
    Unit tests for RouterProvides dataclass.
'''

from __future__ import annotations

from dataclasses import FrozenInstanceError
from unittest import TestCase, main

from scaralang.core.service.trajectory.avoidance.bypass.arc.factory import ArcFactory
from scaralang.core.service.trajectory.avoidance.bypass.dependencies import BypassDependencies
from scaralang.core.service.trajectory.avoidance.bypass.factory import BypassFactory
from scaralang.core.service.trajectory.avoidance.router.dependencies import RouterDependencies
from scaralang.core.service.trajectory.avoidance.router.provides import RouterProvides
from scaralang.core.service.trajectory.avoidance.router.router import SafeTrajectoryRouter
from scaralang.core.service.trajectory.avoidance.validation.factory import ValidationFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.8'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestRouterProvides(TestCase):
    '''
        Test cases for RouterProvides container dataclass.

        It defines:

            :methods:
                | test_provides_attributes - Verifies router instance exposed properly.
                | test_provides_immutability - Verifies frozen immutability of bundle.
    '''

    def _create_router(self) -> SafeTrajectoryRouter:
        '''Helper to instantiate a dummy SafeTrajectoryRouter.'''
        validator = ValidationFactory.create(dead_zone_radius=86.0).validator
        calculator = ArcFactory.create().calculator
        deps = BypassDependencies(
            validator=validator,
            calculator=calculator,
            safety_margin_mm=5.0,
        )
        bypass_planner = BypassFactory.create(dependencies=deps).planner
        router_deps = RouterDependencies(
            validator=validator,
            bypass_planner=bypass_planner,
        )
        return SafeTrajectoryRouter(dependencies=router_deps)

    def test_provides_attributes(self) -> None:
        '''Verifies router attribute is properly exposed.'''
        router = self._create_router()
        provides = RouterProvides(router=router)
        self.assertIs(provides.router, router)

    def test_provides_immutability(self) -> None:
        '''Verifies frozen dataclass immutability.'''
        router = self._create_router()
        provides = RouterProvides(router=router)
        with self.assertRaises(FrozenInstanceError):
            provides.router = None  # type: ignore[misc]


if __name__ == '__main__':
    main()
