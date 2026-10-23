# -*- coding: UTF-8 -*-

'''
Module
    repl_status_presenter_test.py
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
    Unit tests for ReplStatusPresenter class.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.model.dsl.ast.speed_mode import SpeedMode
from scaralang.core.model.dsl.ast.zone_mode import ZoneMode
from scaralang.core.model.repl.pose import ReplPoseState
from scaralang.core.model.repl.context import ReplSessionContext
from scaralang.infrastructure.cli.repl.presentation.repl_status_presenter import ReplStatusPresenter

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestReplStatusPresenter(TestCase):
    '''
        Test cases verifying ReplStatusPresenter functionality.

        It defines:

            :attributes:
                | presenter - ReplStatusPresenter under test.
                | context - Fixture session context.
            :methods:
                | setUp - Initializes test fixtures.
                | test_present_help - Verifies help manual formatting.
                | test_present_status - Verifies state summary formatting.
                | test_present_pose - Verifies Cartesian pose line formatting.
    '''

    def setUp(self) -> None:
        '''
            Sets up test fixtures before each test method.

            :exceptions: None.
        '''
        self.presenter: ReplStatusPresenter = ReplStatusPresenter()
        self.context: ReplSessionContext = ReplSessionContext(
            pose=ReplPoseState(
                current_x=150.0,
                current_y=75.5,
                current_z=20.0,
                current_theta4=45.0,
            ),
            elbow_left=True,
            speed_mode=SpeedMode.RAPID,
            zone_mode=ZoneMode.FINE,
            pump_active=True,
            valve_active=False,
        )

    def test_present_help(self) -> None:
        '''
            Verifies presentation of REPL help manual and command catalog.

            :exceptions: None.
        '''
        help_text: str = self.presenter.present_help()
        self.assertIn('Built-in REPL Commands:', help_text)
        self.assertIn('help, ?', help_text)
        self.assertIn('MOVE_L', help_text)
        self.assertIn('PUMP', help_text)

    def test_present_status(self) -> None:
        '''
            Verifies presentation of active robot kinematics, modes and pneumatics.

            :exceptions: None.
        '''
        status_text: str = self.presenter.present_status(context=self.context)
        self.assertIn('Current Robot State:', status_text)
        self.assertIn('X=150.00 mm', status_text)
        self.assertIn('Y=75.50 mm', status_text)
        self.assertIn('Z=20.00 mm', status_text)
        self.assertIn('Phi=45.00°', status_text)
        self.assertIn('Elbow=LEFT', status_text)
        self.assertIn('SpeedMode=RAPID', status_text)
        self.assertIn('Pump=ACTIVE', status_text)
        self.assertIn('Valve=INACTIVE', status_text)

    def test_present_pose(self) -> None:
        '''
            Verifies presentation of Cartesian pose coordinates.

            :exceptions: None.
        '''
        pose_text: str = self.presenter.present_pose(context=self.context)
        self.assertTrue(pose_text.startswith('Pose: '))
        self.assertIn('X=150.00 mm', pose_text)
        self.assertIn('Y=75.50 mm', pose_text)
        self.assertIn('Z=20.00 mm', pose_text)
        self.assertIn('Phi=45.00°', pose_text)


if __name__ == '__main__':
    main()
