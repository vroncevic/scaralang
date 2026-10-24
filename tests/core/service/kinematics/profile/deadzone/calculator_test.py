# -*- coding: UTF-8 -*-

'''
Module
    calculator_test.py
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
    Unit tests for DeadzoneCalculator implementation.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.service.kinematics.profile.deadzone.calculator import DeadzoneCalculator
from scaralang.core.service.kinematics.profile.deadzone.icalculator import IDeadzoneCalculator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestDeadzoneCalculator(TestCase):
    '''
        Test cases verifying DeadzoneCalculator implementation.

        It defines:

            :methods:
                | setUp - Initializes test environment and calculator instance.
                | test_structural_protocol_compliance - Verifies protocol adherence.
                | test_calculate_radius - Verifies deadzone radius computation.
                | test_get_version - Verifies version string retrieval.
    '''

    def setUp(self) -> None:
        '''
            Sets up calculator test fixture.

            :exceptions: None.
        '''
        self.calculator: DeadzoneCalculator = DeadzoneCalculator()

    def test_structural_protocol_compliance(self) -> None:
        '''
            Verifies calculator implements IDeadzoneCalculator protocol.

            :exceptions: None.
        '''
        self.assertTrue(isinstance(self.calculator, IDeadzoneCalculator))

    def test_calculate_radius(self) -> None:
        '''
            Verifies analytical dead zone radius calculation.

            :exceptions: None.
        '''
        r_dead: float = self.calculator.calculate_radius(
            l1=150.0, l2=150.0, j2_max_rad=2.61799
        )
        self.assertAlmostEqual(r_dead, 77.646, places=2)

    def test_get_version(self) -> None:
        '''
            Verifies calculator version string retrieval.

            :exceptions: None.
        '''
        self.assertEqual(self.calculator.get_version(), '1.1.1')


if __name__ == '__main__':
    main()
