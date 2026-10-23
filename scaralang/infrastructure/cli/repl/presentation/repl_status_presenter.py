# -*- coding: UTF-8 -*-

'''
Module
    repl_status_presenter.py
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
    Concrete implementation of REPL status, help manual and pose presenter.
'''

from __future__ import annotations

from scaralang.core.model.repl.context import ReplSessionContext

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ReplStatusPresenter:
    '''
        Presenter formatting help manual, session status and Cartesian poses for the REPL.

        It defines:

            :methods:
                | present_help - Returns formatted help text for REPL commands and syntax.
                | present_status - Returns formatted status text for active session state.
                | present_pose - Returns formatted Cartesian pose string.
    '''

    def present_help(self) -> str:
        '''
            Returns formatted help text for REPL commands and syntax.

            :return: Multiline help string.
            :exceptions: None.
        '''
        lines: list[str] = [
            'Built-in REPL Commands:',
            '  help, ?        - Show this reference manual',
            '  status, state  - Display current kinematic and tool status',
            '  pose, pos      - Display current Cartesian coordinates',
            '  info [-v]      - Display SCARA toolchain specifications and limits',
            '  clear, cls     - Clear terminal screen',
            '  exit, quit, :q - Terminate the interactive REPL session',
            '',
            'Robotic DSL Instructions (Immediate Execution):',
            '  MOVE_L X=<mm> Y=<mm> Z=<mm> SPEED=<mm/s> - Linear motion',
            '  MOVE_J X=<mm> Y=<mm> Z=<mm> SPEED=<mm/s> - Joint motion',
            '  MOVE_REL [X=<mm>] [Y=<mm>] [Z=<mm>]      - Relative motion',
            '  JUMP X=<mm> Y=<mm> Z=<mm> HEIGHT=<mm>    - Gate pick/place',
            '  ARC CW|CCW X=<mm> Y=<mm> CX=<mm> CY=<mm> - Circular arc',
            '  WAIT MS=<ms>                              - Dwell delay',
            '  PUMP ON|OFF                               - Vacuum suction',
            '  VALVE ON|OFF                              - Vent blow-off',
            '  HOME                                      - Calibration',
        ]

        return '\n'.join(lines)

    def present_status(self, *, context: ReplSessionContext) -> str:
        '''
            Returns formatted status text for active session state.

            :param context: Active REPL session context model.
            :return: Multiline status string.
            :exceptions: None.
        '''
        elbow_str: str = 'LEFT' if context.elbow_left else 'RIGHT'
        pump_str: str = 'ACTIVE' if context.pump_active else 'INACTIVE'
        valve_str: str = 'ACTIVE' if context.valve_active else 'INACTIVE'
        lines: list[str] = [
            'Current Robot State:',
            f'  Pose:     X={context.pose.current_x:.2f} mm, Y={context.pose.current_y:.2f} mm, '
            f'Z={context.pose.current_z:.2f} mm, Phi={context.pose.current_theta4:.2f}°',
            f'  Config:   Elbow={elbow_str}, SpeedMode={context.speed_mode.name}, '
            f'ZoneMode={context.zone_mode.name}',
            f'  Pneumatics: Pump={pump_str}, Valve={valve_str}',
        ]

        return '\n'.join(lines)

    def present_pose(self, *, context: ReplSessionContext) -> str:
        '''
            Returns formatted Cartesian pose string.

            :param context: Active REPL session context model.
            :return: Single-line Cartesian pose string.
            :exceptions: None.
        '''
        return (
            f'Pose: X={context.pose.current_x:.2f} mm | Y={context.pose.current_y:.2f} mm | '
            f'Z={context.pose.current_z:.2f} mm | Phi={context.pose.current_theta4:.2f}°'
        )
