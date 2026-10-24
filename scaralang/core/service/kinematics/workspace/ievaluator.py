# -*- coding: UTF-8 -*-

'''
Module
    ievaluator.py
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
    Defines structural protocol IWorkspaceBoundsEvaluator for manipulator workspace and reachability checks.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from scaralang.core.model.kinematics.solver.elbow import ElbowConfig
from scaralang.core.model.kinematics.pose.point_2d import Point2D
from scaralang.core.model.kinematics.pose.point_3d import Point3D
from scaralang.core.model.kinematics.profile.bounds import ScaraBounds

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IWorkspaceBoundsEvaluator(Protocol):
    '''
        Structural protocol defining workspace envelope and joint limit evaluation.

        It defines:

            :methods:
                | is_in_workspace - Checks whether coordinates fall within annular envelope.
                | is_joint_reachable - Evaluates if position is reachable within joint limits.
                | get_bounds - Returns the active robot geometry and limits model.
                | get_version - Returns evaluator component version string.
    '''

    def is_in_workspace(
        self,
        point: Point3D,
    ) -> tuple[bool, str]:
        '''
            Checks whether coordinates lie within the physical annular workspace and Z limits.

            :param point: Target Cartesian 3D spatial coordinate in mm.
            :return: Tuple of (is_in_bounds, error_or_warning_message).
        '''

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
        '''

    def get_bounds(self) -> ScaraBounds:
        '''
            Returns the active robot geometry and limits model.

            :return: ScaraBounds instance.
        '''

    def get_version(self) -> str:
        '''
            Returns evaluator component version string representation.

            :return: Semantic version string.
        '''
