# -*- coding: UTF-8 -*-

'''
Module
    iexporter.py
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
    Defines structural runtime-checkable protocol IScaraPlanExporter for exporting
    trajectory plans directly into SCARA DSL source text.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from scaralang.core.model.trajectory.waypoint import Waypoint
from scaralang.core.service.trajectory.plan.iplan import ITrajectoryPlan
from scaralang.core.service.trajectory.plan.iread_only import ITrajectoryReadOnly

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.9'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IScaraPlanExporter(Protocol):
    '''
        Structural protocol defining contracts for SCARA DSL source generation from plans.

        It defines:

            :methods:
                | export_scara - Serializes trajectory plan into formatted .scara source code.
                | export_plan - Backward-compatible plan export contract.
                | format_waypoint - Formats trajectory waypoint into SCARA instruction.
                | get_version - Returns the exporter version string representation.
    '''

    def export_scara(self, *, plan: ITrajectoryPlan) -> str:
        '''
            Serializes trajectory plan into formatted .scara source code.

            :param plan: Validated ITrajectoryPlan protocol instance.
            :return: Formatted SCARA DSL script.
        '''

    def export_plan(self, *, plan: ITrajectoryReadOnly) -> str:
        '''
            Serializes trajectory plan into formatted .scara source code.

            :param plan: Trajectory plan instance.
            :return: Formatted SCARA DSL script.
        '''

    def format_waypoint(
        self, *, waypoint: Waypoint, is_initial: bool = False
    ) -> str:
        '''
            Formats a single trajectory waypoint into a SCARA DSL move instruction.

            :param waypoint: Trajectory Waypoint instance.
            :param is_initial: True if generating the initial joint move, False for linear.
            :return: Formatted SCARA DSL instruction line.
        '''

    def get_version(self) -> str:
        '''
            Returns the exporter version string representation.

            :return: Semantic version string.
        '''
