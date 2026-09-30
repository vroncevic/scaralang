# -*- coding: UTF-8 -*-

'''
Module
    control_waypoint_builder.py
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
    Concrete implementation of control command waypoint builder.
'''

from __future__ import annotations

from scaralang.core.model.dsl.compiler.control_waypoint_descriptor import ControlWaypointDescriptor
from scaralang.core.model.dsl.compiler.scara_compiler_context import ScaraCompilerContext
from scaralang.core.model.trajectory.waypoint import Waypoint

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ControlWaypointBuilder:
    '''
        Builds domain waypoints for workflow and machine execution control commands.

        It defines:

            :methods:
                | __init__ - Initializes ControlWaypointBuilder instance.
                | build_waypoint - Builds waypoint for execution control commands.
    '''

    def __init__(self) -> None:
        '''
            Initializes ControlWaypointBuilder instance.

            :exceptions: None.
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
            :exceptions: None.
        '''
        return Waypoint(
            x=context.current_x,
            y=context.current_y,
            z=context.current_z,
            phi=descriptor.phi,
            speed=descriptor.speed,
            name=descriptor.name,
            command=descriptor.command,
        )
