# -*- coding: UTF-8 -*-

'''
Module
    scara_compiler_context.py
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
    Stateful domain model tracking robot pose, coordinate frames, speeds,
    and pallets during compilation.
'''

from __future__ import annotations

from dataclasses import dataclass, field

from scaralang.core.model.dsl.ast.tool_orient_mode import ToolOrientMode
from scaralang.core.model.dsl.compiler.compiler_blend_state import CompilerBlendState
from scaralang.core.model.dsl.compiler.compiler_pose_state import CompilerPoseState
from scaralang.core.model.dsl.compiler.compiler_speed_state import CompilerSpeedState
from scaralang.core.model.dsl.macro.pallet_definition import PalletDefinition
from scaralang.core.model.dsl.macro.work_frame import WorkFrame
from scaralang.core.model.kinematics.point_2d import Point2D
from scaralang.core.model.motor.motor_drive_mode import MotorDriveMode

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(slots=True, kw_only=True)
class ScaraCompilerContext:
    '''
        Stateful compiler context tracking coordinate transformation, speeds, pallets, and pose.

        It defines:

            :attributes:
                | pose - Stateful Cartesian pose coordinates and elbow configuration.
                | speed - Stateful feedrates, accelerations, and overrides.
                | blend - Stateful corner zone mode and blend radius.
                | active_frame - Active planar work coordinate frame.
                | tool_orient_mode - Tool orientation mode (FIXED, TANGENTIAL, JOINT_LOCKED).
                | motor_drive_mode - Active motor actuation mode (OPEN_LOOP or CLOSED_LOOP).
                | pallets - Dictionary mapping pallet names to PalletDefinition entities.
    '''

    pose: CompilerPoseState = field(default_factory=CompilerPoseState)
    speed: CompilerSpeedState = field(default_factory=CompilerSpeedState)
    blend: CompilerBlendState = field(default_factory=CompilerBlendState)
    active_frame: WorkFrame = field(
        default_factory=lambda: WorkFrame(
            origin=Point2D(x=0.0, y=0.0), angle_deg=0.0
        )
    )
    tool_orient_mode: ToolOrientMode = ToolOrientMode.FIXED
    motor_drive_mode: MotorDriveMode = MotorDriveMode.OPEN_LOOP
    pallets: dict[str, PalletDefinition] = field(default_factory=dict)
