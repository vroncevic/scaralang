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
    Unit tests for CycleFactory.
'''

from __future__ import annotations

from unittest import TestCase, main

from scaralang.core.service.trajectory.metrics.cycle.factory import CycleFactory
from scaralang.core.service.trajectory.metrics.cycle.icalculator import ICycleTimeCalculator
from scaralang.core.service.trajectory.metrics.cycle.provides import CycleProvides

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestCycleFactory(TestCase):
    '''
        Test cases for CycleFactory component creation.

        It defines:

            :methods:
                | test_create - Verifies factory returns CycleProvides bundle.
                | test_get_version - Verifies factory version string format.
    '''

    def test_create(self) -> None:
        '''Verifies factory instantiates and wires CycleProvides bundle.'''
        bundle = CycleFactory.create()
        self.assertIsInstance(bundle, CycleProvides)
        self.assertIsInstance(bundle.calculator, ICycleTimeCalculator)

    def test_get_version(self) -> None:
        '''Verifies factory returns valid semantic version string.'''
        version_str = CycleFactory.get_version()
        self.assertIsInstance(version_str, str)
        self.assertTrue(len(version_str) > 0)


if __name__ == '__main__':
    main()
