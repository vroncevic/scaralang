# -*- coding: UTF-8 -*-

'''
Module
    factory.py
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
    Factory instantiating initialized CompilerContext instances.
'''

from __future__ import annotations

from typing import ClassVar

from scaralang.core.model.dsl.ast.tool_orient_mode import ToolOrientMode
from scaralang.core.model.dsl.ast.zone_mode import ZoneMode
from scaralang.core.model.dsl.compiler.compiler_blend_state import CompilerBlendState
from scaralang.core.model.dsl.compiler.compiler_context import CompilerContext
from scaralang.core.model.dsl.compiler.compiler_pose_state import CompilerPoseState
from scaralang.core.model.dsl.compiler.compiler_speed_state import CompilerSpeedState
from scaralang.core.model.dsl.macro.work_frame import WorkFrame
from scaralang.core.model.kinematics.elbow_config import ElbowConfig
from scaralang.core.model.kinematics.point_3d import Point3D
from scaralang.core.model.motor.motor_drive_mode import MotorDriveMode

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.9'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class CompilerContextFactory:
    '''
        Factory providing initialized CompilerContext instances and sub-states.

        It defines:

            :attributes:
                | DEFAULT_POSE_X - Initial Cartesian X coordinate in mm.
                | DEFAULT_POSE_Y - Initial Cartesian Y coordinate in mm.
                | DEFAULT_POSE_Z - Initial Cartesian vertical Z coordinate in mm.
                | DEFAULT_POSE_PHI - Initial tool orientation angle in degrees.
                | DEFAULT_SPEED_RAPID - Initial rapid traverse feedrate in mm/s.
                | DEFAULT_SPEED_WORK - Initial machining feedrate in mm/s.
                | DEFAULT_SPEED_CURRENT - Initial active motion feedrate in mm/s.
                | DEFAULT_ACCEL - Initial path acceleration in mm/s^2.
                | DEFAULT_OVERRIDE_PCT - Initial speed scaling percentage.
                | DEFAULT_ZONE_RADIUS - Initial corner blending radius in mm.
            :methods:
                | create - Creates an initialized CompilerContext instance.
                | get_version - Returns factory version string.
    '''

    DEFAULT_POSE_X: ClassVar[float] = 150.0
    DEFAULT_POSE_Y: ClassVar[float] = 0.0
    DEFAULT_POSE_Z: ClassVar[float] = 20.0
    DEFAULT_POSE_PHI: ClassVar[float] = 0.0

    DEFAULT_SPEED_RAPID: ClassVar[float] = 150.0
    DEFAULT_SPEED_WORK: ClassVar[float] = 40.0
    DEFAULT_SPEED_CURRENT: ClassVar[float] = 40.0
    DEFAULT_ACCEL: ClassVar[float] = 300.0
    DEFAULT_OVERRIDE_PCT: ClassVar[float] = 100.0

    DEFAULT_ZONE_RADIUS: ClassVar[float] = 0.0

    @classmethod
    def create(cls) -> CompilerContext:
        '''
            Creates an initialized CompilerContext instance.

            :return: Initialized CompilerContext instance.
            :exceptions: None.
        '''
        return CompilerContext(
            pose=CompilerPoseState(
                current_x=cls.DEFAULT_POSE_X,
                current_y=cls.DEFAULT_POSE_Y,
                current_z=cls.DEFAULT_POSE_Z,
                current_phi=cls.DEFAULT_POSE_PHI,
                elbow_config=ElbowConfig.RIGHT,
            ),
            speed=CompilerSpeedState(
                speed_rapid=cls.DEFAULT_SPEED_RAPID,
                speed_work=cls.DEFAULT_SPEED_WORK,
                current_speed=cls.DEFAULT_SPEED_CURRENT,
                active_accel=cls.DEFAULT_ACCEL,
                speed_override_pct=cls.DEFAULT_OVERRIDE_PCT,
            ),
            blend=CompilerBlendState(
                zone_mode=ZoneMode.FINE,
                zone_radius=cls.DEFAULT_ZONE_RADIUS,
            ),
            active_frame=WorkFrame(
                origin=Point3D(x=0.0, y=0.0, z=0.0),
                angle_deg=0.0,
            ),
            tool_orient_mode=ToolOrientMode.FIXED,
            motor_drive_mode=MotorDriveMode.OPEN_LOOP,
            pallets={},
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory version string representation.

            :return: Factory version string.
            :exceptions: None.
        '''
        return __version__
