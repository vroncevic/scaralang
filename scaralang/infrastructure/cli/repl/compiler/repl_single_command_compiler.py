# -*- coding: UTF-8 -*-

'''
Module
    repl_single_command_compiler.py
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
    Concrete implementation of single-line DSL instruction compiler.
'''

from __future__ import annotations

from typing import Final

from scaralang.core.model.dsl.binary.step import Step
from scaralang.core.model.exceptions.scara_semantic_error import ScaraSemanticError
from scaralang.core.model.protocol.binary_frame import BinaryFrame
from scaralang.core.model.protocol.message_id import MessageId
from scaralang.core.model.repl.repl_pose_state import ReplPoseState
from scaralang.core.model.repl.repl_session_context import ReplSessionContext
from scaralang.core.service.compiler.iscara_compiler import IScaraCompiler
from scaralang.core.service.compiler.plan.iscara_plan_compiler import IScaraPlanCompiler

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.5'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ReplSingleCommandCompiler:
    '''
        Compiles single-line DSL instructions into executable steps and updated session contexts.

        It defines:

            :attributes:
                | _compiler - Injected IScaraPlanCompiler protocol instance.
                | _binary_compiler - Injected IScaraCompiler protocol instance.
            :methods:
                | __init__ - Initializes compiler with injected DSL compilers.
                | compile_instruction - Compiles single instruction and derives updated context.
                | update_context - Computes updated session context model from plan and step.
    '''

    _compiler: IScaraPlanCompiler
    _binary_compiler: IScaraCompiler

    def __init__(
        self,
        *,
        compiler: IScaraPlanCompiler,
        binary_compiler: IScaraCompiler,
    ) -> None:
        '''
            Initializes single-line command compiler.

            :param compiler: Injected IScaraPlanCompiler protocol instance.
            :param binary_compiler: Injected IScaraCompiler protocol instance.
            :exceptions: None.
        '''
        self._compiler: Final[IScaraPlanCompiler] = compiler
        self._binary_compiler: Final[IScaraCompiler] = binary_compiler

    def compile_instruction(
        self,
        *,
        line: str,
        context: ReplSessionContext,
    ) -> tuple[BinaryFrame, Step, ReplSessionContext]:
        '''
            Compiles single DSL line into BinaryFrame, Step, and updated context.

            :param line: Single DSL instruction line.
            :param context: Active REPL session context model.
            :return: Tuple of (BinaryFrame, Step, ReplSessionContext).
            :exceptions:
                | ScaraSemanticError: If no binary steps compiled for line.
        '''
        plan = self._compiler.compile_script(source=line)
        program = self._binary_compiler.compile_plan(plan=plan)

        if not program.steps:
            raise ScaraSemanticError(f'No binary steps compiled for line: {line}')

        step: Step = program.steps[-1]
        new_context: ReplSessionContext = self.update_context(
            line=line, step=step, plan_waypoints=plan.waypoints, context=context
        )

        return step.frame, step, new_context

    def update_context(
        self,
        *,
        line: str,
        step: Step,
        plan_waypoints: tuple[object, ...],
        context: ReplSessionContext,
    ) -> ReplSessionContext:
        '''
            Computes updated session context model from plan and step.

            :param line: Raw DSL instruction line.
            :param step: Compiled binary execution step.
            :param plan_waypoints: Waypoints generated from the plan.
            :param context: Prior active REPL session context.
            :return: Updated ReplSessionContext instance.
            :exceptions: None.
        '''
        x = context.pose.current_x
        y = context.pose.current_y
        z = context.pose.current_z
        phi = context.pose.current_theta4

        if step.frame.msg_id == MessageId.CMD_HOME:
            x, y, z, phi = 150.0, 0.0, 20.0, 0.0
        elif plan_waypoints:
            last_wp = plan_waypoints[-1]
            cmd_name: str = str(getattr(last_wp, 'command', ''))

            if not cmd_name.startswith('<CMD:'):
                x = float(getattr(last_wp, 'x', x))
                y = float(getattr(last_wp, 'y', y))
                z = float(getattr(last_wp, 'z', z))
                phi = float(getattr(last_wp, 'phi', phi))

        upper = line.strip().upper()
        pump = (
            True if 'PUMP ON' in upper
            else (False if 'PUMP OFF' in upper else context.pump_active)
        )
        valve = (
            True if 'VALVE ON' in upper
            else (False if 'VALVE OFF' in upper else context.valve_active)
        )

        return ReplSessionContext(
            pose=ReplPoseState(
                current_x=x,
                current_y=y,
                current_z=z,
                current_theta4=phi,
            ),
            elbow_left=context.elbow_left,
            speed_mode=context.speed_mode,
            zone_mode=context.zone_mode,
            pump_active=pump,
            valve_active=valve,
        )
