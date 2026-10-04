# -*- coding: UTF-8 -*-

'''
Module
    repl_command_dispatcher.py
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
    Concrete implementation of REPL command dispatcher.
'''

from __future__ import annotations

from typing import Final

from scaralang.core.model.repl.repl_dispatch_result import ReplDispatchResult
from scaralang.core.model.repl.repl_session_context import ReplSessionContext
from scaralang.core.service.info.itoolchain_info_provider import IToolchainInfoProvider

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ReplCommandDispatcher:
    '''
        Command dispatcher routing user inputs between built-in commands and DSL compilation.

        It defines:

            :attributes:
                | _info_provider - Injected toolchain metadata and instruction catalog provider.
            :methods:
                | __init__ - Initializes dispatcher with injected info provider.
                | dispatch_line - Dispatches line to built-in session handlers or flags for DSL.
                | format_help - Returns formatted help text for REPL commands and syntax.
                | format_status - Returns formatted status text for active session state.
                | format_pose - Returns formatted Cartesian pose string.
    '''

    _info_provider: IToolchainInfoProvider

    def __init__(
        self,
        *,
        info_provider: IToolchainInfoProvider,
    ) -> None:
        '''
            Initializes REPL command dispatcher with injected collaborators.

            :param info_provider: Injected toolchain metadata and instruction provider.
            :exceptions: None.
        '''
        self._info_provider: Final[IToolchainInfoProvider] = info_provider

    def dispatch_line(
        self,
        *,
        line: str,
        context: ReplSessionContext,
    ) -> ReplDispatchResult:
        '''
            Dispatches line to built-in session handlers or flags for DSL compilation.

            :param line: Input command line string.
            :param context: Active REPL session context model.
            :return: ReplDispatchResult model capturing dispatch outcome.
            :exceptions: None.
        '''
        tokens: list[str] = [token.lower() for token in line.strip().split()]
        result: ReplDispatchResult

        match tokens:
            case []:
                result = ReplDispatchResult(
                    is_exit=False,
                    is_handled=True,
                    message='',
                )
            case ['exit' | 'quit' | ':q', *_]:
                result = ReplDispatchResult(
                    is_exit=True,
                    is_handled=True,
                    message='Session terminated.',
                )
            case ['help' | '?', *_]:
                result = ReplDispatchResult(
                    is_exit=False,
                    is_handled=True,
                    message=self.format_help(),
                )
            case ['clear' | 'cls', *_]:
                result = ReplDispatchResult(
                    is_exit=False,
                    is_handled=True,
                    message='\033[H\033[2J',
                )
            case ['info' | 'specs' | 'catalog', *args]:
                is_verbose: bool = any(
                    flag in ('-v', '--verbose', 'verbose') for flag in args
                )
                info_lines: tuple[str, ...] = self._info_provider.get_toolchain_info(
                    verbose=is_verbose
                )
                result = ReplDispatchResult(
                    is_exit=False,
                    is_handled=True,
                    message='\n'.join(info_lines),
                )
            case ['status' | 'state', *_]:
                result = ReplDispatchResult(
                    is_exit=False,
                    is_handled=True,
                    message=self.format_status(context=context),
                )
            case ['pose' | 'pos', *_]:
                result = ReplDispatchResult(
                    is_exit=False,
                    is_handled=True,
                    message=self.format_pose(context=context),
                )
            case _:
                result = ReplDispatchResult(
                    is_exit=False,
                    is_handled=False,
                    message='',
                )

        return result

    def format_help(self) -> str:
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
            '  JUMP X=<mm> Y=<mm> Z=<mm> HEIGHT=<mm>    - Gate pick/place',
            '  ARC CW|CCW X=<mm> Y=<mm> CX=<mm> CY=<mm> - Circular arc',
            '  WAIT MS=<ms>                              - Dwell delay',
            '  PUMP ON|OFF                               - Vacuum suction',
            '  VALVE ON|OFF                              - Vent blow-off',
            '  HOME                                      - Calibration',
        ]

        return '\n'.join(lines)

    def format_status(self, *, context: ReplSessionContext) -> str:
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

    def format_pose(self, *, context: ReplSessionContext) -> str:
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
