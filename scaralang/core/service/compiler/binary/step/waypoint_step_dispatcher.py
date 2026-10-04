# -*- coding: UTF-8 -*-

'''
Module
    waypoint_step_dispatcher.py
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
    Dispatches waypoints and commands into binary execution steps.
'''

from __future__ import annotations

from collections.abc import Sequence
from typing import Final

from scaralang.core.model.dsl.binary.step import Step
from scaralang.core.model.trajectory.waypoint import Waypoint
from scaralang.core.service.compiler.binary.command.icommand_compiler import ICommandCompiler
from scaralang.core.service.compiler.binary.motion.imotion_compiler import IMotionCompiler

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class WaypointStepDispatcher:
    '''
        Dispatches waypoints and commands into binary execution steps.

        It defines:

            :attributes:
                | _command_compiler - Hardware command compiler protocol instance.
                | _motion_compiler - Motion waypoint compiler protocol instance.
            :methods:
                | __init__ - Initializes WaypointStepDispatcher with injected compilers.
                | dispatch_steps - Dispatches sequence of waypoints into binary steps tuple.
                | get_version - Gets implementation version string.
    '''

    _command_compiler: ICommandCompiler
    _motion_compiler: IMotionCompiler

    def __init__(
        self,
        *,
        command_compiler: ICommandCompiler,
        motion_compiler: IMotionCompiler,
    ) -> None:
        '''
            Initializes WaypointStepDispatcher with injected compilers.

            :param command_compiler: Injected ICommandCompiler protocol instance.
            :param motion_compiler: Injected IMotionCompiler protocol instance.
            :exceptions: None.
        '''
        self._command_compiler: Final[ICommandCompiler] = command_compiler
        self._motion_compiler: Final[IMotionCompiler] = motion_compiler

    def dispatch_steps(
        self, *, waypoints: Sequence[Waypoint]
    ) -> tuple[Step, ...]:
        '''
            Dispatches sequence of domain waypoints into compiled binary steps.

            :param waypoints: Sequence of domain Waypoint instances.
            :return: Tuple of compiled Step instances.
            :exceptions: None.
        '''
        steps: list[Step] = []
        prev_angles: tuple[float, float, float, float] = (0.0, 0.0, 0.0, 0.0)

        for idx, pt in enumerate(waypoints):
            seq: int = idx & 0xFF
            line: int = idx + 1

            if pt.command:
                step = self._command_compiler.compile_command_step(
                    command=pt.command,
                    seq_num=seq,
                    line_num=line,
                )
            else:
                step, prev_angles = self._motion_compiler.compile_motion_step(
                    waypoint=pt,
                    seq_num=seq,
                    prev_angles=prev_angles,
                    line_num=line,
                )

            steps.append(step)

        return tuple(steps)

    def get_version(self) -> str:
        '''
            Gets implementation version string.

            :return: Version string.
            :exceptions: None.
        '''
        return __version__
