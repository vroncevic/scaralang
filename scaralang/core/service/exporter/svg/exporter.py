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
from typing import ClassVar

from scaralang.core.model.trajectory.plan.waypoint import Waypoint
from scaralang.core.service.trajectory.plan.iplan import ITrajectoryPlan

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class SvgExporter:
    '''
        Serializes trajectory plan waypoints into an SVG toolpath visualization.

        It defines:

            :attributes:
                | VIEWBOX_SIZE - Width and height dimension of SVG viewBox in pixels.
                | VIEWBOX_CENTER_X - SVG viewBox center X coordinate in pixels.
                | VIEWBOX_CENTER_Y - SVG viewBox center Y coordinate in pixels.
                | SCALE_FACTOR - Coordinate scaling multiplier from mm to pixels.
                | OUTER_ENVELOPE_RADIUS - Outer workspace boundary radius in pixels.
                | INNER_ENVELOPE_RADIUS - Inner workspace boundary radius in pixels.
                | BG_COLOR - Background rectangle hex color code.
                | ENVELOPE_COLOR - Workspace boundary circles hex color code.
                | TOOLPATH_COLOR - Trajectory toolpath stroke hex color code.
            :methods:
                | build_svg_path - Constructs SVG path 'd' attribute from waypoints.
                | export_svg - Serializes ITrajectoryPlan into SVG XML string.
                | get_version - Returns the exporter version string.
    '''

    VIEWBOX_SIZE: ClassVar[int] = 800
    VIEWBOX_CENTER_X: ClassVar[float] = 400.0
    VIEWBOX_CENTER_Y: ClassVar[float] = 400.0
    SCALE_FACTOR: ClassVar[float] = 1.0
    OUTER_ENVELOPE_RADIUS: ClassVar[int] = 350
    INNER_ENVELOPE_RADIUS: ClassVar[int] = 100
    BG_COLOR: ClassVar[str] = '#1e1e2e'
    ENVELOPE_COLOR: ClassVar[str] = '#313244'
    TOOLPATH_COLOR: ClassVar[str] = '#89b4fa'

    def build_svg_path(self, *, waypoints: Sequence[Waypoint]) -> str:
        '''
            Constructs SVG path data attribute from motion waypoints.

            :param waypoints: Sequence of trajectory Waypoint instances.
            :return: SVG path 'd' attribute string.
            :exceptions: None.
        '''
        if not waypoints:
            return ''

        # Map robot XY (mm) to SVG viewBox coordinates with center offset
        cx: float = self.VIEWBOX_CENTER_X
        cy: float = self.VIEWBOX_CENTER_Y
        scale: float = self.SCALE_FACTOR

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
            f'<svg xmlns="http://www.w3.org/2000/svg" '
            f'viewBox="0 0 {self.VIEWBOX_SIZE} {self.VIEWBOX_SIZE}" '
            f'width="{self.VIEWBOX_SIZE}" height="{self.VIEWBOX_SIZE}">',
            '  <!-- SCARA Workspace Background -->',
            f'  <rect width="{self.VIEWBOX_SIZE}" height="{self.VIEWBOX_SIZE}" fill="{self.BG_COLOR}" />',
            '  <!-- Reachable Workspace Envelope Reference -->',
            f'  <circle cx="{int(self.VIEWBOX_CENTER_X)}" cy="{int(self.VIEWBOX_CENTER_Y)}" '
            f'r="{self.OUTER_ENVELOPE_RADIUS}" fill="none" '
            f'stroke="{self.ENVELOPE_COLOR}" stroke-width="2" />',
            f'  <circle cx="{int(self.VIEWBOX_CENTER_X)}" cy="{int(self.VIEWBOX_CENTER_Y)}" '
            f'r="{self.INNER_ENVELOPE_RADIUS}" fill="none" '
            f'stroke="{self.ENVELOPE_COLOR}" stroke-width="2" stroke-dasharray="5,5" />',
            '  <!-- Trajectory Toolpath -->',
            f'  <path d="{path_d}" fill="none" stroke="{self.TOOLPATH_COLOR}" '
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
