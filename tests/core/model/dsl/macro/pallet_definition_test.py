# -*- coding: UTF-8 -*-

'''
Module
    pallet_definition_test.py
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
    Unit testing for PalletDefinition domain model.
'''

from __future__ import annotations

from dataclasses import FrozenInstanceError
from unittest import TestCase, main

from scaralang.core.model.dsl.macro.pallet_definition import PalletDefinition
from scaralang.core.model.kinematics.point_2d import Point2D

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.7'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class PalletDefinitionTest(TestCase):
    '''
        Validates PalletDefinition initialization, attributes, and immutability.
    '''

    def test_initialization_and_attributes(self) -> None:
        '''
            Verifies that valid parameters correctly populate fields.
        '''
        pallet = PalletDefinition(
            name='PALLET_A',
            rows=3,
            cols=4,
            dx=25.0,
            dy=30.0,
            start=Point2D(x=100.0, y=50.0),
        )
        self.assertEqual(pallet.name, 'PALLET_A')
        self.assertEqual(pallet.rows, 3)
        self.assertEqual(pallet.cols, 4)
        self.assertAlmostEqual(pallet.dx, 25.0)
        self.assertAlmostEqual(pallet.dy, 30.0)
        self.assertEqual(pallet.start, Point2D(x=100.0, y=50.0))
        self.assertAlmostEqual(pallet.start.x, 100.0)
        self.assertAlmostEqual(pallet.start.y, 50.0)

    def test_immutability(self) -> None:
        '''
            Verifies that PalletDefinition instances are immutable.
        '''
        pallet = PalletDefinition(
            name='CONST',
            rows=1,
            cols=1,
            dx=5.0,
            dy=5.0,
            start=Point2D(x=0.0, y=0.0),
        )
        with self.assertRaises(FrozenInstanceError):
            pallet.name = 'MUTATED'


if __name__ == '__main__':
    main()
