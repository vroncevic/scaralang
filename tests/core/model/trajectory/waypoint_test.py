# -*- coding: UTF-8 -*-

'''
Module
    waypoint_test.py
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
    Unit tests for Waypoint trajectory domain model.
'''

from __future__ import annotations

from dataclasses import FrozenInstanceError
from unittest import TestCase, main

from scaralang.core.model.trajectory.waypoint import Waypoint

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class WaypointTest(TestCase):
    '''Unit tests validating Waypoint purity, immutability, and attribute values.'''

    def test_instantiation_and_attributes(self) -> None:
        '''Verify proper initialization and access of Waypoint fields.'''
        point = Waypoint(
            x=100.5,
            y=50.2,
            z=15.0,
            phi=45.0,
            speed=35.0,
            name='P1',
            command='MOVE',
        )
        self.assertEqual(point.x, 100.5)
        self.assertEqual(point.y, 50.2)
        self.assertEqual(point.z, 15.0)
        self.assertEqual(point.phi, 45.0)
        self.assertEqual(point.speed, 35.0)
        self.assertEqual(point.name, 'P1')
        self.assertEqual(point.command, 'MOVE')

    def test_frozen_immutability(self) -> None:
        '''Verify that modifying attributes on Waypoint raises FrozenInstanceError.'''
        point = Waypoint(
            x=10.0,
            y=20.0,
            z=30.0,
            phi=0.0,
            speed=50.0,
            name='A',
            command='',
        )
        with self.assertRaises(FrozenInstanceError):
            setattr(point, 'x', 99.9)

    def test_equality(self) -> None:
        '''Verify equality comparison between Waypoint instances.'''
        pt1 = Waypoint(
            x=10.0,
            y=20.0,
            z=30.0,
            phi=0.0,
            speed=50.0,
            name='A',
            command='',
        )
        pt2 = Waypoint(
            x=10.0,
            y=20.0,
            z=30.0,
            phi=0.0,
            speed=50.0,
            name='A',
            command='',
        )
        pt3 = Waypoint(
            x=10.0,
            y=20.0,
            z=30.0,
            phi=0.0,
            speed=50.0,
            name='B',
            command='',
        )
        self.assertEqual(pt1, pt2)
        self.assertNotEqual(pt1, pt3)


if __name__ == '__main__':
    main()
