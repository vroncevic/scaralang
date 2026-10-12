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
    Unit tests for ITangentArcCalculator structural protocol conformance.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.service.trajectory.avoidance.bypass.arc.calculator import TangentArcCalculator
from scaralang.core.service.trajectory.avoidance.bypass.arc.factory import ArcFactory
from scaralang.core.service.trajectory.avoidance.bypass.arc.icalculator import ITangentArcCalculator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.8'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestITangentArcCalculator(TestCase):
    '''
        Test cases verifying ITangentArcCalculator protocol structural subtyping.

        It defines:

            :methods:
                | test_structural_conformance - Verifies TangentArcCalculator satisfies protocol.
                | test_factory_return_conformance - Verifies factory returns protocol instance.
    '''

    def test_structural_conformance(self) -> None:
        '''
            Verifies concrete TangentArcCalculator satisfies ITangentArcCalculator protocol.
        '''
        calculator = TangentArcCalculator()
        self.assertIsInstance(calculator, ITangentArcCalculator)

    def test_factory_return_conformance(self) -> None:
        '''
            Verifies factory returns instance satisfying ITangentArcCalculator protocol.
        '''
        provides = ArcFactory.create()
        self.assertIsInstance(provides.calculator, ITangentArcCalculator)


if __name__ == '__main__':
    main()
