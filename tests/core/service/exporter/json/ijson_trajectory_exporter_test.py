# -*- coding: UTF-8 -*-

'''
Module
    ijson_trajectory_exporter_test.py
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
    Unit tests for IJsonTrajectoryExporter protocol contract.
'''

from __future__ import annotations

from unittest import TestCase, main

from scaralang.core.model.trajectory.waypoint import Waypoint
from scaralang.core.service.exporter.json.ijson_trajectory_exporter import IJsonTrajectoryExporter
from scaralang.core.service.trajectory.plan.itrajectory_plan import ITrajectoryPlan

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DummyJsonExporter:
    '''Dummy exporter for protocol runtime check verification.'''

    def export_json(self, *, plan: ITrajectoryPlan) -> str:
        '''Dummy export_json implementation.'''
        _ = plan
        return '{}'

    def serialize_waypoint(
        self, *, index: int, waypoint: Waypoint
    ) -> dict[str, object]:
        '''Dummy serialize_waypoint implementation.'''
        _ = (index, waypoint)
        return {'index': index}


class TestIJsonTrajectoryExporter(TestCase):
    '''
        Test cases verifying IJsonTrajectoryExporter protocol contract.

        It defines:

            :methods:
                | test_protocol_conformance - Verifies dummy class satisfies protocol.
                | test_protocol_methods - Verifies dummy exporter methods can be called.
    '''

    def test_protocol_conformance(self) -> None:
        '''Verifies structural typing conformance without inheritance.'''
        exporter = DummyJsonExporter()
        self.assertIsInstance(exporter, IJsonTrajectoryExporter)

    def test_protocol_methods(self) -> None:
        '''Verifies protocol methods return expected types.'''
        exporter: IJsonTrajectoryExporter = DummyJsonExporter()
        wp = Waypoint(x=0.0, y=0.0, z=0.0, speed=10.0)
        self.assertEqual(
            exporter.serialize_waypoint(index=0, waypoint=wp), {'index': 0}
        )


if __name__ == '__main__':
    main()
