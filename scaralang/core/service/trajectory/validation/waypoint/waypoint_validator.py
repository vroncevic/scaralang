# -*- coding: UTF-8 -*-

'''
Module
    waypoint_validator.py
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
    Validates waypoint reachability and joint boundary constraints for SCARA robot.
'''

from __future__ import annotations

from typing import Final

from scaralang.core.model.kinematics.point_2d import Point2D
from scaralang.core.model.kinematics.point_3d import Point3D
from scaralang.core.model.trajectory.validation_result import ValidationResult
from scaralang.core.model.trajectory.waypoint import Waypoint
from scaralang.core.service.kinematics.ikinematics_service import IKinematicsService

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.6'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class WaypointValidator:
    '''
        Validates waypoint coordinates against SCARA kinematic envelope and joint limits.

        It defines:

            :attributes:
                | name - Identifier name of the waypoint validator.
                | _kinematics - Injected analytical kinematics service.
            :methods:
                | __init__ - Initializes validator with kinematics service.
                | validate_point - Validates Waypoint coordinates against reachability rules.
    '''

    _kinematics: IKinematicsService

    def __init__(self, kinematics: IKinematicsService) -> None:
        '''
            Initializes waypoint validator using injected kinematics service.

            :param kinematics: IKinematicsService instance.
        '''
        self._kinematics: Final[IKinematicsService] = kinematics

    @property
    def name(self) -> str:
        '''
            Gets the waypoint validator identifier name.

            :return: Validator name string.
        '''
        return 'waypoint_validator'

    def validate_point(self, point: Waypoint) -> ValidationResult:
        '''
            Validates Waypoint coordinates against annular horizontal reach and vertical bounds.

            :param point: Target Waypoint to validate.
            :return: ValidationResult with pass/fail and descriptive reason.
        '''
        in_workspace, ws_msg = self._kinematics.is_in_workspace(
            point=Point3D(x=point.x, y=point.y, z=point.z)
        )

        if not in_workspace:
            return ValidationResult(is_valid=False, message=ws_msg, error_index=-1)

        is_reachable, reasons = self._kinematics.is_joint_reachable(
            point=Point2D(x=point.x, y=point.y)
        )

        if not is_reachable:
            if reasons and 'Mathematically unreachable' in reasons[0]:
                return ValidationResult(
                    is_valid=False,
                    message=f'Point ({point.x:.1f}, {point.y:.1f}) is kinematically unreachable',
                    error_index=-1,
                )

            reason_str: str = ', '.join(reasons) if reasons else 'Joint limits exceeded'

            return ValidationResult(
                is_valid=False,
                message=f'Point ({point.x:.1f}, {point.y:.1f}) violates joint limits: {reason_str}',
                error_index=-1,
            )

        return ValidationResult(is_valid=True, message='Point is reachable', error_index=-1)
