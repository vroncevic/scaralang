# -*- coding: UTF-8 -*-

'''
Module
    dead_zone_bypass_planner.py
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

from math import acos, atan2, ceil, cos, hypot, pi, sin
from typing import Final

from scaralang.core.model.kinematics.point_2d import Point2D
from scaralang.core.model.trajectory.waypoint import Waypoint
from scaralang.core.service.trajectory.avoidance.idead_zone_validator import IDeadZoneValidator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.7'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DeadZoneBypassPlanner:
    '''
        Generates safe tangential detour trajectories bypassing the central dead zone.

        It defines:

            :attributes:
                | _validator - Injected dead zone validation port.
                | _safe_radius - Radius of the bypass arc clearance boundary in mm.
                | _angular_step_rad - Maximum angular resolution for bypass arc in radians.
            :methods:
                | __init__ - Initializes bypass planner with validator and safe radius.
                | plan_bypass - Generates collision-free detour waypoints to destination.
                | get_safe_radius - Returns safe avoidance circle radius in mm.
                | get_version - Returns planner component version string.
    '''

    _validator: IDeadZoneValidator
    _safe_radius: float
    _angular_step_rad: float

    def __init__(
        self,
        *,
        validator: IDeadZoneValidator,
        safety_margin_mm: float = 5.0,
        angular_step_rad: float = pi / 12.0,
    ) -> None:
        '''
            Initializes dead zone bypass planner with validator and safety clearances.

            :param validator: Injected IDeadZoneValidator instance.
            :param safety_margin_mm: Additional clearance margin beyond dead zone in mm.
            :param angular_step_rad: Step size along the bypass arc in radians.
            :exceptions: None.
        '''
        self._validator: Final[IDeadZoneValidator] = validator
        self._safe_radius: Final[float] = (
            validator.get_dead_zone_radius() + max(0.1, safety_margin_mm)
        )
        self._angular_step_rad: Final[float] = max(0.01, angular_step_rad)

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
            return [Waypoint(x=end_pt.x, y=end_pt.y, z=z, speed=speed)]

        theta_start: float = atan2(start_pt.y, start_pt.x)
        theta_end: float = atan2(end_pt.y, end_pt.x)

        diff: float = (theta_end - theta_start) % (2.0 * pi)
        if diff > pi:
            diff -= 2.0 * pi

        r_start: float = hypot(start_pt.x, start_pt.y)
        r_end: float = hypot(end_pt.x, end_pt.y)

        alpha1: float = (
            acos(min(1.0, self._safe_radius / r_start))
            if r_start > self._safe_radius
            else 0.0
        )
        alpha2: float = (
            acos(min(1.0, self._safe_radius / r_end))
            if r_end > self._safe_radius
            else 0.0
        )

        step_sign: float = 1.0 if diff >= 0.0 else -1.0
        phi_entry: float = theta_start + step_sign * alpha1
        phi_exit: float = theta_end - step_sign * alpha2
        arc_sweep: float = (
            (phi_exit - phi_entry) % (2.0 * pi)
            if step_sign > 0.0
            else (phi_entry - phi_exit) % (2.0 * pi)
        )

        num_steps: int = max(1, ceil(arc_sweep / self._angular_step_rad))
        waypoints: list[Waypoint] = []

        for i in range(num_steps + 1):
            t_ratio: float = float(i) / float(num_steps)
            angle: float = phi_entry + step_sign * arc_sweep * t_ratio
            waypoints.append(
                Waypoint(
                    x=self._safe_radius * cos(angle),
                    y=self._safe_radius * sin(angle),
                    z=z,
                    speed=speed,
                )
            )

        waypoints.append(Waypoint(x=end_pt.x, y=end_pt.y, z=z, speed=speed))

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
