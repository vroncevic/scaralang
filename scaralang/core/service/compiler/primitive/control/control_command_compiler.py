# -*- coding: UTF-8 -*-

'''
Module
    control_command_compiler.py
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
    Compiles workflow control, homing, dwell, and motor enable/disable
    DSL instructions into waypoints.
'''

from __future__ import annotations

from scaralang.core.model.dsl.ast.command_type import ScaraCommandType
from scaralang.core.model.dsl.ast.instruction import ScaraInstruction
from scaralang.core.model.dsl.ast.instruction_param import InstructionParam
from scaralang.core.model.dsl.compiler.control_waypoint_descriptor import (
    ControlWaypointDescriptor,
)
from scaralang.core.model.dsl.compiler.scara_compiler_context import ScaraCompilerContext
from scaralang.core.model.motor.motor_drive_mode import MotorDriveMode
from scaralang.core.model.trajectory.waypoint import Waypoint
from scaralang.core.service.compiler.primitive.control.icontrol_waypoint_builder import (
    IControlWaypointBuilder,
)
from scaralang.core.service.motor.motor_config_factory import MotorConfigFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ControlCommandCompiler:
    '''
        Sub-compiler handling execution control instructions:
        HOME, WAIT_MS, HOLD, RESUME, ESTOP, ENABLE, DISABLE, CONFIG_MOTOR.

        It defines:

            :attributes:
                | _SUPPORTED - Frozenset of handled ScaraCommandType instances.
                | _waypoint_builder - Collaborator building execution control waypoints.
            :methods:
                | __init__ - Initializes ControlCommandCompiler with injected waypoint builder.
                | can_compile - Checks if command is a workflow control instruction.
                | compile - Appends control command waypoints to the waypoint accumulator.
    '''

    _SUPPORTED: frozenset[ScaraCommandType] = frozenset({
        ScaraCommandType.HOME,
        ScaraCommandType.WAIT_MS,
        ScaraCommandType.HOLD,
        ScaraCommandType.RESUME,
        ScaraCommandType.ESTOP,
        ScaraCommandType.ENABLE,
        ScaraCommandType.DISABLE,
        ScaraCommandType.CONFIG_MOTOR,
    })

    _waypoint_builder: IControlWaypointBuilder

    def __init__(
        self,
        *,
        waypoint_builder: IControlWaypointBuilder,
    ) -> None:
        '''
            Initializes ControlCommandCompiler with injected waypoint builder.

            :param waypoint_builder: Injected IControlWaypointBuilder instance.
            :exceptions: None.
        '''
        self._waypoint_builder = waypoint_builder

    def can_compile(self, *, instruction: ScaraInstruction) -> bool:
        '''
            Determines whether this sub-compiler handles the specified instruction.

            :param instruction: Primitive AST instruction node.
            :return: True if handled, False otherwise.
            :exceptions: None.
        '''
        return instruction.command_type in self._SUPPORTED

    def compile(
        self,
        *,
        instruction: ScaraInstruction,
        context: ScaraCompilerContext,
    ) -> tuple[Waypoint, ...]:
        '''
            Processes control instructions and returns control command waypoints.

            :param instruction: Primitive AST instruction node.
            :param context: Mutable compiler execution context.
            :return: Tuple of compiled Waypoint instances.
            :exceptions: None.
        '''
        cmd_type = instruction.command_type

        if cmd_type not in self._SUPPORTED:
            return ()

        params = instruction.parameters

        if cmd_type == ScaraCommandType.HOME:
            return (
                self._waypoint_builder.build_waypoint(
                    context=context,
                    descriptor=ControlWaypointDescriptor(
                        name='HOME',
                        command='<CMD:HOME>',
                        phi=0.0,
                        speed=context.speed_rapid,
                    ),
                ),
            )
        if cmd_type == ScaraCommandType.WAIT_MS:
            delay_ms = max(0, int(float(params.get(InstructionParam.MS, 0.0))))
            return (
                self._waypoint_builder.build_waypoint(
                    context=context,
                    descriptor=ControlWaypointDescriptor(
                        name=f'WAIT_{delay_ms}MS',
                        command=f'<CMD:WAIT#{delay_ms}>',
                        phi=context.current_phi,
                        speed=context.current_speed,
                    ),
                ),
            )
        if cmd_type == ScaraCommandType.CONFIG_MOTOR:
            mode_param = str(
                params.get(InstructionParam.MODE, MotorDriveMode.OPEN_LOOP.value)
            ).upper()
            mode_obj: MotorDriveMode = (
                MotorConfigFactory.parse_drive_mode(mode_param)
                if MotorConfigFactory.is_valid_drive_mode(mode_param)
                else MotorDriveMode.OPEN_LOOP
            )
            context.motor_drive_mode = mode_obj
            return (
                self._waypoint_builder.build_waypoint(
                    context=context,
                    descriptor=ControlWaypointDescriptor(
                        name=f'CONFIG_MOTOR_{mode_obj.value}',
                        command=f'<CMD:CONFIG_MOTOR#{mode_obj.value}>',
                        phi=context.current_phi,
                        speed=context.current_speed,
                    ),
                ),
            )
        return (
            self._waypoint_builder.build_waypoint(
                context=context,
                descriptor=ControlWaypointDescriptor(
                    name=cmd_type.value,
                    command=f'<CMD:{cmd_type.value}>',
                    phi=context.current_phi,
                    speed=context.current_speed,
                ),
            ),
        )
