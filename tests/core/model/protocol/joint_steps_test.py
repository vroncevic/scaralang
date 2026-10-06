# -*- coding: UTF-8 -*-

'''
Module
    joint_steps_test.py
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
    Unit tests for JointSteps protocol domain model.
'''

from __future__ import annotations

from dataclasses import FrozenInstanceError
from unittest import TestCase, main

from scaralang.core.model.protocol.joint_steps import JointSteps

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.6'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class JointStepsTest(TestCase):
    '''Unit tests validating JointSteps purity, immutability, and attribute values.'''

    def test_instantiation_and_attributes(self) -> None:
        '''Verify proper initialization and access of JointSteps fields.'''
        steps = JointSteps(
            target_j1_steps=1000,
            target_j2_steps=2000,
            target_z_steps=-500,
            target_j4_steps=300,
            duration_us=50000,
            feedrate_scale=100,
        )
        self.assertEqual(steps.target_j1_steps, 1000)
        self.assertEqual(steps.target_j2_steps, 2000)
        self.assertEqual(steps.target_z_steps, -500)
        self.assertEqual(steps.target_j4_steps, 300)
        self.assertEqual(steps.duration_us, 50000)
        self.assertEqual(steps.feedrate_scale, 100)

    def test_frozen_immutability(self) -> None:
        '''Verify that modifying attributes on JointSteps raises FrozenInstanceError.'''
        steps = JointSteps(
            target_j1_steps=100,
            target_j2_steps=200,
            target_z_steps=300,
            target_j4_steps=400,
            duration_us=10000,
            feedrate_scale=50,
        )
        with self.assertRaises(FrozenInstanceError):
            setattr(steps, 'target_j1_steps', 999)

    def test_equality(self) -> None:
        '''Verify that two JointSteps instances with identical fields evaluate equal.'''
        steps_a = JointSteps(
            target_j1_steps=100,
            target_j2_steps=200,
            target_z_steps=300,
            target_j4_steps=400,
            duration_us=10000,
            feedrate_scale=50,
        )
        steps_b = JointSteps(
            target_j1_steps=100,
            target_j2_steps=200,
            target_z_steps=300,
            target_j4_steps=400,
            duration_us=10000,
            feedrate_scale=50,
        )
        self.assertEqual(steps_a, steps_b)


if __name__ == '__main__':
    main()
