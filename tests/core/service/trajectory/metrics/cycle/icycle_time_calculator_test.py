# -*- coding: UTF-8 -*-

'''
Module
    icycle_time_calculator_test.py
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
    Unit tests for ICycleTimeCalculator protocol.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.service.trajectory.metrics.cycle.cycle_time_calculator import CycleTimeCalculator
from scaralang.core.service.trajectory.metrics.cycle.cycle_time_calculator_factory import CycleTimeCalculatorFactory
from scaralang.core.service.trajectory.metrics.cycle.icycle_time_calculator import ICycleTimeCalculator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestICycleTimeCalculator(TestCase):
    '''
        Test cases for ICycleTimeCalculator protocol structural typing.

        It defines:

            :methods:
                | test_structural_conformance - Verifies calculator satisfies protocol.
                | test_factory_conformance - Verifies factory returns protocol instance.
                | test_calculator_name - Verifies calculator name property.
    '''

    def test_structural_conformance(self) -> None:
        '''Verifies CycleTimeCalculator satisfies protocol.'''
        calculator = CycleTimeCalculator()
        self.assertIsInstance(calculator, ICycleTimeCalculator)

    def test_factory_conformance(self) -> None:
        '''Verifies factory returns instance satisfying protocol.'''
        calculator = CycleTimeCalculatorFactory.create()
        self.assertIsInstance(calculator, ICycleTimeCalculator)

    def test_calculator_name(self) -> None:
        '''Verifies calculator name property.'''
        calculator = CycleTimeCalculator()
        self.assertEqual(calculator.name, 'cycle_time_calculator')


if __name__ == '__main__':
    main()
