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
    Unit tests for JacobianCalculatorFactory.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.model.kinematics.profile.link import LinkDimensions
from scaralang.core.service.kinematics.solver.numerical.jacobian.calculator import JacobianCalculator
from scaralang.core.service.kinematics.solver.numerical.jacobian.factory import JacobianCalculatorFactory
from scaralang.core.service.kinematics.solver.numerical.jacobian.icalculator import IJacobianCalculator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestJacobianCalculatorFactory(TestCase):
    '''
        Test cases verifying JacobianCalculatorFactory.

        It defines:

            :methods:
                | test_create - Verifies factory returns configured IJacobianCalculator instance.
                | test_get_version - Verifies factory returns version string.
    '''

    def test_create(self) -> None:
        '''
            Verifies factory creates working IJacobianCalculator.

            :exceptions: None.
        '''
        links = LinkDimensions(l1=150.0, l2=120.0)
        calc: IJacobianCalculator = JacobianCalculatorFactory.create(links=links)
        self.assertIsInstance(calc, IJacobianCalculator)
        self.assertIsInstance(calc, JacobianCalculator)

    def test_get_version(self) -> None:
        '''
            Verifies factory version string.

            :exceptions: None.
        '''
        self.assertEqual(JacobianCalculatorFactory.get_version(), '1.1.0')


if __name__ == '__main__':
    main()
