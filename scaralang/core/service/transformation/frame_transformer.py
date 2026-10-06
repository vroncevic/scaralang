# -*- coding: UTF-8 -*-

'''
Module
    frame_transformer.py
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
    Implementation of IFrameTransformer calculating coordinate transformations for work frames.
'''

from __future__ import annotations

from math import cos, radians, sin

from scaralang.core.model.dsl.macro.work_frame import WorkFrame
from scaralang.core.model.kinematics.point_2d import Point2D

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.6'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class FrameTransformer:
    '''
        Service calculating 2D coordinate rotations and offsets for planar work frames.

        It defines:

            :attributes:
                | None.
            :methods:
                | transform_point - Transforms local frame coordinates into global base coordinates.
                | get_version - Returns the transformer version string.
    '''

    def transform_point(
        self,
        *,
        frame: WorkFrame,
        point: Point2D,
    ) -> Point2D:
        '''
            Transforms point from local work frame to global base coordinate system.

            :param frame: WorkFrame instance defining offset and rotation.
            :param point: Local coordinate Point2D in millimeters.
            :return: Transformed global coordinate Point2D.
        '''
        if (
            frame.origin.x == 0.0
            and frame.origin.y == 0.0
            and frame.angle_deg == 0.0
        ):
            return point

        rad = radians(frame.angle_deg)
        cos_a = cos(rad)
        sin_a = sin(rad)
        gx = frame.origin.x + (point.x * cos_a - point.y * sin_a)
        gy = frame.origin.y + (point.x * sin_a + point.y * cos_a)

        return Point2D(x=gx, y=gy)

    def get_version(self) -> str:
        '''
            Returns the transformer version string.

            :return: Version string representation.
            :exceptions: None.
        '''
        return __version__
