# -*- coding: UTF-8 -*-

'''
Module
    compiler_pose_state_test.py
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
    Unit tests for CompilerPoseState model.
'''

from __future__ import annotations

from unittest import TestCase, main

from scaralang.core.model.dsl.compiler.compiler_pose_state import CompilerPoseState
from scaralang.core.model.kinematics.elbow_config import ElbowConfig

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.6'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class CompilerPoseStateTest(TestCase):
    '''
        Validates CompilerPoseState default initialization, custom values, and mutation.
    '''

    def test_default_values(self) -> None:
        '''
            Verifies default initialization coordinates and elbow solution.
        '''
        pose = CompilerPoseState()
        self.assertEqual(pose.current_x, 150.0)
        self.assertEqual(pose.current_y, 0.0)
        self.assertEqual(pose.current_z, 20.0)
        self.assertEqual(pose.current_phi, 0.0)
        self.assertEqual(pose.elbow_config, ElbowConfig.RIGHT)

    def test_custom_values(self) -> None:
        '''
            Verifies custom values assignment on instantiation.
        '''
        pose = CompilerPoseState(
            current_x=200.0,
            current_y=100.0,
            current_z=50.0,
            current_phi=90.0,
            elbow_config=ElbowConfig.LEFT,
        )
        self.assertEqual(pose.current_x, 200.0)
        self.assertEqual(pose.current_y, 100.0)
        self.assertEqual(pose.current_z, 50.0)
        self.assertEqual(pose.current_phi, 90.0)
        self.assertEqual(pose.elbow_config, ElbowConfig.LEFT)

    def test_state_mutation(self) -> None:
        '''
            Verifies in-place mutation of pose coordinates.
        '''
        pose = CompilerPoseState()
        pose.current_x = 120.0
        pose.current_y = -30.0
        pose.current_z = 15.0
        pose.current_phi = 45.0
        pose.elbow_config = ElbowConfig.LEFT

        self.assertEqual(pose.current_x, 120.0)
        self.assertEqual(pose.current_y, -30.0)
        self.assertEqual(pose.current_z, 15.0)
        self.assertEqual(pose.current_phi, 45.0)
        self.assertEqual(pose.elbow_config, ElbowConfig.LEFT)


if __name__ == '__main__':
    main()
