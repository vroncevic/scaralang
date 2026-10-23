# -*- coding: UTF-8 -*-

'''
Module
    planner.py
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
    Implementation of arm elbow configuration transition trajectory planner.
'''

from __future__ import annotations

from typing import ClassVar, Final

from scaralang.core.model.exceptions.kinematics import ScaraKinematicsError
from scaralang.core.model.kinematics.solver.elbow import ElbowConfig
from scaralang.core.model.kinematics.pose.point_2d import Point2D
from scaralang.core.model.kinematics.profile.bounds import ScaraBounds
from scaralang.core.model.kinematics.solver.solution_2d import ScaraJoints2D
from scaralang.core.model.trajectory.plan.reconfiguration import ReconfigurationRequest
from scaralang.core.model.trajectory.plan.waypoint import Waypoint
from scaralang.core.service.kinematics.solver.analytical.planar.isolver import IPlanarKinematicsSolver
from scaralang.core.service.kinematics.workspace.ievaluator import IWorkspaceBoundsEvaluator
from scaralang.core.service.trajectory.reconfiguration.dependencies import ReconfigurationDependencies

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ElbowReconfigurationPlanner:
    '''
        Defines class ElbowReconfigurationPlanner implementing IElbowReconfigurationPlanner contract structurally.
        Plans safe transition waypoints for SCARA arm elbow configuration switching.

        It defines:

            :attributes:
                | HALF_FACTOR - Divisor factor for midpoint computation.
                | SINGULARITY_J2_RAD - Elbow joint angle at boundary singularity in radians.
                | RETRACT_SUFFIX - Waypoint name suffix for retraction phase.
                | ALIGN_SUFFIX - Waypoint name suffix for alignment phase.
                | TRANSIT_NAME - Waypoint name for intermediate singularity transit.
                | CMD_RETRACT - Command tag for vertical retraction.
                | CMD_TRANSIT - Command tag for singularity transit.
                | CMD_ALIGN - Command tag for safe-height alignment.
                | _planar - Injected planar kinematics solver.
                | _workspace - Injected workspace bounds and reachability evaluator.
            :methods:
                | __init__ - Initializes ElbowReconfigurationPlanner constructor.
                | is_reconfiguration_required - Checks if elbow reconfiguration is needed.
                | plan_reconfiguration - Generates safe intermediate transition waypoints.
                | get_version - Returns planner component version string.
    '''

    HALF_FACTOR: ClassVar[float] = 2.0
    SINGULARITY_J2_RAD: ClassVar[float] = 0.0
    RETRACT_SUFFIX: ClassVar[str] = '_RETRACT'
    ALIGN_SUFFIX: ClassVar[str] = '_ALIGN'
    TRANSIT_NAME: ClassVar[str] = 'RECONFIG_TRANSIT'
    CMD_RETRACT: ClassVar[str] = 'RECONFIG_RETRACT'
    CMD_TRANSIT: ClassVar[str] = 'RECONFIG_TRANSIT'
    CMD_ALIGN: ClassVar[str] = 'RECONFIG_ALIGN'

    _planar: IPlanarKinematicsSolver
    _workspace: IWorkspaceBoundsEvaluator

    def __init__(self, dependencies: ReconfigurationDependencies) -> None:
        '''
            Initializes elbow reconfiguration planner with injected dependencies bundle.

            :param dependencies: Injected ReconfigurationDependencies container bundle.
            :exceptions: None.
        '''
        self._planar: Final[IPlanarKinematicsSolver] = dependencies.planar
        self._workspace: Final[IWorkspaceBoundsEvaluator] = dependencies.workspace

    def is_reconfiguration_required(
        self,
        from_elbow: ElbowConfig,
        to_elbow: ElbowConfig,
    ) -> bool:
        '''
            Determines whether a transition between two elbow configurations is required.

            :param from_elbow: Current arm kinematic elbow configuration.
            :param to_elbow: Target arm kinematic elbow configuration.
            :return: True if configurations differ and reconfiguration is needed, False otherwise.
            :exceptions: None.
        '''
        return from_elbow != to_elbow

    def plan_reconfiguration(
        self,
        request: ReconfigurationRequest,
    ) -> list[Waypoint]:
        '''
            Plans intermediate waypoints to safely reconfigure robot elbow from one pose to another.

            :param request: ReconfigurationRequest parameter bundle containing transition parameters.
            :return: Ordered list of intermediate transition waypoints leading to target pose.
            :exceptions:
                | ScaraKinematicsError: If waypoints or transition poses violate kinematic limits.
        '''
        if not self.is_reconfiguration_required(request.from_elbow, request.to_elbow):
            return []

        bounds: ScaraBounds = self._workspace.get_bounds()
        safe_z: float = max(
            request.z_safe, request.from_waypoint.z, request.to_waypoint.z
        )
        if safe_z < bounds.vertical.z_min or safe_z > bounds.vertical.z_max:
            raise ScaraKinematicsError(
                f'Safe height {safe_z} mm exceeds vertical bounds '
                f'[{bounds.vertical.z_min}, {bounds.vertical.z_max}] mm'
            )

        start_pt: Point2D = Point2D(
            x=request.from_waypoint.x, y=request.from_waypoint.y
        )
        target_pt: Point2D = Point2D(
            x=request.to_waypoint.x, y=request.to_waypoint.y
        )

        reach_a, _ = self._workspace.is_joint_reachable(start_pt, request.from_elbow)
        if not reach_a:
            raise ScaraKinematicsError(
                f'Start waypoint {request.from_waypoint.name} unreachable with '
                f'{request.from_elbow.value} elbow'
            )

        reach_b, _ = self._workspace.is_joint_reachable(target_pt, request.to_elbow)
        if not reach_b:
            raise ScaraKinematicsError(
                f'Target waypoint {request.to_waypoint.name} unreachable with '
                f'{request.to_elbow.value} elbow'
            )

        joints_a: ScaraJoints2D = self._planar.solve_ik_2d(
            start_pt, elbow_left=(request.from_elbow == ElbowConfig.LEFT)
        )
        joints_b: ScaraJoints2D = self._planar.solve_ik_2d(
            target_pt, elbow_left=(request.to_elbow == ElbowConfig.LEFT)
        )

        mid_pt: Point2D = self._planar.solve_fk_2d(
            theta1=(joints_a.theta1 + joints_b.theta1) / self.HALF_FACTOR,
            theta2=self.SINGULARITY_J2_RAD,
        )

        return [
            Waypoint(
                x=request.from_waypoint.x,
                y=request.from_waypoint.y,
                z=safe_z,
                phi=request.from_waypoint.phi,
                speed=request.from_waypoint.speed,
                name=f'{request.from_waypoint.name}{self.RETRACT_SUFFIX}',
                command=self.CMD_RETRACT,
            ),
            Waypoint(
                x=mid_pt.x,
                y=mid_pt.y,
                z=safe_z,
                phi=(request.from_waypoint.phi + request.to_waypoint.phi) / self.HALF_FACTOR,
                speed=request.to_waypoint.speed,
                name=self.TRANSIT_NAME,
                command=self.CMD_TRANSIT,
            ),
            Waypoint(
                x=request.to_waypoint.x,
                y=request.to_waypoint.y,
                z=safe_z,
                phi=request.to_waypoint.phi,
                speed=request.to_waypoint.speed,
                name=f'{request.to_waypoint.name}{self.ALIGN_SUFFIX}',
                command=self.CMD_ALIGN,
            ),
        ]

    def get_version(self) -> str:
        '''
            Returns planner component version string representation.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return __version__
