# -*- coding: UTF-8 -*-

'''
Module
    ireconfiguration_planner.py
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
    Defines structural protocol IElbowReconfigurationPlanner for arm configuration transitions.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from scaralang.core.model.kinematics.solver.elbow import ElbowConfig
from scaralang.core.model.trajectory.plan.reconfiguration import ReconfigurationRequest
from scaralang.core.model.trajectory.plan.waypoint import Waypoint

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IElbowReconfigurationPlanner(Protocol):
    '''
        Structural protocol defining arm elbow configuration transition planning.

        It defines:

            :methods:
                | is_reconfiguration_required - Checks if elbow reconfiguration is needed.
                | plan_reconfiguration - Generates safe intermediate transition waypoints.
                | get_version - Returns planner component version string.
    '''

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
        '''

    def plan_reconfiguration(
        self,
        request: ReconfigurationRequest,
    ) -> list[Waypoint]:
        '''
            Plans intermediate waypoints to safely reconfigure robot elbow from one pose to another.

            :param request: ReconfigurationRequest parameter bundle containing transition parameters.
            :return: Ordered list of intermediate transition waypoints leading to target pose.
        '''

    def get_version(self) -> str:
        '''
            Returns planner component version string representation.

            :return: Semantic version string.
        '''
