# -*- coding: UTF-8 -*-

'''
Module
    axis_peak_metric_test.py
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
    Unit tests for AxisPeakMetric data model.
'''

from __future__ import annotations

from dataclasses import FrozenInstanceError
from unittest import TestCase
from unittest import main

from scaralang.core.model.trajectory.axis_peak_metric import AxisPeakMetric

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.7'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class AxisPeakMetricTest(TestCase):
    '''Unit tests validating AxisPeakMetric dataclass instantiation and immutability.'''

    def test_instantiation_and_attributes(self) -> None:
        '''Verify correct field assignment upon instantiation.'''
        metric = AxisPeakMetric(
            axis_name='J1',
            peak_velocity=3.14,
            peak_acceleration=12.56,
            peak_steps=3200
        )
        self.assertEqual(metric.axis_name, 'J1')
        self.assertEqual(metric.peak_velocity, 3.14)
        self.assertEqual(metric.peak_acceleration, 12.56)
        self.assertEqual(metric.peak_steps, 3200)

    def test_immutability(self) -> None:
        '''Verify that attributes cannot be modified on frozen dataclass.'''
        metric = AxisPeakMetric(
            axis_name='Z',
            peak_velocity=50.0,
            peak_acceleration=200.0,
            peak_steps=800
        )
        with self.assertRaises(FrozenInstanceError):
            metric.peak_velocity = 60.0  # type: ignore[misc]


if __name__ == '__main__':
    main()
