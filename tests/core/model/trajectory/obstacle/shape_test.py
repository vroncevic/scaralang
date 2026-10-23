# -*- coding: UTF-8 -*-

'''
Module
    shape_test.py
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
    Unit tests for ObstacleShape enumeration.
'''

from __future__ import annotations

from unittest import TestCase, main

from scaralang.core.model.trajectory.obstacle.shape import ObstacleShape

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ObstacleShapeTest(TestCase):
    '''Unit tests validating ObstacleShape enumeration members and values.'''

    def test_members_count(self) -> None:
        '''
            Verifies total count of obstacle shape types.

            :exceptions: None.
        '''
        self.assertEqual(len(ObstacleShape), 2)

    def test_member_values(self) -> None:
        '''
            Verifies string representation values.

            :exceptions: None.
        '''
        self.assertEqual(ObstacleShape.BOX, 'BOX')
        self.assertEqual(ObstacleShape.CIRCLE, 'CIRCLE')

    def test_lookup_by_value(self) -> None:
        '''
            Verifies enum instantiation from string.

            :exceptions: None.
        '''
        self.assertIs(ObstacleShape('BOX'), ObstacleShape.BOX)
        self.assertIs(ObstacleShape('CIRCLE'), ObstacleShape.CIRCLE)

    def test_invalid_shape_raises_value_error(self) -> None:
        '''
            Verifies ValueError on invalid string.

            :exceptions: None.
        '''
        with self.assertRaises(ValueError):
            ObstacleShape('POLYGON')


if __name__ == '__main__':
    main()
