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
    Implementation of dead zone avoidance bypass trajectory generator.
'''

from __future__ import annotations

from math import ceil, cos, sin
from typing import ClassVar, Final

from scaralang.core.model.kinematics.pose.point_2d import Point2D
from scaralang.core.model.trajectory.geometry.bypass import BypassArcGeometry
from scaralang.core.model.trajectory.plan.waypoint import Waypoint
from scaralang.core.service.trajectory.avoidance.bypass.arc.icalculator import ITangentArcCalculator
from scaralang.core.service.trajectory.avoidance.bypass.planner.dependencies import PlannerDependencies
from scaralang.core.service.trajectory.avoidance.validation.ivalidator import IDeadZoneValidator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DeadZoneBypassPlanner:
    '''
        Generates safe tangential detour trajectories bypassing the central dead zone.

        It defines:

            :attributes:
                | MIN_SAFETY_MARGIN_MM - Minimum allowed obstacle safety margin in mm.
                | MIN_ANGULAR_STEP_RAD - Minimum allowed angular discretization resolution in radians.
                | MIN_STEPS - Minimum bypass arc step count.
                | STEP_OFFSET - Loop boundary offset for arc endpoint inclusion.
                | DEFAULT_PHI - Default orientation angle in degrees.
                | DEFAULT_NAME - Default waypoint identifier label.
                | DEFAULT_COMMAND - Default waypoint command string.
                | _validator - Injected dead zone validation port.
                | _calculator - Injected obstacle tangent arc calculator port.
                | _safe_radius - Radius of the bypass arc clearance boundary in mm.
                | _angular_step_rad - Maximum angular resolution for bypass arc in radians.
            :methods:
                | __init__ - Initializes bypass planner with injected dependencies bundle.
                | plan_bypass - Generates collision-free detour waypoints to destination.
                | get_safe_radius - Returns safe avoidance circle radius in mm.
                | get_version - Returns planner component version string.
    '''

    MIN_SAFETY_MARGIN_MM: ClassVar[float] = 0.1
    MIN_ANGULAR_STEP_RAD: ClassVar[float] = 0.01
    MIN_STEPS: ClassVar[int] = 1
    STEP_OFFSET: ClassVar[int] = 1
    DEFAULT_PHI: ClassVar[float] = 0.0
    DEFAULT_NAME: ClassVar[str] = ''
    DEFAULT_COMMAND: ClassVar[str] = ''

    _validator: IDeadZoneValidator
    _calculator: ITangentArcCalculator
    _safe_radius: float
    _angular_step_rad: float

    def __init__(self, dependencies: PlannerDependencies) -> None:
        '''
            Initializes dead zone bypass planner with injected dependencies bundle.

            :param dependencies: Injected PlannerDependencies configuration bundle.
            :exceptions: None.
        '''
        self._validator: Final[IDeadZoneValidator] = dependencies.validator
        self._calculator: Final[ITangentArcCalculator] = dependencies.calculator
        self._safe_radius: Final[float] = (
            dependencies.validator.get_dead_zone_radius()
            + max(self.MIN_SAFETY_MARGIN_MM, dependencies.safety_margin_mm)
        )
        self._angular_step_rad: Final[float] = max(
            self.MIN_ANGULAR_STEP_RAD, dependencies.angular_step_rad
        )

    def plan_bypass(
        self,
        start_pt: Point2D,
        end_pt: Point2D,
        *,
        z: float,
        speed: float,
    ) -> list[Waypoint]:
        '''
            Computes a collision-free bypass trajectory sequence around the central dead zone.

            :param start_pt: Start coordinate Point2D in mm.
            :param end_pt: Target destination coordinate Point2D in mm.
            :param z: Z vertical height coordinate in mm.
            :param speed: Feedrate speed in mm/s.
            :return: Ordered list of intermediate detour Waypoints to destination.
            :exceptions: None.
        '''
        if not self._validator.is_segment_crossing_dead_zone(start_pt, end_pt):
            return [
                Waypoint(
                    x=end_pt.x,
                    y=end_pt.y,
                    z=z,
                    phi=self.DEFAULT_PHI,
                    speed=speed,
                    name=self.DEFAULT_NAME,
                    command=self.DEFAULT_COMMAND,
                )
            ]

        arc: BypassArcGeometry = self._calculator.calculate_bypass_arc(
            start_pt=start_pt,
            end_pt=end_pt,
            safe_radius=self._safe_radius,
        )

        num_steps: int = max(self.MIN_STEPS, ceil(arc.arc_sweep / self._angular_step_rad))
        waypoints: list[Waypoint] = []

        for i in range(num_steps + self.STEP_OFFSET):
            t_ratio: float = float(i) / float(num_steps)
            angle: float = arc.phi_entry + arc.step_sign * arc.arc_sweep * t_ratio
            waypoints.append(
                Waypoint(
                    x=arc.safe_radius * cos(angle),
                    y=arc.safe_radius * sin(angle),
                    z=z,
                    phi=self.DEFAULT_PHI,
                    speed=speed,
                    name=self.DEFAULT_NAME,
                    command=self.DEFAULT_COMMAND,
                )
            )

        waypoints.append(
            Waypoint(
                x=end_pt.x,
                y=end_pt.y,
                z=z,
                phi=self.DEFAULT_PHI,
                speed=speed,
                name=self.DEFAULT_NAME,
                command=self.DEFAULT_COMMAND,
            )
        )

        return waypoints

    def get_safe_radius(self) -> float:
        '''
            Returns the safe radial clearance boundary distance in mm.

            :return: Safe avoidance radius in mm.
            :exceptions: None.
        '''
        return self._safe_radius

    def get_version(self) -> str:
        '''
            Returns planner component version string representation.

            :return: Version string representation.
            :exceptions: None.
        '''
        return __version__
