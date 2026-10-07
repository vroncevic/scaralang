# -*- coding: UTF-8 -*-

'''
Module
    bottleneck_incident_test.py
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
    Unit tests for BottleneckIncident data model.
'''

from __future__ import annotations

from unittest import TestCase, main

from scaralang.core.model.trajectory.bottleneck_incident import BottleneckIncident

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.7'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class BottleneckIncidentTest(TestCase):
    '''Unit tests validating BottleneckIncident dataclass instantiation and fields.'''

    def test_instantiation_and_attributes(self) -> None:
        '''Verify correct field assignment upon instantiation.'''
        incident = BottleneckIncident(
            step_index=4,
            limiting_axis='Z',
            constraint_type='VELOCITY',
            duration_us=250000
        )
        self.assertEqual(incident.step_index, 4)
        self.assertEqual(incident.limiting_axis, 'Z')
        self.assertEqual(incident.constraint_type, 'VELOCITY')
        self.assertEqual(incident.duration_us, 250000)

    def test_immutability(self) -> None:
        '''Verify that attributes cannot be modified on frozen dataclass.'''
        incident = BottleneckIncident(
            step_index=1,
            limiting_axis='J1',
            constraint_type='ACCELERATION',
            duration_us=100000
        )
        with self.assertRaises(AttributeError):
            incident.limiting_axis = 'J2'  # type: ignore[misc]


if __name__ == '__main__':
    main()
