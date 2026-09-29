# -*- coding: UTF-8 -*-

'''
Module
    axis_mask_test.py
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
    Unit tests for AxisMask domain enumeration.
'''

from __future__ import annotations

from unittest import TestCase

from scaralang.core.model.motor.axis_mask import AxisMask

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class AxisMaskTest(TestCase):
    '''
        Tests for AxisMask IntEnum members and bitwise operations.
    '''

    def test_members(self) -> None:
        '''Verifies all enum member values.'''
        self.assertEqual(AxisMask.NONE.value, 0x00)
        self.assertEqual(AxisMask.J1.value, 0x01)
        self.assertEqual(AxisMask.J2.value, 0x02)
        self.assertEqual(AxisMask.Z.value, 0x04)
        self.assertEqual(AxisMask.J4.value, 0x08)
        self.assertEqual(AxisMask.ALL.value, 0x0F)

    def test_bitwise_combination(self) -> None:
        '''Verifies bitwise OR across joint axes equals ALL.'''
        combined = AxisMask.J1 | AxisMask.J2 | AxisMask.Z | AxisMask.J4
        self.assertEqual(combined, AxisMask.ALL.value)

    def test_instantiation_from_int(self) -> None:
        '''Verifies instantiation from integer value.'''
        self.assertEqual(AxisMask(0x0F), AxisMask.ALL)
        self.assertEqual(AxisMask(0x00), AxisMask.NONE)
