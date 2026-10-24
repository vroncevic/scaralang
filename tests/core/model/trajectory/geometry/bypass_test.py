# -*- coding: UTF-8 -*-

'''
Module
    bypass_test.py
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
    Unit tests for pure data structure BypassArcGeometry.
'''

from __future__ import annotations

from dataclasses import FrozenInstanceError
from unittest import TestCase, main

from scaralang.core.model.trajectory.geometry.bypass import BypassArcGeometry

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class BypassArcGeometryTest(TestCase):
    '''Unit tests validating BypassArcGeometry initialization and attributes.'''

    def test_instantiation_and_attributes(self) -> None:
        '''
            Verify proper initialization and access of BypassArcGeometry fields.

            :exceptions: None.
        '''
        arc = BypassArcGeometry(
            phi_entry=0.5,
            phi_exit=1.5,
            step_sign=1.0,
            arc_sweep=1.0,
            safe_radius=85.0
        )
        self.assertEqual(arc.phi_entry, 0.5)
        self.assertEqual(arc.phi_exit, 1.5)
        self.assertEqual(arc.step_sign, 1.0)
        self.assertEqual(arc.arc_sweep, 1.0)
        self.assertEqual(arc.safe_radius, 85.0)

    def test_immutability(self) -> None:
        '''
            Verify that modifying attributes raises FrozenInstanceError.

            :exceptions: None.
        '''
        arc = BypassArcGeometry(
            phi_entry=0.0,
            phi_exit=1.0,
            step_sign=-1.0,
            arc_sweep=1.0,
            safe_radius=85.0
        )
        with self.assertRaises(FrozenInstanceError):
            setattr(arc, 'safe_radius', 90.0)


if __name__ == '__main__':
    main()
