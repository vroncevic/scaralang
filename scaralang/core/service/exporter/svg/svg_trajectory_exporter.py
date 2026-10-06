# -*- coding: UTF-8 -*-

'''
Module
    svg_trajectory_exporter.py
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
    Serializes trajectory plans into 2D SVG vector graphic toolpath diagrams.
'''

from __future__ import annotations

from collections.abc import Sequence

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


class SvgTrajectoryExporter:
    '''
        Serializes trajectory plans into SVG vector diagrams showing 2D Cartesian toolpaths.

        It defines:

            :methods:
                | build_svg_path - Constructs SVG path 'd' attribute from waypoints.
                | export_svg - Serializes ITrajectoryPlan into SVG document string.
    '''

    def build_svg_path(self, *, waypoints: Sequence[Waypoint]) -> str:
        '''
            Constructs SVG path data attribute from motion waypoints.

            :param waypoints: Sequence of trajectory Waypoint instances.
            :return: SVG path 'd' attribute string.
            :exceptions: None.
        '''
        path_segments: list[str] = []
        is_first: bool = True

        for wp in waypoints:
            if not wp.command:
                prefix = 'M' if is_first else 'L'
                path_segments.append(f'{prefix} {wp.x:.2f} {wp.y:.2f}')
                is_first = False

        return ' '.join(path_segments)

    def export_svg(self, *, plan: ITrajectoryPlan) -> str:
        '''
            Serializes trajectory plan into 2D vector graphic SVG string.

            :param plan: Validated ITrajectoryPlan protocol instance.
            :return: Formatted SVG XML string.
            :exceptions: None.
        '''
        path_d: str = self.build_svg_path(waypoints=plan.waypoints)

        return (
            '<svg xmlns="http://www.w3.org/2000/svg" '
            'viewBox="-300 -300 600 600" width="600" height="600">\n'
            '  <rect x="-300" y="-300" width="600" height="600" fill="#1e1e2e"/>\n'
            '  <circle cx="0" cy="0" r="300" fill="none" stroke="#45475a" stroke-dasharray="4"/>\n'
            f'  <path d="{path_d}" fill="none" stroke="#89b4fa" stroke-width="2"/>\n'
            '</svg>\n'
        )
