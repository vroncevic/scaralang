# -*- coding: UTF-8 -*-

'''
Module
    itangent_heading_calculator_test.py
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
    Unit tests for ITangentHeadingCalculator protocol.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.service.compiler.primitive.motion.cartesian.itangent_heading_calculator import ITangentHeadingCalculator
from scaralang.core.service.compiler.primitive.motion.cartesian.tangent_heading_calculator import TangentHeadingCalculator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.9'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DummyNonConformingCalculator:  # pylint: disable=too-few-public-methods
    '''
        Dummy class missing required protocol methods.
    '''

    def get_version(self) -> str:
        '''
            Gets dummy version.
        '''
        return '1.0.0'


class TestITangentHeadingCalculator(TestCase):
    '''
        Test cases verifying ITangentHeadingCalculator protocol.

        It defines:

            :methods:
                | test_conforming_instance - Verifies conforming instance passes isinstance.
                | test_non_conforming_instance - Verifies non-conforming instance fails.
    '''

    def test_conforming_instance(self) -> None:
        '''
            Verifies conforming instance passes structural typing check.
        '''
        calculator = TangentHeadingCalculator()
        self.assertIsInstance(calculator, ITangentHeadingCalculator)

    def test_non_conforming_instance(self) -> None:
        '''
            Verifies non-conforming instance fails structural typing check.
        '''
        calculator = DummyNonConformingCalculator()
        self.assertNotIsInstance(calculator, ITangentHeadingCalculator)


if __name__ == '__main__':
    main()
