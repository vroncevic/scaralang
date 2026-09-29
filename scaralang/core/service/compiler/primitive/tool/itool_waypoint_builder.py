# -*- coding: UTF-8 -*-

'''
Module
    itool_waypoint_builder.py
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
    Defines structural runtime-checkable protocol IToolWaypointBuilder for pneumatic waypoints.
'''

from __future__ import annotations

from typing import Protocol
from typing import runtime_checkable

from scaralang.core.model.dsl.ast.command_type import ScaraCommandType
from scaralang.core.model.dsl.ast.pneumatic_state import PneumaticState
from scaralang.core.model.dsl.compiler.scara_compiler_context import ScaraCompilerContext
from scaralang.core.model.trajectory.waypoint import Waypoint

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IToolWaypointBuilder(Protocol):
    '''
        Structural protocol defining contracts for pneumatic tool waypoint construction.

        It defines:

            :methods:
                | build_waypoint - Builds waypoint for pneumatic tool actuation.
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
        '''
