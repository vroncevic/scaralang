# -*- coding: UTF-8 -*-

'''
Module
    exporter.py
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
    Serializes trajectory plans into standard RS-274 G-code commands.
'''

from __future__ import annotations

from scaralang.core.model.trajectory.waypoint import Waypoint
from scaralang.core.service.trajectory.plan.iplan import ITrajectoryPlan

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.9'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class GcodeExporter:
    '''
        Serializes trajectory plan waypoints into standard RS-274 G-code.

        It defines:

            :methods:
                | format_waypoint_line - Formats single Waypoint into G-code line.
                | export_gcode - Serializes ITrajectoryPlan into G-code string.
                | get_version - Returns the exporter version string.
    '''

    def format_waypoint_line(self, *, waypoint: Waypoint) -> str:
        '''
            Formats a single trajectory waypoint into a G-code line.

            :param waypoint: Trajectory Waypoint instance.
            :return: Formatted G-code instruction string.
            :exceptions: None.
        '''
        gcode_cmd: str = 'G0' if waypoint.speed >= 100.0 else 'G1'
        comment: str = f' ; {waypoint.name}' if waypoint.name else ''

        return (
            f'{gcode_cmd} X{waypoint.x:.3f} Y{waypoint.y:.3f} '
            f'Z{waypoint.z:.3f} F{waypoint.speed * 60.0:.0f}{comment}'
        )

    def export_gcode(self, *, plan: ITrajectoryPlan) -> str:
        '''
            Serializes trajectory plan waypoints into formatted G-code lines.

            :param plan: Validated ITrajectoryPlan protocol instance.
            :return: Formatted G-code string.
            :exceptions: None.
        '''
        lines: list[str] = [
            '; SCARA Trajectory G-code Export',
            '; Coordinate System: Absolute (G90), Millimeters (G21)',
            'G21 ; Set units to millimeters',
            'G90 ; Use absolute coordinates',
            'G92 X0 Y0 Z0 ; Set origin',
        ]

        for wp in plan.waypoints:
            lines.append(self.format_waypoint_line(waypoint=wp))

        lines.extend(['M2 ; End of program', ''])

        return '\n'.join(lines)

    def get_version(self) -> str:
        '''
            Returns the exporter version string.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return __version__
