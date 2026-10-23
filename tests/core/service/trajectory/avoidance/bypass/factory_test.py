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
    Unit tests for BypassFactory component.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.service.trajectory.avoidance.bypass.arc.calculator import TangentArcCalculator
from scaralang.core.service.trajectory.avoidance.bypass.arc.icalculator import ITangentArcCalculator
from scaralang.core.service.trajectory.avoidance.bypass.dependencies import BypassDependencies
from scaralang.core.service.trajectory.avoidance.bypass.factory import BypassFactory
from scaralang.core.service.trajectory.avoidance.bypass.planner.iplanner import IDeadZoneBypassPlanner
from scaralang.core.service.trajectory.avoidance.bypass.provides import BypassProvides
from scaralang.core.service.trajectory.avoidance.validation.validator import DeadZoneValidator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestBypassFactory(TestCase):
    '''
        Validates BypassFactory instantiations.

        It defines:

            :methods:
                | test_create - Verifies factory builds BypassProvides.
                | test_get_version - Verifies component version string.
    '''

    def test_create(self) -> None:
        '''
            Verifies factory builds BypassProvides with planner and calculator.
        '''
        validator = DeadZoneValidator(dead_zone_radius=86.0)
        calculator = TangentArcCalculator()
        deps = BypassDependencies(validator=validator, calculator=calculator)
        provides = BypassFactory.create(dependencies=deps)
        self.assertIsInstance(provides, BypassProvides)
        self.assertIsInstance(provides.planner, IDeadZoneBypassPlanner)
        self.assertIsInstance(provides.calculator, ITangentArcCalculator)

    def test_get_version(self) -> None:
        '''
            Verifies component version string representation.
        '''
        version = BypassFactory.get_version()
        self.assertIsInstance(version, str)
        self.assertTrue(len(version) > 0)


if __name__ == '__main__':
    main()
