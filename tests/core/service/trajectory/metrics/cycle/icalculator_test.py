# -*- coding: UTF-8 -*-

'''
Module
    icalculator_test.py
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

from unittest import TestCase, main

from scaralang.core.service.trajectory.metrics.cycle.calculator import CycleTimeCalculator
from scaralang.core.service.trajectory.metrics.cycle.factory import CycleFactory
from scaralang.core.service.trajectory.metrics.cycle.icalculator import ICycleTimeCalculator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.8'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class NonConformingCycleCalculator:  # pylint: disable=too-few-public-methods
    '''Dummy class not implementing ICycleTimeCalculator.'''


class TestICycleTimeCalculator(TestCase):
    '''
        Test cases for ICycleTimeCalculator structural protocol conformance.

        It defines:

            :methods:
                | test_structural_conformance - Verifies CycleTimeCalculator satisfies protocol.
                | test_factory_return_conformance - Verifies factory returns protocol instance.
                | test_non_conforming_instance - Verifies non-conforming object rejected.
                | test_calculator_name_property - Verifies name property matches expectation.
    '''

    def test_structural_conformance(self) -> None:
        '''Verifies concrete CycleTimeCalculator satisfies ICycleTimeCalculator protocol.'''
        calc = CycleTimeCalculator()
        self.assertIsInstance(calc, ICycleTimeCalculator)

    def test_factory_return_conformance(self) -> None:
        '''Verifies factory returns instance satisfying ICycleTimeCalculator.'''
        provides = CycleFactory.create()
        self.assertIsInstance(provides.calculator, ICycleTimeCalculator)

    def test_non_conforming_instance(self) -> None:
        '''Verifies non-conforming object is rejected by runtime_checkable protocol.'''
        dummy = NonConformingCycleCalculator()
        self.assertNotIsInstance(dummy, ICycleTimeCalculator)

    def test_calculator_name_property(self) -> None:
        '''Verifies name property returns correct identifier string.'''
        calc = CycleTimeCalculator()
        self.assertEqual(calc.name, 'cycle_time_calculator')


if __name__ == '__main__':
    main()
