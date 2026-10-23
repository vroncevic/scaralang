# -*- coding: UTF-8 -*-

'''
Module
    transformer.py
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
    Implementation of coordinate transformations for planar work frames.
'''

from __future__ import annotations

from math import cos, radians, sin
from typing import ClassVar

from scaralang.core.model.dsl.macro.frame import WorkFrame
from scaralang.core.model.kinematics.pose.point_3d import Point3D

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class FrameTransformer:
    '''
        Service calculating 3D coordinate rotations and offsets for work frames.

        It defines:

            :attributes:
                | _FLOAT_ZERO - Floating-point zero constant.
            :methods:
                | transform_point - Transforms local frame coordinates into global base coordinates.
                | inverse_transform_point - Transforms global coordinates into local frame coordinates.
                | get_version - Returns the transformer version string.
    '''

    _FLOAT_ZERO: ClassVar[float] = 0.0

    def transform_point(
        self,
        *,
        frame: WorkFrame,
        point: Point3D,
    ) -> Point3D:
        '''
            Transforms 3D point from local work frame to global base coordinate system.

            :param frame: WorkFrame instance defining offset and rotation.
            :param point: Local coordinate Point3D in millimeters.
            :return: Transformed global coordinate Point3D.
        '''
        if (
            frame.origin.x == self._FLOAT_ZERO
            and frame.origin.y == self._FLOAT_ZERO
            and frame.origin.z == self._FLOAT_ZERO
            and frame.angle_deg == self._FLOAT_ZERO
        ):
            return point

        rad = radians(frame.angle_deg)
        cos_a = cos(rad)
        sin_a = sin(rad)
        gx = frame.origin.x + (point.x * cos_a - point.y * sin_a)
        gy = frame.origin.y + (point.x * sin_a + point.y * cos_a)
        gz = frame.origin.z + point.z

        return Point3D(x=gx, y=gy, z=gz)

    def inverse_transform_point(
        self,
        *,
        frame: WorkFrame,
        point: Point3D,
    ) -> Point3D:
        '''
            Transforms 3D point from global base coordinate system to local work frame.

            :param frame: WorkFrame instance defining offset and rotation.
            :param point: Global coordinate Point3D in millimeters.
            :return: Transformed local coordinate Point3D.
        '''
        if (
            frame.origin.x == self._FLOAT_ZERO
            and frame.origin.y == self._FLOAT_ZERO
            and frame.origin.z == self._FLOAT_ZERO
            and frame.angle_deg == self._FLOAT_ZERO
        ):
            return point

        dx = point.x - frame.origin.x
        dy = point.y - frame.origin.y
        dz = point.z - frame.origin.z
        rad = radians(frame.angle_deg)
        cos_a = cos(rad)
        sin_a = sin(rad)
        lx = dx * cos_a + dy * sin_a
        ly = -dx * sin_a + dy * cos_a
        lz = dz

        return Point3D(x=lx, y=ly, z=lz)

    def get_version(self) -> str:
        '''
            Returns the transformer version string.

            :return: Version string representation.
            :exceptions: None.
        '''
        return __version__
