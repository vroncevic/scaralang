# -*- coding: UTF-8 -*-

'''
Module
    calculator.py
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
    Implementation of analytical circular obstacle tangential bypass arc calculation.
'''

from __future__ import annotations

from math import acos, atan2, hypot, pi

from scaralang.core.model.kinematics.point_2d import Point2D
from scaralang.core.model.trajectory.bypass_arc_geometry import BypassArcGeometry

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.8'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TangentArcCalculator:
    '''
        Computes analytical tangential entry, exit, and sweep angles bypassing a circular obstacle.

        It defines:

            :methods:
                | calculate_bypass_arc - Computes tangential entry, exit, and sweep angles.
                | get_version - Returns calculator component version string.
    '''

    def calculate_bypass_arc(
        self,
        start_pt: Point2D,
        end_pt: Point2D,
        safe_radius: float,
    ) -> BypassArcGeometry:
        '''
            Computes tangential entry, exit, and sweep angles around an obstacle circle.

            :param start_pt: Start coordinate Point2D in mm.
            :param end_pt: Target destination coordinate Point2D in mm.
            :param safe_radius: Safe clearance circle radius in mm.
            :return: Calculated BypassArcGeometry value object.
            :exceptions: None.
        '''
        theta_start: float = atan2(start_pt.y, start_pt.x)
        theta_end: float = atan2(end_pt.y, end_pt.x)

        diff: float = (theta_end - theta_start) % (2.0 * pi)

        if diff > pi:
            diff -= 2.0 * pi

        r_start: float = hypot(start_pt.x, start_pt.y)
        r_end: float = hypot(end_pt.x, end_pt.y)

        alpha1: float = (
            acos(min(1.0, safe_radius / r_start))
            if r_start > safe_radius
            else 0.0
        )
        alpha2: float = (
            acos(min(1.0, safe_radius / r_end))
            if r_end > safe_radius
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

        return BypassArcGeometry(
            phi_entry=phi_entry,
            phi_exit=phi_exit,
            step_sign=step_sign,
            arc_sweep=arc_sweep,
            safe_radius=safe_radius,
        )

    def get_version(self) -> str:
        '''
            Returns calculator component version string representation.

            :return: Component semantic version string.
            :exceptions: None.
        '''
        return __version__
