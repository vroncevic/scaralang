# -*- coding: UTF-8 -*-

'''
Module
    ijson_trajectory_exporter.py
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
    Defines IJsonTrajectoryExporter Protocol for exporting trajectory plans to JSON format.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from scaralang.core.model.trajectory.waypoint import Waypoint
from scaralang.core.service.trajectory.plan.itrajectory_plan import ITrajectoryPlan

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.5'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IJsonTrajectoryExporter(Protocol):
    '''
        Structural protocol defining contracts for JSON trajectory export.

        It defines:

            :methods:
                | export_json - Serializes ITrajectoryPlan into structured JSON text.
                | serialize_waypoint - Converts a Waypoint into a dictionary representation.
    '''

    def export_json(self, *, plan: ITrajectoryPlan) -> str:
        '''
            Serializes trajectory plan into structured JSON string.

            :param plan: Validated ITrajectoryPlan protocol instance.
            :return: Formatted JSON string.
        '''

    def serialize_waypoint(
        self, *, index: int, waypoint: Waypoint
    ) -> dict[str, object]:
        '''
            Serializes a single trajectory waypoint into a JSON-compatible dictionary.

            :param index: Zero-based waypoint sequence index.
            :param waypoint: Trajectory Waypoint instance.
            :return: Dictionary representation of waypoint.
        '''
