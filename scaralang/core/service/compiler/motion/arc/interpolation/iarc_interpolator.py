# -*- coding: UTF-8 -*-

'''
Module
    iarc_interpolator.py
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
    Defines structural runtime-checkable protocol IArcInterpolator for circular arc segmentation.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from scaralang.core.model.dsl.compiler.arc_geometry import ArcGeometry
from scaralang.core.model.trajectory.arc_point import ArcPoint

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.7'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IArcInterpolator(Protocol):
    '''
        Structural protocol defining contract for circular arc Cartesian segmentation.

        It defines:

            :attributes:
                | None.
            :methods:
                | interpolate - Generates discrete points and tangent angles along circular arc.
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
            :return: Tuple of ArcPoint instances along the arc.
        '''

    def get_version(self) -> str:
        '''
            Gets implementation version string.

            :return: Version string.
        '''
