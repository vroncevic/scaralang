# -*- coding: UTF-8 -*-

'''
Module
    repl_pose_state_test.py
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
    Unit tests for ReplPoseState data model.
'''

from __future__ import annotations

from unittest import TestCase, main

from scaralang.core.model.repl.repl_pose_state import ReplPoseState

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.6'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ReplPoseStateTest(TestCase):
    '''Unit tests validating ReplPoseState dataclass default and custom initialization.'''

    def test_default_initialization(self) -> None:
        '''Verify default values on fresh REPL pose state.'''
        pose = ReplPoseState()
        self.assertEqual(pose.current_x, 0.0)
        self.assertEqual(pose.current_y, 0.0)
        self.assertEqual(pose.current_z, 0.0)
        self.assertEqual(pose.current_theta4, 0.0)

    def test_custom_initialization(self) -> None:
        '''Verify custom field assignment.'''
        pose = ReplPoseState(
            current_x=150.0,
            current_y=75.0,
            current_z=10.0,
            current_theta4=45.0,
        )
        self.assertEqual(pose.current_x, 150.0)
        self.assertEqual(pose.current_y, 75.0)
        self.assertEqual(pose.current_z, 10.0)
        self.assertEqual(pose.current_theta4, 45.0)

    def test_immutability(self) -> None:
        '''Verify that attributes cannot be modified on frozen dataclass.'''
        pose = ReplPoseState()
        with self.assertRaises(AttributeError):
            setattr(pose, 'current_x', 10.0)


if __name__ == '__main__':
    main()
