# -*- coding: UTF-8 -*-

'''
Module
    iarc_waypoint_builder.py
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
    Interface protocol for building trajectory waypoints along circular arc paths.
'''

from __future__ import annotations

from collections.abc import Sequence
from typing import Protocol, runtime_checkable

from scaralang.core.model.dsl.compiler.scara_compiler_context import ScaraCompilerContext
from scaralang.core.model.trajectory.arc_point import ArcPoint
from scaralang.core.model.trajectory.waypoint import Waypoint

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.6'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IArcWaypointBuilder(Protocol):
    '''
        Structural interface protocol for building domain waypoints from arc points.

        It defines:

            :methods:
                | build_waypoints - Builds interpolated arc coordinates as domain waypoints.
                | get_version - Gets implementation version string.
    '''

    def build_waypoints(
        self,
        *,
        arc_points: Sequence[ArcPoint],
        target_z: float,
        speed: float,
        context: ScaraCompilerContext,
    ) -> tuple[Waypoint, ...]:
        '''
            Builds interpolated arc points as domain waypoints.

            :param arc_points: Sequence of ArcPoint coordinate value objects.
            :param target_z: Target vertical elevation coordinate in mm.
            :param speed: Effective feedrate speed in mm/s.
            :param context: Active compiler context with orientation state.
            :return: Tuple of generated Waypoint instances.
        '''

    def get_version(self) -> str:
        '''
            Gets implementation version string.

            :return: Version string.
        '''
