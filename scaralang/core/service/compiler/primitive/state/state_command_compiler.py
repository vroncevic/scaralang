# -*- coding: UTF-8 -*-

'''
Module
    state_command_compiler.py
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
    Compiles machine state, kinematics configuration, and speed override
    DSL instructions into compiler context.
'''

from __future__ import annotations

from scaralang.core.model.dsl.ast.command_type import ScaraCommandType
from scaralang.core.model.dsl.ast.instruction import ScaraInstruction
from scaralang.core.model.dsl.ast.instruction_param import InstructionParam
from scaralang.core.model.dsl.ast.speed_mode import SpeedMode
from scaralang.core.model.dsl.ast.zone_mode import ZoneMode
from scaralang.core.model.dsl.compiler.scara_compiler_context import ScaraCompilerContext
from scaralang.core.model.kinematics.elbow_config import ElbowConfig
from scaralang.core.model.trajectory.waypoint import Waypoint

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.5'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class StateCommandCompiler:
    '''
        Sub-compiler handling state, speed, acceleration, elbow, and zone instructions.

        It defines:

            :attributes:
                | _SUPPORTED - Frozenset of handled ScaraCommandType instances.
            :methods:
                | can_compile - Checks if command is a state configuration instruction.
                | compile - Updates ScaraCompilerContext with instruction parameters.
    '''

    _SUPPORTED: frozenset[ScaraCommandType] = frozenset({
        ScaraCommandType.SPEED,
        ScaraCommandType.ACCEL,
        ScaraCommandType.OVERRIDE,
        ScaraCommandType.CONFIG_ELBOW,
        ScaraCommandType.ZONE,
    })

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
            Applies state configuration parameters to compiler context.

            :param instruction: Primitive AST instruction node.
            :param context: Mutable compiler execution context.
            :return: Tuple of compiled Waypoint instances.
            :exceptions: None.
        '''
        cmd_type = instruction.command_type

        if cmd_type not in self._SUPPORTED:
            return ()

        params = instruction.parameters

        match cmd_type:
            case ScaraCommandType.SPEED:
                raw_mode = str(params.get(InstructionParam.MODE, SpeedMode.WORK)).upper()
                spd = float(params.get(InstructionParam.SPEED, 40.0))

                if raw_mode == SpeedMode.RAPID:
                    context.speed.speed_rapid = spd
                else:
                    context.speed.speed_work = spd
                    context.speed.current_speed = spd

            case ScaraCommandType.ACCEL:
                context.speed.active_accel = float(params.get(InstructionParam.ACCEL, 300.0))

            case ScaraCommandType.OVERRIDE:
                context.speed.speed_override_pct = float(
                    params.get(InstructionParam.PERCENT, 100.0)
                )

            case ScaraCommandType.CONFIG_ELBOW:
                raw_elbow = str(params.get(InstructionParam.ELBOW, ElbowConfig.RIGHT)).upper()
                context.pose.elbow_config = (
                    ElbowConfig(raw_elbow)
                    if raw_elbow in (ElbowConfig.RIGHT, ElbowConfig.LEFT)
                    else ElbowConfig.RIGHT
                )

            case ScaraCommandType.ZONE:
                raw_zone = str(params.get(InstructionParam.MODE, ZoneMode.FINE)).upper()
                context.blend.zone_mode = (
                    ZoneMode(raw_zone)
                    if raw_zone in (ZoneMode.FINE, ZoneMode.EXACT, ZoneMode.BLEND)
                    else ZoneMode.FINE
                )
                context.blend.zone_radius = float(params.get(InstructionParam.RADIUS, 0.0))

        return ()
