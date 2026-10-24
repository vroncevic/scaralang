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
    Unit tests for DefaultBypassFactory.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.service.trajectory.avoidance.bypass.arc.icalculator import ITangentArcCalculator
from scaralang.core.service.trajectory.avoidance.bypass.planner.iplanner import IDeadZoneBypassPlanner
from scaralang.core.service.trajectory.avoidance.bypass.provides import BypassProvides
from scaralang.core.service.trajectory.avoidance.validation.validator import DeadZoneValidator
from scaralang.infrastructure.trajectory.avoidance.bypass.dependencies import DefaultBypassDependencies
from scaralang.infrastructure.trajectory.avoidance.bypass.factory import DefaultBypassFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestDefaultBypassFactory(TestCase):
    '''
        Test cases verifying DefaultBypassFactory assembly.

        It defines:

            :methods:
                | test_create - Verifies factory returns BypassProvides with protocols.
                | test_get_version - Verifies factory version string.
    '''

    def test_create(self) -> None:
        '''
            Verifies that DefaultBypassFactory returns configured BypassProvides.
        '''
        validator = DeadZoneValidator(dead_zone_radius=86.0)
        deps = DefaultBypassDependencies(validator=validator)
        provides = DefaultBypassFactory.create(dependencies=deps)
        self.assertIsInstance(provides, BypassProvides)
        self.assertIsInstance(provides.planner, IDeadZoneBypassPlanner)
        self.assertIsInstance(provides.calculator, ITangentArcCalculator)

    def test_get_version(self) -> None:
        '''
            Verifies that get_version returns a valid version string.
        '''
        version = DefaultBypassFactory.get_version()
        self.assertIsInstance(version, str)
        self.assertTrue(len(version) > 0)


if __name__ == '__main__':
    main()
