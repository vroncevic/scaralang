# -*- coding: UTF-8 -*-

'''
Module
    icontrol_waypoint_builder.py
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
    Defines structural runtime-checkable protocol IControlWaypointBuilder for control waypoints.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from scaralang.core.model.dsl.compiler.control_waypoint_descriptor import ControlWaypointDescriptor
from scaralang.core.model.dsl.compiler.scara_compiler_context import ScaraCompilerContext
from scaralang.core.model.trajectory.waypoint import Waypoint

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IControlWaypointBuilder(Protocol):
    '''
        Structural protocol defining contracts for control command waypoint construction.

        It defines:

            :methods:
                | build_waypoint - Builds waypoint for execution control commands.
                | get_version - Returns the control waypoint builder version string.
    '''

    def build_waypoint(
        self,
        *,
        context: ScaraCompilerContext,
        descriptor: ControlWaypointDescriptor,
    ) -> Waypoint:
        '''
            Builds a control command Waypoint with context coordinates.

            :param context: Mutable compiler execution context.
            :param descriptor: Immutable control waypoint attributes descriptor.
            :return: Instantiated Waypoint.
        '''

    def get_version(self) -> str:
        '''
            Returns the builder version string representation.

            :return: Version string representation.
        '''
