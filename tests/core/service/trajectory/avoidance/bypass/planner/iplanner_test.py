# -*- coding: UTF-8 -*-

'''
Module
    iplanner_test.py
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
    Unit tests for IDeadZoneBypassPlanner protocol.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.service.trajectory.avoidance.bypass.arc.calculator import TangentArcCalculator
from scaralang.core.service.trajectory.avoidance.bypass.planner.dependencies import PlannerDependencies
from scaralang.core.service.trajectory.avoidance.bypass.planner.factory import PlannerFactory
from scaralang.core.service.trajectory.avoidance.bypass.planner.iplanner import IDeadZoneBypassPlanner
from scaralang.core.service.trajectory.avoidance.bypass.planner.planner import DeadZoneBypassPlanner
from scaralang.core.service.trajectory.avoidance.validation.validator import DeadZoneValidator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.9'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestIDeadZoneBypassPlanner(TestCase):
    '''
        Test cases for IDeadZoneBypassPlanner structural protocol conformance.

        It defines:

            :methods:
                | test_structural_conformance - Verifies DeadZoneBypassPlanner satisfies protocol.
                | test_factory_return_conformance - Verifies factory returns instance satisfying protocol.
    '''

    def test_structural_conformance(self) -> None:
        '''
            Verifies concrete DeadZoneBypassPlanner satisfies IDeadZoneBypassPlanner protocol.
        '''
        validator = DeadZoneValidator(dead_zone_radius=86.0)
        calculator = TangentArcCalculator()
        deps = PlannerDependencies(validator=validator, calculator=calculator)
        planner = DeadZoneBypassPlanner(dependencies=deps)
        self.assertIsInstance(planner, IDeadZoneBypassPlanner)

    def test_factory_return_conformance(self) -> None:
        '''
            Verifies factory returns instance satisfying IDeadZoneBypassPlanner protocol.
        '''
        validator = DeadZoneValidator(dead_zone_radius=86.0)
        calculator = TangentArcCalculator()
        deps = PlannerDependencies(validator=validator, calculator=calculator)
        provides = PlannerFactory.create(dependencies=deps)
        self.assertIsInstance(provides.planner, IDeadZoneBypassPlanner)


if __name__ == '__main__':
    main()
