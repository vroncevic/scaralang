# -*- coding: UTF-8 -*-

'''
Module
    constraint_test.py
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
    Unit tests for ConstraintType enumeration model.
'''

from __future__ import annotations

from unittest import TestCase, main

from scaralang.core.model.trajectory.metrics.constraint import ConstraintType

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ConstraintTypeTest(TestCase):
    '''Unit tests validating ConstraintType enumeration members and string values.'''

    def test_enumeration_members_count(self) -> None:
        '''
            Verify total number of defined constraint types.

            :exceptions: None.
        '''
        self.assertEqual(len(ConstraintType), 2)

    def test_string_representation(self) -> None:
        '''
            Verify that constraint type members match expected string values.

            :exceptions: None.
        '''
        self.assertEqual(ConstraintType.ACCELERATION, 'ACCELERATION')
        self.assertEqual(ConstraintType.VELOCITY, 'VELOCITY')

    def test_lookup_by_value(self) -> None:
        '''
            Verify enum instantiation from raw string values.

            :exceptions: None.
        '''
        self.assertIs(ConstraintType('ACCELERATION'), ConstraintType.ACCELERATION)
        self.assertIs(ConstraintType('VELOCITY'), ConstraintType.VELOCITY)

    def test_invalid_constraint_raises_value_error(self) -> None:
        '''
            Verify that invalid string values raise ValueError.

            :exceptions: None.
        '''
        with self.assertRaises(ValueError):
            ConstraintType('JERK')


if __name__ == '__main__':
    main()
