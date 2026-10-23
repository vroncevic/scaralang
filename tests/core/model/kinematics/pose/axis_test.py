# -*- coding: UTF-8 -*-

'''
Module
    axis_test.py
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
    Unit tests for AxisName enumeration model.
'''

from __future__ import annotations

from unittest import TestCase, main

from scaralang.core.model.kinematics.pose.axis import AxisName

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class AxisTest(TestCase):
    '''
        Unit tests validating AxisName enumeration members and string values.

        It defines:

            :methods:
                | test_enumeration_members_count - Verifies total axis count.
                | test_string_representation - Verifies member string representations.
                | test_lookup_by_value - Verifies enum member lookup.
    '''

    def test_enumeration_members_count(self) -> None:
        '''
            Verify total number of defined manipulator axes.

            :exceptions: None.
        '''
        self.assertEqual(len(AxisName), 4)

    def test_string_representation(self) -> None:
        '''
            Verify that manipulator axis members match expected string values.

            :exceptions: None.
        '''
        self.assertEqual(AxisName.J1, 'J1')
        self.assertEqual(AxisName.J2, 'J2')
        self.assertEqual(AxisName.Z, 'Z')
        self.assertEqual(AxisName.J4, 'J4')

    def test_lookup_by_value(self) -> None:
        '''
            Verify member lookup from string values.

            :exceptions: None.
        '''
        self.assertIs(AxisName('J1'), AxisName.J1)
        self.assertIs(AxisName('J2'), AxisName.J2)
        self.assertIs(AxisName('Z'), AxisName.Z)
        self.assertIs(AxisName('J4'), AxisName.J4)


if __name__ == '__main__':
    main()
