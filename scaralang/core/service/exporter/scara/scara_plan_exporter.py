# -*- coding: UTF-8 -*-

'''
Module
    scara_plan_exporter.py
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
    Implementation of trajectory plan exporter converting waypoints into SCARA DSL code.
'''

from __future__ import annotations

from scaralang.core.model.trajectory.waypoint import Waypoint
from scaralang.core.service.trajectory.plan.itrajectory_read_only import ITrajectoryReadOnly

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ScaraPlanExporter:
    '''
        Exports active TrajectoryPlan waypoints into clean, readable SCARA DSL source text.

        It defines:

            :methods:
                | export_plan - Serializes trajectory plan into formatted .scara source code.
                | format_waypoint - Formats trajectory waypoint into SCARA move instruction.
    '''

    def format_waypoint(
        self, *, waypoint: Waypoint, is_initial: bool = False
    ) -> str:
        '''
            Formats a single trajectory waypoint into a SCARA DSL move instruction.

            :param waypoint: Trajectory Waypoint instance.
            :param is_initial: True if generating the initial joint move, False for linear.
            :return: Formatted SCARA DSL instruction line.
            :exceptions: None.
        '''
        comment = f'  # {waypoint.name}' if waypoint.name else ''

        if is_initial:
            return (
                f'MOVE_J X={waypoint.x:.2f} Y={waypoint.y:.2f} '
                f'Z={waypoint.z:.2f} PHI={waypoint.phi:.2f}{comment}'
            )

        return (
            f'MOVE_L X={waypoint.x:.2f} Y={waypoint.y:.2f} '
            f'Z={waypoint.z:.2f} PHI={waypoint.phi:.2f} '
            f'SPEED={waypoint.speed:.1f}{comment}'
        )

    def export_plan(self, *, plan: ITrajectoryReadOnly) -> str:
        '''
            Serializes trajectory plan into formatted .scara source code.

            :param plan: Trajectory plan instance.
            :return: Formatted SCARA DSL script.
            :exceptions: None.
        '''
        waypoints: tuple[Waypoint, ...] = plan.waypoints

        if not waypoints:
            return '# SCARAjectory DSL Program\n# Empty trajectory plan\n'

        lines: list[str] = [
            '# ==========================================================',
            '# SCARAjectory DSL Program',
            f'# Generated with {len(waypoints)} waypoints',
            '# ==========================================================',
            'CONFIG ELBOW RIGHT',
            'SPEED RAPID 100.0',
            f'SPEED WORK {waypoints[0].speed:.1f}',
            'ACCEL 500.0',
            'ZONE FINE',
            '',
        ]

        lines.append(
            self.format_waypoint(waypoint=waypoints[0], is_initial=True)
        )

        for pt in waypoints[1:]:
            lines.append(self.format_waypoint(waypoint=pt, is_initial=False))

        lines.append('')

        return '\n'.join(lines)
