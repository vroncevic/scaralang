# -*- coding: UTF-8 -*-

'''
Module
    compiler.py
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
    Compiles Cartesian motion waypoints into discrete joint steps and binary move frames.
'''

from __future__ import annotations

from typing import Final

from scaralang.core.model.dsl.binary.step import BinaryStep
from scaralang.core.model.kinematics.pose.angles import JointAngles
from scaralang.core.model.kinematics.pose.steps import JointStepCoordinates
from scaralang.core.model.protocol.frame import BinaryFrame
from scaralang.core.model.trajectory.plan.waypoint import Waypoint
from scaralang.core.service.compiler.binary.motion.dependencies import MotionDependencies
from scaralang.core.service.compiler.binary.step.discretizer.idiscretizer import IStepDiscretizer
from scaralang.core.service.protocol.ipacker import IBinaryFramePacker
from scaralang.core.service.protocol.imotion_builder import IBinaryMotionFrameBuilder

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class MotionCompiler:
    '''
        Compiles Cartesian motion waypoints into discrete joint steps and binary move frames.

        It defines:

            :attributes:
                | _discretizer - Kinematic discretization service.
                | _frame_builder - Binary motion frame assembler protocol.
                | _frame_packer - Binary frame packer protocol.
            :methods:
                | __init__ - Initializes motion step compiler with injected dependencies.
                | compile_motion_step - Compiles a single motion waypoint into a binary step.
                | get_version - Gets implementation version string.
    '''

    _discretizer: IStepDiscretizer
    _frame_builder: IBinaryMotionFrameBuilder
    _frame_packer: IBinaryFramePacker

    def __init__(self, *, dependencies: MotionDependencies) -> None:
        '''
            Initializes motion step compiler with injected dependencies.

            :param dependencies: MotionDependencies parameter bundle.
            :exceptions: None.
        '''
        self._discretizer: Final[IStepDiscretizer] = dependencies.discretizer
        self._frame_builder: Final[IBinaryMotionFrameBuilder] = dependencies.frame_builder
        self._frame_packer: Final[IBinaryFramePacker] = dependencies.frame_packer

    def compile_motion_step(
        self,
        *,
        waypoint: Waypoint,
        seq_num: int,
        prev_angles: JointAngles,
        line_num: int
    ) -> tuple[BinaryStep, JointAngles]:
        '''
            Compiles a motion waypoint into a binary joint move step.

            :param waypoint: Target Cartesian waypoint.
            :param seq_num: Frame sequence counter.
            :param prev_angles: Previous joint angles model.
            :param line_num: Source line index.
            :return: Tuple of compiled BinaryStep and updated joint angles model.
            :exceptions: ValueError if kinematic solving fails.
        '''
        joint_steps, new_angles = self._discretizer.discretize_waypoint(
            waypoint=waypoint, prev_angles=prev_angles
        )
        frame: BinaryFrame = self._frame_builder.build_joint_move(
            seq_num=seq_num, steps=joint_steps
        )
        raw_bytes: bytes = self._frame_packer.pack_frame(frame=frame)
        target_steps = JointStepCoordinates(
            j1=joint_steps.target_j1_steps,
            j2=joint_steps.target_j2_steps,
            z=joint_steps.target_z_steps,
            j4=joint_steps.target_j4_steps,
        )
        step = BinaryStep(
            frame=frame,
            raw_bytes=raw_bytes,
            duration_us=joint_steps.duration_us,
            target_steps=target_steps,
            description=f'MOVE X={waypoint.x:.1f} Y={waypoint.y:.1f} Z={waypoint.z:.1f}',
            line_number=line_num
        )

        return step, new_angles

    def get_version(self) -> str:
        '''
            Gets implementation version string.

            :return: Version string.
            :exceptions: None.
        '''
        return __version__
