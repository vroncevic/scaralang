# -*- coding: UTF-8 -*-

'''
Module
    evaluator.py
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
    Implementation of manipulator workspace envelope and joint angle limit evaluation.
'''

from __future__ import annotations

from math import degrees, hypot
from typing import ClassVar, Final

from scaralang.core.model.kinematics.solver.elbow import ElbowConfig
from scaralang.core.model.kinematics.pose.point_2d import Point2D
from scaralang.core.model.kinematics.pose.point_3d import Point3D
from scaralang.core.model.kinematics.profile.bounds import ScaraBounds
from scaralang.core.model.kinematics.solver.solution_2d import ScaraJoints2D
from scaralang.core.service.kinematics.solver.analytical.planar.isolver import IPlanarKinematicsSolver

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class WorkspaceBoundsEvaluator:
    '''
        Evaluates physical manipulator workspace envelope, reach radii, and joint angular limits.

        It defines:

            :attributes:
                | _bounds - Robot ScaraBounds containing link lengths, limits, and margins.
                | _planar - Injected planar kinematics solver collaborator.
                | _r_min - Minimum annular reach distance from origin in mm.
                | _r_max - Maximum annular reach distance from origin in mm.
            :methods:
                | __init__ - Initializes evaluator with robot bounds and planar solver.
                | is_in_workspace - Checks whether coordinates fall within annular envelope.
                | is_joint_reachable - Evaluates if position is reachable within joint limits.
                | get_bounds - Returns active ScaraBounds instance.
                | get_version - Returns evaluator component version string.
    '''

    _EPSILON: ClassVar[float] = 1e-4

    _bounds: ScaraBounds
    _planar: IPlanarKinematicsSolver
    _r_min: float
    _r_max: float

    def __init__(
        self,
        *,
        bounds: ScaraBounds,
        planar: IPlanarKinematicsSolver,
    ) -> None:
        '''
            Initializes workspace bounds evaluator with bounds and planar solver.

            :param bounds: Injected ScaraBounds model instance.
            :param planar: Injected IPlanarKinematicsSolver protocol collaborator.
            :exceptions: None.
        '''
        self._bounds: Final[ScaraBounds] = bounds
        self._planar: Final[IPlanarKinematicsSolver] = planar
        self._r_min: Final[float] = max(
            abs(bounds.links.l1 - bounds.links.l2),
            bounds.singularity.deadzone_r_min,
        )
        self._r_max: Final[float] = bounds.links.l1 + bounds.links.l2

    def is_in_workspace(
        self,
        point: Point3D,
    ) -> tuple[bool, str]:
        '''
            Checks whether coordinates lie within the physical annular workspace and Z limits.

            :param point: Target Cartesian 3D spatial coordinate in mm.
            :return: Tuple of (is_in_bounds, error_or_warning_message).
            :exceptions: None.
        '''
        x: float = point.x
        y: float = point.y
        z: float = point.z
        r: float = hypot(x, y)

        if r > self._r_max + self._EPSILON:
            return (
                False,
                f'Point ({x:.1f}, {y:.1f}) exceeds maximum reach '
                f'R_max={self._r_max:.1f} mm (r={r:.1f} mm)'
            )

        if r < self._r_min - self._EPSILON:
            return (
                False,
                f'Point ({x:.1f}, {y:.1f}) is inside deadzone '
                f'R_min={self._r_min:.1f} mm (r={r:.1f} mm)'
            )

        if (
            z < self._bounds.vertical.z_min - self._EPSILON
            or z > self._bounds.vertical.z_max + self._EPSILON
        ):
            return (
                False,
                f'Elevation Z={z:.1f} mm is out of range '
                f'[{self._bounds.vertical.z_min:.1f}, {self._bounds.vertical.z_max:.1f}] mm'
            )

        return True, 'Point is within Cartesian workspace'

    def is_joint_reachable(
        self,
        point: Point2D,
        elbow_config: ElbowConfig,
    ) -> tuple[bool, list[str]]:
        '''
            Evaluates if target position can be achieved within physical joint limits.

            :param point: Target Cartesian 2D planar coordinate in mm.
            :param elbow_config: Target kinematic elbow configuration.
            :return: Tuple of (is_reachable, list_of_warning_messages).
            :exceptions: None.
        '''
        elbow_left: bool = elbow_config == ElbowConfig.LEFT
        ik_res: ScaraJoints2D = self._planar.solve_ik_2d(
            point=point, elbow_left=elbow_left
        )

        if not ik_res.reachable:
            return False, ['Mathematically unreachable (cos_q2 > 1.0)']

        theta1: float = ik_res.theta1
        theta2: float = ik_res.theta2

        if (
            theta1 < self._bounds.joints.j1_min_rad
            or theta1 > self._bounds.joints.j1_max_rad
        ):
            return False, [
                f'J1 angle {degrees(theta1):.1f}° exceeds limit for {elbow_config.value} elbow'
            ]

        if (
            theta2 < self._bounds.joints.j2_min_rad
            or theta2 > self._bounds.joints.j2_max_rad
        ):
            return False, [
                f'J2 angle {degrees(theta2):.1f}° exceeds limit for {elbow_config.value} elbow'
            ]

        if abs(theta2) < self._bounds.singularity.singularity_theta2_min_rad:
            return False, ['J2 in singularity deadband']

        return True, []

    def get_bounds(self) -> ScaraBounds:
        '''
            Returns the active robot geometry and limits model.

            :return: ScaraBounds instance.
            :exceptions: None.
        '''
        return self._bounds

    def get_version(self) -> str:
        '''
            Returns evaluator component version string representation.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return __version__
