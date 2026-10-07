# -*- coding: UTF-8 -*-

'''
Module
    idead_zone_bypass_planner_test.py
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

from scaralang.core.service.trajectory.avoidance.dead_zone_bypass_planner import DeadZoneBypassPlanner
from scaralang.core.service.trajectory.avoidance.dead_zone_bypass_planner_factory import DeadZoneBypassPlannerFactory
from scaralang.core.service.trajectory.avoidance.dead_zone_validator import DeadZoneValidator
from scaralang.core.service.trajectory.avoidance.idead_zone_bypass_planner import IDeadZoneBypassPlanner

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.7'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestIDeadZoneBypassPlanner(TestCase):
    '''
        Test cases for IDeadZoneBypassPlanner structural protocol conformance.

        It defines:

            :methods:
                | test_structural_conformance - Verifies DeadZoneBypassPlanner satisfies protocol.
                | test_factory_return_conformance - Verifies factory returns protocol instance.
    '''

    def test_structural_conformance(self) -> None:
        '''Verifies concrete DeadZoneBypassPlanner satisfies IDeadZoneBypassPlanner protocol.'''
        validator = DeadZoneValidator(dead_zone_radius=86.0)
        planner = DeadZoneBypassPlanner(validator=validator)
        self.assertIsInstance(planner, IDeadZoneBypassPlanner)

    def test_factory_return_conformance(self) -> None:
        '''Verifies factory returns instance satisfying IDeadZoneBypassPlanner.'''
        validator = DeadZoneValidator(dead_zone_radius=86.0)
        planner = DeadZoneBypassPlannerFactory.create(validator=validator)
        self.assertIsInstance(planner, IDeadZoneBypassPlanner)


if __name__ == '__main__':
    main()
