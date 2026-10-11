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
    Converts Cartesian waypoints into discrete motor joint steps with timing.
'''

from __future__ import annotations

from math import radians
from typing import Final

from scaralang.core.model.exceptions.scara_kinematics_error import ScaraKinematicsError
from scaralang.core.model.kinematics.point_2d import Point2D
from scaralang.core.model.protocol.joint_steps import JointSteps
from scaralang.core.model.trajectory.waypoint import Waypoint
from scaralang.core.service.compiler.binary.step.discretizer.dependencies import DiscretizerDependencies
from scaralang.core.service.kinematics.iservice import IKinematicsService
from scaralang.core.service.kinematics.transmission.iconverter import IJointStepTransmissionConverter

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.8'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class StepDiscretizer:
    '''
        Discretizes Cartesian motion waypoints into hardware motor step coordinates.

        It defines:

            :attributes:
                | _kinematics - Analytical SCARA kinematics calculation engine.
                | _transmission - Injected bidirectional transmission converter.
            :methods:
                | __init__ - Initializes step discretizer with dependency bundle.
                | angles_to_steps - Converts joint radians/mm to integer motor steps.
                | discretize_waypoint - Solves IK and maps Cartesian waypoint into JointSteps.
                | calculate_segment_duration - Computes execution duration in microseconds.
                | get_version - Returns implementation version string.
    '''

    _kinematics: IKinematicsService
    _transmission: IJointStepTransmissionConverter

    def __init__(self, *, dependencies: DiscretizerDependencies) -> None:
        '''
            Initializes step discretizer with injected dependencies bundle.

            :param dependencies: Injected DiscretizerDependencies bundle.
            :exceptions: None.
        '''
        self._kinematics: Final[IKinematicsService] = dependencies.kinematics
        self._transmission: Final[IJointStepTransmissionConverter] = dependencies.transmission

    def angles_to_steps(
        self,
        theta1_rad: float,
        theta2_rad: float,
        z_mm: float,
        theta4_rad: float,
    ) -> tuple[int, int, int, int]:
        '''
            Converts joint angles and linear Z travel into discrete motor steps.

            :param theta1_rad: Shoulder joint angle in radians.
            :param theta2_rad: Elbow joint angle in radians.
            :param z_mm: Linear vertical travel in millimeters.
            :param theta4_rad: Wrist joint angle in radians.
            :return: Tuple of (j1, j2, z, j4) integer microsteps.
            :exceptions: None.
        '''
        return self._transmission.angles_to_steps(
            theta1_rad, theta2_rad, z_mm, theta4_rad
        )

    def discretize_waypoint(
        self,
        *,
        waypoint: Waypoint,
        prev_angles: tuple[float, float, float, float],
    ) -> tuple[JointSteps, tuple[float, float, float, float]]:
        '''
            Solves IK and converts Cartesian waypoint into motor steps with duration.

            :param waypoint: Target Cartesian Waypoint instance.
            :param prev_angles: Preceding joint angles (th1, th2, z, th4).
            :return: Tuple of (JointSteps model, new joint angles tuple).
            :exceptions: ScaraKinematicsError if position is unreachable.
        '''
        ik_sol: tuple[float, float] | None = self._kinematics.solve_ik(
            point=Point2D(x=waypoint.x, y=waypoint.y),
            elbow_left=False,
        )

        if ik_sol is None:
            raise ScaraKinematicsError(
                f'Waypoint ({waypoint.x:.2f}, {waypoint.y:.2f}) is outside kinematic reach.'
            )

        new_angles: tuple[float, float, float, float] = (
            ik_sol[0], ik_sol[1], waypoint.z, radians(waypoint.phi)
        )
        target_steps: tuple[int, int, int, int] = self.angles_to_steps(*new_angles)
        current_steps: tuple[int, int, int, int] = self.angles_to_steps(*prev_angles)
        duration_us: int = self.calculate_segment_duration(
            current_steps=current_steps,
            target_steps=target_steps,
            speed_mm_s=waypoint.speed,
        )

        return (
            JointSteps(
                target_j1_steps=target_steps[0],
                target_j2_steps=target_steps[1],
                target_z_steps=target_steps[2],
                target_j4_steps=target_steps[3],
                duration_us=duration_us,
                feedrate_scale=100,
            ),
            new_angles,
        )

    def calculate_segment_duration(
        self,
        *,
        current_steps: tuple[int, int, int, int],
        target_steps: tuple[int, int, int, int],
        speed_mm_s: float,
    ) -> int:
        '''
            Computes segment execution duration in microseconds.

            :param current_steps: Initial joint step coordinates.
            :param target_steps: Target joint step coordinates.
            :param speed_mm_s: Planned linear tool speed in mm/s.
            :return: Microsecond execution duration.
            :exceptions: None.
        '''
        deltas: tuple[int, int, int, int] = (
            abs(target_steps[0] - current_steps[0]),
            abs(target_steps[1] - current_steps[1]),
            abs(target_steps[2] - current_steps[2]),
            abs(target_steps[3] - current_steps[3]),
        )
        max_delta: int = max(deltas)

        if max_delta == 0:
            return 1000

        safe_speed: float = max(1.0, speed_mm_s)
        duration_sec: float = max_delta / (safe_speed * 10.0)
        duration_us: int = int(duration_sec * 1000000.0)

        return max(duration_us, 5000)

    def get_version(self) -> str:
        '''
            Returns implementation version string.

            :return: Implementation version string.
            :exceptions: None.
        '''
        return __version__
