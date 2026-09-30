# -*- coding: UTF-8 -*-

'''
Module
    control_waypoint_descriptor_test.py
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
    Unit tests for pure data model ControlWaypointDescriptor.
'''

from __future__ import annotations

from dataclasses import FrozenInstanceError
from unittest import TestCase, main

from scaralang.core.model.dsl.compiler.control_waypoint_descriptor import ControlWaypointDescriptor

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestControlWaypointDescriptor(TestCase):
    '''Unit tests validating ControlWaypointDescriptor initialization and immutability.'''

    def test_instantiation(self) -> None:
        '''Verify field values on initialization.'''
        desc = ControlWaypointDescriptor(
            name='HOME',
            command='<CMD:HOME>',
            phi=0.0,
            speed=150.0,
        )
        self.assertEqual(desc.name, 'HOME')
        self.assertEqual(desc.command, '<CMD:HOME>')
        self.assertEqual(desc.phi, 0.0)
        self.assertEqual(desc.speed, 150.0)

    def test_immutability(self) -> None:
        '''Verify frozen dataclass prevents mutation.'''
        desc = ControlWaypointDescriptor(
            name='WAIT_100MS',
            command='<CMD:WAIT#100>',
            phi=45.0,
            speed=40.0,
        )
        with self.assertRaises(FrozenInstanceError):
            desc.name = 'OTHER'

    def test_equality(self) -> None:
        '''Verify value-object equality semantics.'''
        d1 = ControlWaypointDescriptor(name='A', command='<CMD:A>', phi=0.0, speed=10.0)
        d2 = ControlWaypointDescriptor(name='A', command='<CMD:A>', phi=0.0, speed=10.0)
        d3 = ControlWaypointDescriptor(name='B', command='<CMD:B>', phi=0.0, speed=10.0)
        self.assertEqual(d1, d2)
        self.assertNotEqual(d1, d3)


if __name__ == '__main__':
    main()
