# -*- coding: UTF-8 -*-

'''
Module
    arc_interpolator.py
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
    Implementation of IArcInterpolator calculating smooth discrete arc segments.
'''

from __future__ import annotations

from math import atan2, ceil, cos, degrees, hypot, pi, radians, sin

from scaralang.core.model.dsl.compiler.arc_geometry import ArcGeometry
from scaralang.core.model.exceptions.scara_kinematics_error import ScaraKinematicsError
from scaralang.core.model.kinematics.point_2d import Point2D
from scaralang.core.model.trajectory.arc_point import ArcPoint

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ArcInterpolator:
    '''
        Mathematical interpolator segmenting circular arcs into linear waypoints.

        It defines:

            :attributes:
                | None.
            :methods:
                | interpolate - Segments circular arc into discrete coordinates and tangent angles.
                | calculate_point - Calculates coordinates and heading angle for given circle angle.
                | get_version - Gets implementation version string.
    '''

    def interpolate(
        self,
        *,
        geometry: ArcGeometry,
    ) -> tuple[ArcPoint, ...]:
        '''
            Segments circular arc into intermediate coordinates and tangent angles.

            :param geometry: ArcGeometry describing arc coordinates and orientation.
            :return: Tuple of ArcPoint instances.
            :exceptions: ScaraKinematicsError if arc radius is zero or less than 1e-4.
        '''
        center = Point2D(
            x=geometry.start.x + geometry.offset.x,
            y=geometry.start.y + geometry.offset.y,
        )
        radius = hypot(geometry.offset.x, geometry.offset.y)

        if radius < 1e-4:
            raise ScaraKinematicsError('Arc radius must be greater than zero')

        angle_start = atan2(
            geometry.start.y - center.y, geometry.start.x - center.x
        )
        angle_end = atan2(
            geometry.target.y - center.y, geometry.target.x - center.x
        )

        if geometry.is_clockwise:
            if angle_end >= angle_start:
                angle_end -= 2.0 * pi
        else:
            if angle_end <= angle_start:
                angle_end += 2.0 * pi

        total_sweep = abs(angle_end - angle_start)
        step_rad = radians(max(0.5, geometry.step_angle_deg))
        num_segments = max(4, int(ceil(total_sweep / step_rad)))

        points: list[ArcPoint] = []

        for i in range(1, num_segments + 1):
            cur_angle = angle_start + (i / float(num_segments)) * (angle_end - angle_start)
            points.append(
                self.calculate_point(
                    center=center,
                    radius=radius,
                    angle=cur_angle,
                    is_clockwise=geometry.is_clockwise,
                )
            )

        return tuple(points)

    def calculate_point(
        self,
        *,
        center: Point2D,
        radius: float,
        angle: float,
        is_clockwise: bool,
    ) -> ArcPoint:
        '''
            Calculates 2D Cartesian coordinates and heading angle for given circle angle.

            :param center: Circle center Point2D coordinate.
            :param radius: Circle radius.
            :param angle: Point angular position in radians.
            :param is_clockwise: Arc rotation direction flag.
            :return: ArcPoint instance.
            :exceptions: None.
        '''
        px: float = center.x + radius * cos(angle)
        py: float = center.y + radius * sin(angle)
        tangent_rad: float = angle - (
            pi / 2.0 if is_clockwise else -pi / 2.0
        )
        tangent_deg: float = (degrees(tangent_rad) + 180.0) % 360.0 - 180.0

        return ArcPoint(
            point=Point2D(x=px, y=py),
            heading_deg=tangent_deg,
        )

    def get_version(self) -> str:
        '''
            Gets implementation version string.

            :return: Version string.
            :exceptions: None.
        '''
        return __version__
