# -*- coding: UTF-8 -*-

'''
Module
    box_test.py
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
    Unit tests for BoxObstacle data model.
'''

from __future__ import annotations

from dataclasses import FrozenInstanceError
from unittest import TestCase, main

from scaralang.core.model.trajectory.obstacle.box import BoxObstacle

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class BoxObstacleTest(TestCase):
    '''Unit tests validating BoxObstacle properties and immutability.'''

    def test_instantiation(self) -> None:
        '''
            Verifies valid attribute storage.

            :exceptions: None.
        '''
        box = BoxObstacle(x_min=50.0, x_max=90.0, y_min=-70.0, y_max=-30.0)
        self.assertEqual(box.x_min, 50.0)
        self.assertEqual(box.x_max, 90.0)
        self.assertEqual(box.y_min, -70.0)
        self.assertEqual(box.y_max, -30.0)

    def test_immutability(self) -> None:
        '''
            Verifies frozen instance raises FrozenInstanceError.

            :exceptions: None.
        '''
        box = BoxObstacle(x_min=0.0, x_max=10.0, y_min=0.0, y_max=10.0)
        with self.assertRaises(FrozenInstanceError):
            setattr(box, 'x_max', 20.0)


if __name__ == '__main__':
    main()
