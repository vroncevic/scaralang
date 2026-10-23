# -*- coding: UTF-8 -*-

'''
Module
    discretizer.py
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
    Discretizes Cartesian motion waypoints into hardware motor step coordinates.
'''

from __future__ import annotations

from math import radians
from sys import stderr
from typing import ClassVar, Final

from scaralang.core.model.exceptions.kinematics import ScaraKinematicsError
from scaralang.core.model.kinematics.pose.cartesian import CartesianPose
from scaralang.core.model.kinematics.solver.status import IkStatus
from scaralang.core.model.kinematics.pose.angles import JointAngles
from scaralang.core.model.kinematics.pose.steps import JointStepCoordinates
from scaralang.core.model.kinematics.solver.solution import ScaraJoints
from scaralang.core.model.protocol.joint_steps import JointSteps
from scaralang.core.model.trajectory.plan.waypoint import Waypoint
from scaralang.core.service.compiler.binary.step.discretizer.dependencies import DiscretizerDependencies
from scaralang.core.service.compiler.binary.step.duration.icalculator import ISegmentDurationCalculator
from scaralang.core.service.kinematics.solver.analytical.spatial.isolver import ISpatialKinematicsSolver
from scaralang.core.service.kinematics.solver.numerical.spatial.isolver import INumericalSpatialKinematicsSolver
from scaralang.core.service.kinematics.transmission.iconverter import IJointStepTransmissionConverter

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class StepDiscretizer:
    '''
        Discretizes Cartesian motion waypoints into hardware motor step coordinates.

        It defines:

            :attributes:
                | DEFAULT_FEEDRATE_SCALE - Default percentage feedrate scale.
                | DEFAULT_ELBOW_LEFT - Default IK elbow configuration flag.
                | _spatial - Analytical spatial SCARA kinematics solver engine.
                | _numerical_spatial - Injected numerical DLS spatial kinematics solver.
                | _transmission - Injected bidirectional transmission converter.
                | _duration_calculator - Injected segment duration calculator.
            :methods:
                | __init__ - Initializes step discretizer with dependency bundle.
                | angles_to_steps - Converts joint radians/mm to integer motor steps.
                | discretize_waypoint - Solves IK and maps Cartesian waypoint into JointSteps.
                | get_version - Returns implementation version string.
    '''

    DEFAULT_FEEDRATE_SCALE: ClassVar[int] = 100
    DEFAULT_ELBOW_LEFT: ClassVar[bool] = False

    _spatial: ISpatialKinematicsSolver
    _numerical_spatial: INumericalSpatialKinematicsSolver
    _transmission: IJointStepTransmissionConverter
    _duration_calculator: ISegmentDurationCalculator

    def __init__(self, *, dependencies: DiscretizerDependencies) -> None:
        '''
            Initializes step discretizer with injected dependencies bundle.

            :param dependencies: Injected DiscretizerDependencies bundle.
            :exceptions: None.
        '''
        self._spatial: Final[ISpatialKinematicsSolver] = dependencies.spatial
        self._numerical_spatial: Final[INumericalSpatialKinematicsSolver] = (
            dependencies.numerical_spatial
        )
        self._transmission: Final[IJointStepTransmissionConverter] = dependencies.transmission
        self._duration_calculator: Final[ISegmentDurationCalculator] = (
            dependencies.duration_calculator
        )

    def angles_to_steps(
        self,
        theta1_rad: float,
        theta2_rad: float,
        z_mm: float,
        theta4_rad: float,
    ) -> JointStepCoordinates:
        '''
            Converts joint angles and linear Z travel into discrete motor steps.

            :param theta1_rad: Shoulder joint angle in radians.
            :param theta2_rad: Elbow joint angle in radians.
            :param z_mm: Linear vertical travel in millimeters.
            :param theta4_rad: Wrist joint angle in radians.
            :return: JointStepCoordinates containing (j1, j2, z, j4) integer microsteps.
            :exceptions: None.
        '''
        return self._transmission.angles_to_steps(
            theta1_rad, theta2_rad, z_mm, theta4_rad
        )

    def discretize_waypoint(
        self,
        *,
        waypoint: Waypoint,
        prev_angles: JointAngles,
    ) -> tuple[JointSteps, JointAngles]:
        '''
            Solves IK and converts Cartesian waypoint into motor steps with duration.

            :param waypoint: Target Cartesian Waypoint instance.
            :param prev_angles: Preceding joint angles model.
            :return: Tuple of (JointSteps model, new joint angles model).
            :exceptions:
                | ScaraKinematicsError: If position is unreachable or limits exceeded.
        '''
        pose = CartesianPose(
            x=waypoint.x,
            y=waypoint.y,
            z=waypoint.z,
            phi=radians(waypoint.phi),
        )
        ik_sol: ScaraJoints = self._spatial.solve_ik_4d(
            pose=pose,
            elbow_left=self.DEFAULT_ELBOW_LEFT,
        )

        if not ik_sol.reachable:
            if ik_sol.status == IkStatus.Z_LIMIT_EXCEEDED:
                raise ScaraKinematicsError(
                    f'Waypoint ({waypoint.x:.2f}, {waypoint.y:.2f}, {waypoint.z:.2f}) '
                    f'is outside vertical limits ({ik_sol.status.name}).'
                )

            analytical_status: IkStatus = ik_sol.status
            initial_guess = ScaraJoints(
                theta1=prev_angles.theta1,
                theta2=prev_angles.theta2,
                z=prev_angles.z,
                theta4=prev_angles.theta4,
                reachable=True,
                status=IkStatus.SUCCESS,
            )
            ik_sol = self._numerical_spatial.solve_dls_4d(
                target_pose=pose,
                initial_joints=initial_guess,
            )
            if not ik_sol.reachable:
                raise ScaraKinematicsError(
                    f'Waypoint ({waypoint.x:.2f}, {waypoint.y:.2f}, {waypoint.z:.2f}) '
                    f'is unreachable: analytical solver failed ({analytical_status.name}), '
                    f'and numerical DLS fallback failed ({ik_sol.status.name}).'
                )

            stderr.write(
                f'scaralang: warning: Waypoint ({waypoint.x:.2f}, {waypoint.y:.2f}, {waypoint.z:.2f}) '
                f'analytical solver failed ({analytical_status.name}); '
                f'recovered using numerical DLS fallback.\n'
            )

        new_angles = JointAngles(
            theta1=ik_sol.theta1,
            theta2=ik_sol.theta2,
            z=ik_sol.z,
            theta4=ik_sol.theta4,
        )
        target_steps: JointStepCoordinates = self.angles_to_steps(
            new_angles.theta1,
            new_angles.theta2,
            new_angles.z,
            new_angles.theta4,
        )
        current_steps: JointStepCoordinates = self.angles_to_steps(
            prev_angles.theta1,
            prev_angles.theta2,
            prev_angles.z,
            prev_angles.theta4,
        )
        duration_us: int = self._duration_calculator.calculate_duration(
            current_steps=current_steps,
            target_steps=target_steps,
            speed_mm_s=waypoint.speed,
        )

        return (
            JointSteps(
                target_j1_steps=target_steps.j1,
                target_j2_steps=target_steps.j2,
                target_z_steps=target_steps.z,
                target_j4_steps=target_steps.j4,
                duration_us=duration_us,
                feedrate_scale=self.DEFAULT_FEEDRATE_SCALE,
            ),
            new_angles,
        )

    def get_version(self) -> str:
        '''
            Returns implementation version string.

            :return: Implementation version string.
            :exceptions: None.
        '''
        return __version__
