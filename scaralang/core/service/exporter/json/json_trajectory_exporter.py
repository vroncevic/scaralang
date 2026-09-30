# -*- coding: UTF-8 -*-

'''
Module
    json_trajectory_exporter.py
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
    Serializes trajectory plans into structured JSON telemetry datasets.
'''

from __future__ import annotations

from json import dumps

from scaralang.core.model.trajectory.waypoint import Waypoint
from scaralang.core.service.trajectory.plan.itrajectory_plan import ITrajectoryPlan

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class JsonTrajectoryExporter:
    '''
        Serializes trajectory plan into structured JSON telemetry data.

        It defines:

            :methods:
                | export_json - Serializes ITrajectoryPlan into JSON string.
                | serialize_waypoint - Converts a Waypoint into a dictionary representation.
    '''

    def serialize_waypoint(
        self, *, index: int, waypoint: Waypoint
    ) -> dict[str, object]:
        '''
            Serializes a single trajectory waypoint into a JSON-compatible dictionary.

            :param index: Zero-based waypoint sequence index.
            :param waypoint: Trajectory Waypoint instance.
            :return: Dictionary representation of waypoint.
            :exceptions: None.
        '''
        return {
            'index': index,
            'name': waypoint.name,
            'x': waypoint.x,
            'y': waypoint.y,
            'z': waypoint.z,
            'phi': waypoint.phi,
            'speed': waypoint.speed,
            'command': waypoint.command,
        }

    def export_json(self, *, plan: ITrajectoryPlan) -> str:
        '''
            Serializes trajectory plan into structured JSON string.

            :param plan: Validated ITrajectoryPlan protocol instance.
            :return: Formatted JSON string.
            :exceptions: None.
        '''
        data: dict[str, object] = {
            'waypoint_count': len(plan.waypoints),
            'waypoints': [
                self.serialize_waypoint(index=idx, waypoint=wp)
                for idx, wp in enumerate(plan.waypoints)
            ],
        }

        return dumps(data, indent=2) + '\n'
