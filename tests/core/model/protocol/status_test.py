# -*- coding: UTF-8 -*-

'''
Module
    status_test.py
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
    Unit tests for ManipulatorStatus protocol model.
'''

from __future__ import annotations

from dataclasses import FrozenInstanceError
from unittest import TestCase, main

from scaralang.core.model.protocol.status import ManipulatorStatus

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ManipulatorStatusTest(TestCase):
    '''
        Unit tests validating ManipulatorStatus dataclass fields, immutability, and equality.
    '''

    def test_instantiation_and_attributes(self) -> None:
        '''
            Verify that ManipulatorStatus correctly stores all telemetry fields.

            :exceptions: None.
        '''
        status = ManipulatorStatus(
            system_state=1,
            is_busy=True,
            queue_count=4,
            j1_steps=100,
            j2_steps=200,
            z_steps=300,
            j4_steps=400,
        )
        self.assertEqual(status.system_state, 1)
        self.assertTrue(status.is_busy)
        self.assertEqual(status.queue_count, 4)
        self.assertEqual(status.j1_steps, 100)
        self.assertEqual(status.j2_steps, 200)
        self.assertEqual(status.z_steps, 300)
        self.assertEqual(status.j4_steps, 400)

    def test_immutability(self) -> None:
        '''
            Verify that ManipulatorStatus is frozen and raises FrozenInstanceError on modification.

            :exceptions: None.
        '''
        status = ManipulatorStatus(
            system_state=0,
            is_busy=False,
            queue_count=0,
            j1_steps=0,
            j2_steps=0,
            z_steps=0,
            j4_steps=0,
        )
        with self.assertRaises(FrozenInstanceError):
            status.is_busy = True

    def test_equality(self) -> None:
        '''
            Verify value equality between two ManipulatorStatus instances.

            :exceptions: None.
        '''
        status_one = ManipulatorStatus(
            system_state=0,
            is_busy=False,
            queue_count=2,
            j1_steps=10,
            j2_steps=20,
            z_steps=30,
            j4_steps=40,
        )
        status_two = ManipulatorStatus(
            system_state=0,
            is_busy=False,
            queue_count=2,
            j1_steps=10,
            j2_steps=20,
            z_steps=30,
            j4_steps=40,
        )
        self.assertEqual(status_one, status_two)


if __name__ == '__main__':
    main()
