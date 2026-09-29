# -*- coding: UTF-8 -*-

'''
Module
    tool_waypoint_builder.py
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
    Concrete implementation of pneumatic tool waypoint builder.
'''

from __future__ import annotations

from scaralang.core.model.dsl.ast.command_type import ScaraCommandType
from scaralang.core.model.dsl.ast.pneumatic_state import PneumaticState
from scaralang.core.model.dsl.compiler.scara_compiler_context import ScaraCompilerContext
from scaralang.core.model.trajectory.waypoint import Waypoint

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ToolWaypointBuilder:
    '''
        Builds domain waypoints for pneumatic tool actuation (PUMP and VALVE).

        It defines:

            :methods:
                | __init__ - Initializes ToolWaypointBuilder instance.
                | build_waypoint - Builds waypoint for pneumatic tool actuation.
    '''

    def __init__(self) -> None:
        '''
            Initializes ToolWaypointBuilder instance.

            :exceptions: None.
        '''

    def build_waypoint(
        self,
        *,
        context: ScaraCompilerContext,
        tool_type: ScaraCommandType,
        state: PneumaticState,
    ) -> Waypoint:
        '''
            Constructs a Waypoint for pneumatic tool actuation.

            :param context: Mutable compiler execution context.
            :param tool_type: Tool command type (PUMP or VALVE).
            :param state: Pneumatic state (ON or OFF).
            :return: Constructed Waypoint instance.
            :exceptions: None.
        '''
        token: str = 'PUMP' if tool_type == ScaraCommandType.PUMP else 'VALVE'
        is_on: bool = state == PneumaticState.ON
        suffix: str = '#1' if is_on else '#0'
        state_str: str = 'ON' if is_on else 'OFF'

        return Waypoint(
            x=context.current_x,
            y=context.current_y,
            z=context.current_z,
            phi=context.current_phi,
            speed=context.current_speed,
            name=f'{token}_{state_str}',
            command=f'<CMD:{token}{suffix}>',
        )
