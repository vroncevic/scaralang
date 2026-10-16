# -*- coding: UTF-8 -*-

'''
Module
    joint_angles_test.py
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
    Unit test suite for JointAngles model.
'''

from __future__ import annotations

from dataclasses import FrozenInstanceError
from unittest import TestCase, main

from scaralang.core.model.kinematics.joint_angles import JointAngles

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.9'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class JointAnglesTestCase(TestCase):
    '''
        Defines test cases for JointAngles model.

        It defines:

            :methods:
                | test_creation_attributes - Verifies attributes match constructor arguments.
                | test_frozen_immutability - Verifies model is frozen and immutable.
    '''

    def test_creation_attributes(self) -> None:
        '''
            Verifies JointAngles attributes match constructor arguments.

            :exceptions: None.
        '''
        angles = JointAngles(theta1=0.5, theta2=-0.25, z=15.0, theta4=1.57)
        self.assertEqual(angles.theta1, 0.5)
        self.assertEqual(angles.theta2, -0.25)
        self.assertEqual(angles.z, 15.0)
        self.assertEqual(angles.theta4, 1.57)

    def test_frozen_immutability(self) -> None:
        '''
            Verifies JointAngles raises FrozenInstanceError on mutation.

            :exceptions: None.
        '''
        angles = JointAngles(theta1=0.1, theta2=0.2, z=10.0, theta4=0.4)
        with self.assertRaises(FrozenInstanceError):
            angles.theta1 = 0.99


if __name__ == '__main__':
    main()
