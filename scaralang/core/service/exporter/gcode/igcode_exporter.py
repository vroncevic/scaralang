# -*- coding: UTF-8 -*-

'''
Module
    igcode_exporter.py
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
    Defines IGCodeExporter Protocol for exporting trajectory plans to RS-274 G-code.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from scaralang.core.model.trajectory.waypoint import Waypoint
from scaralang.core.service.trajectory.plan.itrajectory_plan import ITrajectoryPlan

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.6'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IGCodeExporter(Protocol):
    '''
        Structural protocol defining contracts for G-code trajectory export.

        It defines:

            :methods:
                | export_gcode - Serializes ITrajectoryPlan into standard RS-274 G-code.
                | format_waypoint_line - Formats single Waypoint into G-code instruction.
    '''

    def export_gcode(self, *, plan: ITrajectoryPlan) -> str:
        '''
            Serializes trajectory plan waypoints into formatted G-code lines.

            :param plan: Validated ITrajectoryPlan protocol instance.
            :return: Formatted G-code string.
        '''

    def format_waypoint_line(self, *, waypoint: Waypoint) -> str:
        '''
            Formats a single trajectory waypoint into a G-code line.

            :param waypoint: Trajectory Waypoint instance.
            :return: Formatted G-code instruction string.
        '''
