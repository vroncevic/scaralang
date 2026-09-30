# -*- coding: UTF-8 -*-

'''
Module
    waypoint_step_dispatcher_test.py
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
    Unit tests for WaypointStepDispatcher class.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from scaralang.core.model.dsl.binary.step import Step
from scaralang.core.model.trajectory.waypoint import Waypoint
from scaralang.core.service.compiler.binary.step.iwaypoint_step_dispatcher import IWaypointStepDispatcher
from scaralang.core.service.compiler.binary.step.waypoint_step_dispatcher import WaypointStepDispatcher

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestWaypointStepDispatcher(TestCase):
    '''
        Test cases verifying WaypointStepDispatcher.

        It defines:

            :methods:
                | test_dispatch_motion_waypoint - Verifies dispatch of motion point.
                | test_dispatch_command_waypoint - Verifies dispatch of command point.
    '''

    def setUp(self) -> None:
        '''Sets up test mocks and dispatcher instance.'''
        self.mock_command_compiler = MagicMock()
        self.mock_motion_compiler = MagicMock()
        self.dispatcher = WaypointStepDispatcher(
            command_compiler=self.mock_command_compiler,
            motion_compiler=self.mock_motion_compiler,
        )

    def test_dispatch_motion_waypoint(self) -> None:
        '''Verifies dispatching motion waypoint delegates to motion compiler.'''
        wp = Waypoint(x=100.0, y=100.0, z=0.0, speed=50.0)
        expected_step = MagicMock(spec=Step)
        self.mock_motion_compiler.compile_motion_step.return_value = (
            expected_step,
            (0.5, 0.5, 0.0, 0.0),
        )

        steps = self.dispatcher.dispatch_steps(waypoints=(wp,))
        self.assertEqual(len(steps), 1)
        self.assertEqual(steps[0], expected_step)
        self.mock_motion_compiler.compile_motion_step.assert_called_once_with(
            waypoint=wp,
            seq_num=0,
            prev_angles=(0.0, 0.0, 0.0, 0.0),
            line_num=1,
        )

    def test_dispatch_command_waypoint(self) -> None:
        '''Verifies dispatching command waypoint delegates to command compiler.'''
        wp = Waypoint(x=0.0, y=0.0, z=0.0, speed=50.0, command='PUMP ON')
        expected_step = MagicMock(spec=Step)
        self.mock_command_compiler.compile_command_step.return_value = expected_step

        steps = self.dispatcher.dispatch_steps(waypoints=(wp,))
        self.assertEqual(len(steps), 1)
        self.assertEqual(steps[0], expected_step)
        self.mock_command_compiler.compile_command_step.assert_called_once_with(
            command='PUMP ON',
            seq_num=0,
            line_num=1,
        )

    def test_protocol_conformance(self) -> None:
        '''Verifies WaypointStepDispatcher satisfies IWaypointStepDispatcher.'''
        self.assertIsInstance(self.dispatcher, IWaypointStepDispatcher)


if __name__ == '__main__':
    main()
