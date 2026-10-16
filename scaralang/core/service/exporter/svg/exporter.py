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
    Serializes trajectory plans into 2D SVG vector graphic diagrams.
'''

from __future__ import annotations

from collections.abc import Sequence

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


class SvgExporter:
    '''
        Serializes trajectory plan waypoints into an SVG toolpath visualization.

        It defines:

            :methods:
                | build_svg_path - Constructs SVG path 'd' attribute from waypoints.
                | export_svg - Serializes ITrajectoryPlan into SVG XML string.
                | get_version - Returns the exporter version string.
    '''

    def build_svg_path(self, *, waypoints: Sequence[Waypoint]) -> str:
        '''
            Constructs SVG path data attribute from motion waypoints.

            :param waypoints: Sequence of trajectory Waypoint instances.
            :return: SVG path 'd' attribute string.
            :exceptions: None.
        '''
        if not waypoints:
            return ''

        # Map robot XY (mm) to SVG canvas coordinates with offset
        cx, cy = 400.0, 400.0
        scale = 1.0

        commands: list[str] = [
            f'M {cx + waypoints[0].x * scale:.1f} {cy - waypoints[0].y * scale:.1f}'
        ]

        for wp in waypoints[1:]:
            commands.append(
                f'L {cx + wp.x * scale:.1f} {cy - wp.y * scale:.1f}'
            )

        return ' '.join(commands)

    def export_svg(self, *, plan: ITrajectoryPlan) -> str:
        '''
            Serializes trajectory plan into 2D vector graphic SVG string.

            :param plan: Validated ITrajectoryPlan protocol instance.
            :return: Formatted SVG XML string.
            :exceptions: None.
        '''
        path_d: str = self.build_svg_path(waypoints=plan.waypoints)

        lines: list[str] = [
            '<?xml version="1.0" encoding="UTF-8"?>',
            '<svg xmlns="http://www.w3.org/2000/svg" '
            'viewBox="0 0 800 800" width="800" height="800">',
            '  <!-- SCARA Workspace Background -->',
            '  <rect width="800" height="800" fill="#1e1e2e" />',
            '  <!-- Reachable Workspace Envelope Reference -->',
            '  <circle cx="400" cy="400" r="350" fill="none" '
            'stroke="#313244" stroke-width="2" />',
            '  <circle cx="400" cy="400" r="100" fill="none" '
            'stroke="#313244" stroke-width="2" stroke-dasharray="5,5" />',
            '  <!-- Trajectory Toolpath -->',
            f'  <path d="{path_d}" fill="none" stroke="#89b4fa" '
            'stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" />',
            '</svg>\n',
        ]

        return '\n'.join(lines)

    def get_version(self) -> str:
        '''
            Returns the exporter version string.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return __version__
