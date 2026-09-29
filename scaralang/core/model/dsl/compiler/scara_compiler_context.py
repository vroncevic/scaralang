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
    Stateful domain model tracking robot pose, coordinate frames, speeds, and pallets during compilation.
'''

from __future__ import annotations

from dataclasses import dataclass, field

from scaralang.core.model.dsl.ast.tool_orient_mode import ToolOrientMode
from scaralang.core.model.dsl.ast.zone_mode import ZoneMode
from scaralang.core.model.dsl.macro.pallet_definition import PalletDefinition
from scaralang.core.model.dsl.macro.work_frame import WorkFrame
from scaralang.core.model.kinematics.elbow_config import ElbowConfig
from scaralang.core.model.motor.motor_drive_mode import MotorDriveMode

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(slots=True, kw_only=True)
class ScaraCompilerContext:
    '''
        Stateful compiler context tracking coordinate transformation, speeds, pallets, and pose.

        It defines:

            :attributes:
                | current_x - Current Cartesian X coordinate in mm.
                | current_y - Current Cartesian Y coordinate in mm.
                | current_z - Current Cartesian Z coordinate in mm.
                | current_phi - Current 4th axis tool orientation in degrees.
                | speed_rapid - Default rapid feedrate in mm/s.
                | speed_work - Default work feedrate in mm/s.
                | current_speed - Active motion feedrate in mm/s.
                | active_accel - Active path acceleration in mm/s^2.
                | elbow_config - Active elbow kinematic solution (RIGHT or LEFT).
                | active_frame - Active planar work coordinate frame.
                | tool_orient_mode - Tool orientation mode (FIXED, TANGENTIAL, JOINT_LOCKED).
                | zone_mode - Corner transition mode (FINE or BLEND).
                | zone_radius - Corner blend radius in mm.
                | speed_override_pct - Global velocity scaling percentage (1-100).
                | motor_drive_mode - Active motor actuation mode (OPEN_LOOP or CLOSED_LOOP).
                | pallets - Dictionary mapping pallet names to PalletDefinition entities.
    '''

    current_x: float = 150.0
    current_y: float = 0.0
    current_z: float = 20.0
    current_phi: float = 0.0
    speed_rapid: float = 150.0
    speed_work: float = 40.0
    current_speed: float = 40.0
    active_accel: float = 300.0
    elbow_config: ElbowConfig = ElbowConfig.RIGHT
    active_frame: WorkFrame = field(
        default_factory=lambda: WorkFrame(x=0.0, y=0.0, angle_deg=0.0)
    )
    tool_orient_mode: ToolOrientMode = ToolOrientMode.FIXED
    zone_mode: ZoneMode = ZoneMode.FINE
    zone_radius: float = 0.0
    speed_override_pct: float = 100.0
    motor_drive_mode: MotorDriveMode = MotorDriveMode.OPEN_LOOP
    pallets: dict[str, PalletDefinition] = field(default_factory=dict)
