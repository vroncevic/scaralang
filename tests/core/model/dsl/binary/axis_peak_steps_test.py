# -*- coding: UTF-8 -*-

'''
Module
    axis_peak_steps_test.py
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
    Unit tests for AxisPeakSteps model.
'''

from __future__ import annotations

from dataclasses import FrozenInstanceError
from unittest import TestCase, main

from scaralang.core.model.dsl.binary.axis_peak_steps import AxisPeakSteps

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.6'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class AxisPeakStepsTest(TestCase):
    '''Unit tests validating AxisPeakSteps purity, defaults, and immutability.'''

    def test_default_values(self) -> None:
        '''Verify AxisPeakSteps default initialization.'''
        steps = AxisPeakSteps()
        self.assertEqual(steps.peak_j1_steps, 0)
        self.assertEqual(steps.peak_j2_steps, 0)
        self.assertEqual(steps.peak_z_steps, 0)
        self.assertEqual(steps.peak_j4_steps, 0)

    def test_custom_values(self) -> None:
        '''Verify AxisPeakSteps custom initialization.'''
        steps = AxisPeakSteps(
            peak_j1_steps=1200,
            peak_j2_steps=800,
            peak_z_steps=100,
            peak_j4_steps=50,
        )
        self.assertEqual(steps.peak_j1_steps, 1200)
        self.assertEqual(steps.peak_j2_steps, 800)
        self.assertEqual(steps.peak_z_steps, 100)
        self.assertEqual(steps.peak_j4_steps, 50)

    def test_immutability(self) -> None:
        '''Verify that modifying attributes raises FrozenInstanceError.'''
        steps = AxisPeakSteps()
        with self.assertRaises(FrozenInstanceError):
            setattr(steps, 'peak_j1_steps', 500)


if __name__ == '__main__':
    main()
