# -*- coding: UTF-8 -*-

'''
Module
    igcode_exporter_test.py
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
    Unit tests for IGCodeExporter protocol contract.
'''

from __future__ import annotations

from unittest import TestCase, main

from scaralang.core.model.trajectory.waypoint import Waypoint
from scaralang.core.service.exporter.gcode.igcode_exporter import IGCodeExporter
from scaralang.core.service.trajectory.plan.itrajectory_plan import ITrajectoryPlan

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DummyGCodeExporter:
    '''Dummy exporter for protocol runtime check verification.'''

    def export_gcode(self, *, plan: ITrajectoryPlan) -> str:
        '''Dummy export_gcode implementation.'''
        _ = plan
        return ''

    def format_waypoint_line(self, *, waypoint: Waypoint) -> str:
        '''Dummy format_waypoint_line implementation.'''
        _ = waypoint
        return ''


class TestIGCodeExporter(TestCase):
    '''
        Test cases verifying IGCodeExporter protocol contract.

        It defines:

            :methods:
                | test_protocol_conformance - Verifies dummy class satisfies protocol.
                | test_protocol_methods - Verifies dummy exporter methods can be called.
    '''

    def test_protocol_conformance(self) -> None:
        '''Verifies structural typing conformance without inheritance.'''
        exporter = DummyGCodeExporter()
        self.assertIsInstance(exporter, IGCodeExporter)

    def test_protocol_methods(self) -> None:
        '''Verifies protocol methods return expected types.'''
        exporter: IGCodeExporter = DummyGCodeExporter()
        wp = Waypoint(x=0.0, y=0.0, z=0.0, speed=10.0)
        self.assertEqual(exporter.format_waypoint_line(waypoint=wp), '')


if __name__ == '__main__':
    main()
