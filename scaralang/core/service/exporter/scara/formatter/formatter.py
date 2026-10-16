# -*- coding: UTF-8 -*-

'''
Module
    formatter.py
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
    Formats trajectory waypoints into SCARA DSL instruction statements.
'''

from __future__ import annotations

from scaralang.core.model.dsl.ast.command_type import ScaraCommandType
from scaralang.core.model.dsl.ast.instruction_param import ScaraInstructionParam
from scaralang.core.model.dsl.ast.pneumatic_state import PneumaticState
from scaralang.core.model.trajectory.waypoint import Waypoint

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.9'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ScaraWaypointFormatter:
    '''
        Formats trajectory waypoints into clean SCARA DSL instructions.

        It defines:

            :methods:
                | format_waypoint - Formats waypoint into motion or command line.
                | format_command - Formats non-motion command waypoint into DSL statement.
                | format_motion - Formats motion waypoint into joint or linear move.
                | get_version - Returns formatter version string.
    '''

    def format_command(self, *, waypoint: Waypoint) -> str:
        '''
            Formats a non-motion command waypoint into a SCARA DSL command statement.

            :param waypoint: Trajectory Waypoint instance with command set.
            :return: Formatted SCARA DSL command line.
            :exceptions: None.
        '''
        clean: str = waypoint.command.strip()
        normalized: str = clean.strip('<>').removeprefix('CMD:')
        parts: tuple[str, ...] = tuple(normalized.replace('#', ' ').split())
        cmd_name: str = parts[0] if parts else ''
        arg: str = parts[1] if len(parts) > 1 else ''
        comment: str = (
            f'  # {waypoint.name}'
            if waypoint.name
            and waypoint.name not in (
                cmd_name,
                f'{cmd_name}_{arg}',
                f'{cmd_name}_ON',
                f'{cmd_name}_OFF',
                f'{cmd_name}_{arg}MS',
            )
            else ''
        )
        match cmd_name:
            case ScaraCommandType.PUMP:
                state: str = (
                    PneumaticState.ON.value
                    if arg in ('1', PneumaticState.ON.value)
                    else PneumaticState.OFF.value
                )
                return f'{ScaraCommandType.PUMP.value} {state}{comment}'

            case ScaraCommandType.VALVE:
                state = (
                    PneumaticState.ON.value
                    if arg in ('1', PneumaticState.ON.value)
                    else PneumaticState.OFF.value
                )
                return f'{ScaraCommandType.VALVE.value} {state}{comment}'

            case ScaraCommandType.WAIT | ScaraCommandType.WAIT_MS:
                return f'{ScaraCommandType.WAIT.value} {arg}{comment}'

            case ScaraCommandType.CONFIG_MOTOR:
                return f'{ScaraCommandType.CONFIG.value} MOTOR {arg}{comment}'

            case (
                ScaraCommandType.HOME
                | ScaraCommandType.HOLD
                | ScaraCommandType.RESUME
                | ScaraCommandType.ESTOP
                | ScaraCommandType.ENABLE
                | ScaraCommandType.DISABLE
            ):
                return f'{cmd_name}{comment}'

            case _:
                return f'{clean}{comment}'

    def format_motion(self, *, waypoint: Waypoint, is_joint: bool) -> str:
        '''
            Formats a trajectory waypoint into a SCARA DSL motion instruction.

            :param waypoint: Trajectory Waypoint instance.
            :param is_joint: True for MOVE_J, False for MOVE_L.
            :return: Formatted SCARA DSL motion line.
            :exceptions: None.
        '''
        comment: str = f'  # {waypoint.name}' if waypoint.name else ''

        if is_joint:
            return (
                f'{ScaraCommandType.MOVE_J.value} '
                f'{ScaraInstructionParam.X.value}={waypoint.x:.2f} '
                f'{ScaraInstructionParam.Y.value}={waypoint.y:.2f} '
                f'{ScaraInstructionParam.Z.value}={waypoint.z:.2f} '
                f'{ScaraInstructionParam.PHI.value}={waypoint.phi:.2f}'
                f'{comment}'
            )

        return (
            f'{ScaraCommandType.MOVE_L.value} '
            f'{ScaraInstructionParam.X.value}={waypoint.x:.2f} '
            f'{ScaraInstructionParam.Y.value}={waypoint.y:.2f} '
            f'{ScaraInstructionParam.Z.value}={waypoint.z:.2f} '
            f'{ScaraInstructionParam.PHI.value}={waypoint.phi:.2f} '
            f'{ScaraInstructionParam.SPEED.value}={waypoint.speed:.1f}'
            f'{comment}'
        )

    def format_waypoint(
        self, *, waypoint: Waypoint, is_initial: bool = False
    ) -> str:
        '''
            Formats a single trajectory waypoint into a SCARA DSL instruction line.

            :param waypoint: Trajectory Waypoint instance.
            :param is_initial: True for initial joint move, False for linear.
            :return: Formatted SCARA DSL instruction line.
            :exceptions: None.
        '''
        if waypoint.command:
            return self.format_command(waypoint=waypoint)

        return self.format_motion(waypoint=waypoint, is_joint=is_initial)

    def get_version(self) -> str:
        '''
            Returns the formatter version string.

            :return: Semantic version string representation.
            :exceptions: None.
        '''
        return __version__
