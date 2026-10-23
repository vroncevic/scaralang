# -*- coding: UTF-8 -*-

'''
Module
    steps_test.py
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
    Unit test suite for JointStepCoordinates model.
'''

from __future__ import annotations

from dataclasses import FrozenInstanceError
from unittest import TestCase, main

from scaralang.core.model.kinematics.pose.steps import JointStepCoordinates

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class StepsTest(TestCase):
    '''
        Defines test cases for JointStepCoordinates model.

        It defines:

            :methods:
                | test_creation_attributes - Verifies attributes match constructor arguments.
                | test_frozen_immutability - Verifies model is frozen and immutable.
    '''

    def test_creation_attributes(self) -> None:
        '''
            Verifies JointStepCoordinates attributes match constructor arguments.

            :exceptions: None.
        '''
        coords = JointStepCoordinates(j1=100, j2=200, z=300, j4=400)
        self.assertEqual(coords.j1, 100)
        self.assertEqual(coords.j2, 200)
        self.assertEqual(coords.z, 300)
        self.assertEqual(coords.j4, 400)

    def test_frozen_immutability(self) -> None:
        '''
            Verifies JointStepCoordinates raises FrozenInstanceError on mutation.

            :exceptions: None.
        '''
        coords = JointStepCoordinates(j1=10, j2=20, z=30, j4=40)
        with self.assertRaises(FrozenInstanceError):
            setattr(coords, 'j1', 99)


if __name__ == '__main__':
    main()
