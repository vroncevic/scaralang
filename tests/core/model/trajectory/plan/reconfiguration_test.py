# -*- coding: UTF-8 -*-

'''
Module
    reconfiguration_test.py
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
    Unit tests for ReconfigurationRequest domain model.
'''

from __future__ import annotations

from dataclasses import FrozenInstanceError
from unittest import TestCase, main

from scaralang.core.model.kinematics.solver.elbow import ElbowConfig
from scaralang.core.model.trajectory.plan.reconfiguration import ReconfigurationRequest
from scaralang.core.model.trajectory.plan.waypoint import Waypoint

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ReconfigurationRequestTest(TestCase):
    '''Unit tests validating ReconfigurationRequest purity and immutability.'''

    def test_instantiation_and_attributes(self) -> None:
        '''
            Verify proper initialization and access of ReconfigurationRequest fields.

            :exceptions: None.
        '''
        wp_from = Waypoint(
            x=100.0,
            y=50.0,
            z=10.0,
            phi=0.0,
            speed=20.0,
            name='P1',
            command='MOVE',
        )
        wp_to = Waypoint(
            x=-100.0,
            y=50.0,
            z=10.0,
            phi=0.0,
            speed=20.0,
            name='P2',
            command='MOVE',
        )
        req = ReconfigurationRequest(
            from_waypoint=wp_from,
            to_waypoint=wp_to,
            from_elbow=ElbowConfig.RIGHT,
            to_elbow=ElbowConfig.LEFT,
            z_safe=30.0,
        )
        self.assertEqual(req.from_waypoint, wp_from)
        self.assertEqual(req.to_waypoint, wp_to)
        self.assertEqual(req.from_elbow, ElbowConfig.RIGHT)
        self.assertEqual(req.to_elbow, ElbowConfig.LEFT)
        self.assertEqual(req.z_safe, 30.0)

    def test_frozen_immutability(self) -> None:
        '''
            Verify that modifying attributes on ReconfigurationRequest raises FrozenInstanceError.

            :exceptions: None.
        '''
        wp_from = Waypoint(
            x=100.0,
            y=50.0,
            z=10.0,
            phi=0.0,
            speed=20.0,
            name='P1',
            command='MOVE',
        )
        wp_to = Waypoint(
            x=-100.0,
            y=50.0,
            z=10.0,
            phi=0.0,
            speed=20.0,
            name='P2',
            command='MOVE',
        )
        req = ReconfigurationRequest(
            from_waypoint=wp_from,
            to_waypoint=wp_to,
            from_elbow=ElbowConfig.RIGHT,
            to_elbow=ElbowConfig.LEFT,
            z_safe=30.0,
        )
        with self.assertRaises(FrozenInstanceError):
            setattr(req, 'z_safe', 50.0)


if __name__ == '__main__':
    main()
