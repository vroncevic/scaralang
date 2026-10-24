# -*- coding: UTF-8 -*-

'''
Module
    validator.py
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

from typing import ClassVar, Final

from scaralang.core.model.kinematics.solver.elbow import ElbowConfig
from scaralang.core.model.kinematics.pose.point_2d import Point2D
from scaralang.core.model.kinematics.pose.point_3d import Point3D
from scaralang.core.model.trajectory.validation.result import ValidationResult
from scaralang.core.model.trajectory.plan.waypoint import Waypoint
from scaralang.core.service.kinematics.workspace.ievaluator import IWorkspaceBoundsEvaluator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class WaypointValidator:
    '''
        Validates waypoint coordinates against SCARA kinematic envelope and joint limits.

        It defines:

            :attributes:
                | NAME - Canonical component identifier name.
                | NO_ERROR_INDEX - Sentinel index indicating successful validation.
                | UNREACHABLE_KEYWORD - Substring identifying mathematical inverse reach failure.
                | DEFAULT_JOINT_LIMITS_MSG - Fallback error description when joint bounds exceeded.
                | POINT_REACHABLE_MSG - Standard message for reachable point confirmation.
                | name - Identifier name of the waypoint validator.
                | _workspace - Injected workspace bounds evaluator service.
            :methods:
                | __init__ - Initializes validator with workspace evaluator service.
                | validate_point - Validates Waypoint coordinates against reachability rules.
    '''

    NAME: ClassVar[str] = 'waypoint_validator'
    NO_ERROR_INDEX: ClassVar[int] = -1
    UNREACHABLE_KEYWORD: ClassVar[str] = 'Mathematically unreachable'
    DEFAULT_JOINT_LIMITS_MSG: ClassVar[str] = 'Joint limits exceeded'
    POINT_REACHABLE_MSG: ClassVar[str] = 'Point is reachable'

    _workspace: IWorkspaceBoundsEvaluator

    def __init__(self, *, workspace: IWorkspaceBoundsEvaluator) -> None:
        '''
            Initializes waypoint validator using injected workspace bounds evaluator.

            :param workspace: IWorkspaceBoundsEvaluator instance.
            :exceptions: None.
        '''
        self._workspace: Final[IWorkspaceBoundsEvaluator] = workspace

    @property
    def name(self) -> str:
        '''
            Gets the waypoint validator identifier name.

            :return: Validator name string.
        '''
        return self.NAME

    def validate_point(
        self,
        point: Waypoint,
        elbow_config: ElbowConfig,
    ) -> ValidationResult:
        '''
            Validates Waypoint coordinates against annular horizontal reach and vertical bounds.

            :param point: Target Waypoint to validate.
            :param elbow_config: Target kinematic elbow configuration.
            :return: ValidationResult with pass/fail and descriptive reason.
            :exceptions: None.
        '''
        in_workspace, ws_msg = self._workspace.is_in_workspace(
            point=Point3D(x=point.x, y=point.y, z=point.z)
        )

        if not in_workspace:
            return ValidationResult(
                is_valid=False,
                message=ws_msg,
                error_index=self.NO_ERROR_INDEX,
            )

        is_reachable, reasons = self._workspace.is_joint_reachable(
            point=Point2D(x=point.x, y=point.y),
            elbow_config=elbow_config,
        )

        if not is_reachable:
            if reasons and self.UNREACHABLE_KEYWORD in reasons[0]:
                return ValidationResult(
                    is_valid=False,
                    message=f'Point ({point.x:.1f}, {point.y:.1f}) is kinematically unreachable',
                    error_index=self.NO_ERROR_INDEX,
                )

            reason_str: str = (
                ', '.join(reasons) if reasons else self.DEFAULT_JOINT_LIMITS_MSG
            )

            return ValidationResult(
                is_valid=False,
                message=f'Point ({point.x:.1f}, {point.y:.1f}) violates joint limits: {reason_str}',
                error_index=self.NO_ERROR_INDEX,
            )

        return ValidationResult(
            is_valid=True,
            message=self.POINT_REACHABLE_MSG,
            error_index=self.NO_ERROR_INDEX,
        )
