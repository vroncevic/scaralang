# -*- coding: UTF-8 -*-

'''
Module
    solution_test.py
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
    Unit tests for pure data model ScaraJoints.
'''

from __future__ import annotations

from dataclasses import FrozenInstanceError
from unittest import TestCase, main

from scaralang.core.model.kinematics.solver.solution import ScaraJoints
from scaralang.core.model.kinematics.solver.status import IkStatus

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class SolutionTest(TestCase):
    '''
        Unit tests validating ScaraJoints initialization, slots, and immutability.

        It defines:

            :methods:
                | test_instantiation - Verifies field values on initialization.
                | test_immutability - Verifies frozen dataclass prevents mutation.
                | test_equality - Verifies value-object equality semantics.
    '''

    def test_instantiation(self) -> None:
        '''
            Verify field values on initialization.

            :exceptions: None.
        '''
        joints = ScaraJoints(
            theta1=0.5,
            theta2=-0.3,
            z=50.0,
            theta4=0.2,
            reachable=True,
            status=IkStatus.SUCCESS,
        )
        self.assertEqual(joints.theta1, 0.5)
        self.assertEqual(joints.theta2, -0.3)
        self.assertEqual(joints.z, 50.0)
        self.assertEqual(joints.theta4, 0.2)
        self.assertTrue(joints.reachable)
        self.assertEqual(joints.status, IkStatus.SUCCESS)

    def test_immutability(self) -> None:
        '''
            Verify frozen dataclass prevents mutation.

            :exceptions: None.
        '''
        joints = ScaraJoints(
            theta1=0.0,
            theta2=0.0,
            z=0.0,
            theta4=0.0,
            reachable=False,
            status=IkStatus.INNER_DEADZONE,
        )
        with self.assertRaises(FrozenInstanceError):
            setattr(joints, 'theta4', 1.0)

    def test_equality(self) -> None:
        '''
            Verify value-object equality semantics.

            :exceptions: None.
        '''
        j1 = ScaraJoints(
            theta1=0.5,
            theta2=-0.3,
            z=50.0,
            theta4=0.2,
            reachable=True,
            status=IkStatus.SUCCESS,
        )
        j2 = ScaraJoints(
            theta1=0.5,
            theta2=-0.3,
            z=50.0,
            theta4=0.2,
            reachable=True,
            status=IkStatus.SUCCESS,
        )
        j3 = ScaraJoints(
            theta1=0.5,
            theta2=-0.3,
            z=50.0,
            theta4=0.8,
            reachable=True,
            status=IkStatus.SUCCESS,
        )
        self.assertEqual(j1, j2)
        self.assertNotEqual(j1, j3)


if __name__ == '__main__':
    main()
