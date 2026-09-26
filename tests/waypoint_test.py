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
    Unit tests for Waypoint value object model.
'''

from __future__ import annotations

from os.path import abspath, dirname
from sys import path
from unittest import TestCase, main

pkg_dir = dirname(dirname(abspath(__file__)))
if pkg_dir not in path:
    path.insert(0, pkg_dir)

from scaralang.core.model.trajectory.waypoint import Waypoint

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestWaypoint(TestCase):
    '''
        Test cases for Waypoint data class.

        It defines:

            :methods:
                | test_waypoint_creation - Tests instantiation and property access of Waypoint.
                | test_waypoint_equality - Tests equality and string representation.
                | test_waypoint_properties - Tests properties including phi and command.
    '''

    def test_waypoint_creation(self) -> None:
        '''
            Tests instantiation and default values of Waypoint.

            :exceptions: None.
        '''
        pt = Waypoint(
            x=100.5,
            y=50.2,
            z=15.0,
            phi=45.0,
            speed=35.0,
            name='P1',
            command=''
        )
        self.assertEqual(pt.x, 100.5)
        self.assertEqual(pt.y, 50.2)
        self.assertEqual(pt.z, 15.0)
        self.assertEqual(pt.phi, 45.0)
        self.assertEqual(pt.speed, 35.0)
        self.assertEqual(pt.name, 'P1')
        self.assertEqual(pt.command, '')

    def test_waypoint_equality(self) -> None:
        '''
            Tests equality comparison between Waypoint instances.

            :exceptions: None.
        '''
        pt1 = Waypoint(x=10.0, y=20.0, z=30.0, phi=0.0, speed=50.0, name='A', command='')
        pt2 = Waypoint(x=10.0, y=20.0, z=30.0, phi=0.0, speed=50.0, name='A', command='')
        pt3 = Waypoint(x=10.0, y=20.0, z=30.0, phi=0.0, speed=50.0, name='B', command='')
        self.assertEqual(pt1, pt2)
        self.assertNotEqual(pt1, pt3)

    def test_waypoint_properties(self) -> None:
        '''
            Tests waypoint command and phi attributes.
        '''
        pt = Waypoint(
            x=120.0,
            y=60.0,
            z=10.0,
            phi=90.0,
            speed=20.0,
            name='AUX',
            command='HOME'
        )
        self.assertEqual(pt.command, 'HOME')
        self.assertEqual(pt.phi, 90.0)


if __name__ == '__main__':
    main()
