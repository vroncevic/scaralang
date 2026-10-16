# -*- coding: UTF-8 -*-

'''
Module
    exporter.py
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
    Implementation of trajectory plan exporter converting waypoints into SCARA DSL code.
'''

from __future__ import annotations

from typing import ClassVar, Final

from scaralang.core.model.dsl.ast.command_type import ScaraCommandType
from scaralang.core.model.dsl.ast.instruction_param import ScaraInstructionParam
from scaralang.core.model.dsl.ast.speed_mode import SpeedMode
from scaralang.core.model.dsl.ast.zone_mode import ZoneMode
from scaralang.core.model.kinematics.elbow_config import ElbowConfig
from scaralang.core.model.trajectory.waypoint import Waypoint
from scaralang.core.service.exporter.scara.formatter.factory import ScaraWaypointFormatterFactory
from scaralang.core.service.exporter.scara.formatter.iformatter import IScaraWaypointFormatter
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


class ScaraPlanExporter:
    '''
    Exports active TrajectoryPlan waypoints into clean, readable SCARA DSL source text.

    It defines:

        :attributes:
            | _DEFAULT_RAPID_SPEED - Default rapid transit feedrate.
            | _DEFAULT_WORK_SPEED - Default linear interpolation feedrate.
            | _DEFAULT_ACCEL - Default acceleration limit.
            | _EMPTY_PLAN_COMMENT - Fallback comment string for empty plans.
            | _HEADER_BORDER - Comment separator rule.
            | _HEADER_TITLE - Top-level program comment title.
            | _formatter - Injected waypoint formatter protocol instance.
        :methods:
            | __init__ - Initializes exporter with injected waypoint formatter.
            | format_waypoint - Formats trajectory waypoint into SCARA instruction line.
            | export_scara - Serializes trajectory plan into formatted .scara source code.
            | export_plan - Backward-compatible plan export contract.
            | get_version - Returns the exporter version string.
    '''

    _DEFAULT_RAPID_SPEED: ClassVar[float] = 100.0
    _DEFAULT_WORK_SPEED: ClassVar[float] = 40.0
    _DEFAULT_ACCEL: ClassVar[float] = 500.0

    _EMPTY_PLAN_COMMENT: ClassVar[str] = (
        '# SCARA DSL Program\n# Empty trajectory plan\n'
    )
    _HEADER_BORDER: ClassVar[str] = (
        '# =========================================================='
    )
    _HEADER_TITLE: ClassVar[str] = '# SCARA DSL Program'

    _formatter: IScaraWaypointFormatter

    def __init__(
        self,
        *,
        formatter: IScaraWaypointFormatter | None = None,
    ) -> None:
        '''
        Initializes ScaraPlanExporter with optional waypoint formatter.

        :param formatter: Injected IScaraWaypointFormatter protocol instance.
        :exceptions: None.
        '''
        self._formatter: Final[IScaraWaypointFormatter] = (
            formatter
            if formatter is not None
            else ScaraWaypointFormatterFactory.create()
        )

    def format_waypoint(
        self, *, waypoint: Waypoint, is_initial: bool = False
    ) -> str:
        '''
        Formats a single trajectory waypoint into a SCARA DSL instruction line.

        :param waypoint: Trajectory Waypoint instance.
        :param is_initial: True if generating the initial joint move, False for linear.
        :return: Formatted SCARA DSL instruction line.
        :exceptions: None.
        '''
        return self._formatter.format_waypoint(
            waypoint=waypoint, is_initial=is_initial
        )

    def export_scara(self, *, plan: ITrajectoryPlan) -> str:
        '''
        Serializes trajectory plan into formatted .scara source code.

        :param plan: Validated ITrajectoryPlan protocol instance.
        :return: Formatted SCARA DSL script.
        :exceptions: None.
        '''
        return self.export_plan(plan=plan)

    def export_plan(self, *, plan: ITrajectoryReadOnly) -> str:
        '''
        Serializes trajectory plan into formatted .scara source code.

        :param plan: Trajectory plan instance.
        :return: Formatted SCARA DSL script.
        :exceptions: None.
        '''
        waypoints: tuple[Waypoint, ...] = plan.waypoints

        if not waypoints:
            return self._EMPTY_PLAN_COMMENT

        work_speed: float = (
            waypoints[0].speed
            if waypoints[0].speed > 0.0
            else self._DEFAULT_WORK_SPEED
        )

        lines: list[str] = [
            self._HEADER_BORDER,
            self._HEADER_TITLE,
            f'# Generated with {len(waypoints)} waypoints',
            self._HEADER_BORDER,
            f'{ScaraCommandType.CONFIG.value} '
            f'{ScaraInstructionParam.ELBOW.value} '
            f'{ElbowConfig.RIGHT.value}',
            f'{ScaraCommandType.SPEED.value} '
            f'{SpeedMode.RAPID.value} {self._DEFAULT_RAPID_SPEED:.1f}',
            f'{ScaraCommandType.SPEED.value} '
            f'{SpeedMode.WORK.value} {work_speed:.1f}',
            f'{ScaraCommandType.ACCEL.value} {self._DEFAULT_ACCEL:.1f}',
            f'{ScaraCommandType.ZONE.value} {ZoneMode.FINE.value}',
            '',
        ]

        initial_motion_found: bool = False
        for wp in waypoints:
            if wp.command:
                lines.append(
                    self._formatter.format_waypoint(waypoint=wp)
                )
            elif not initial_motion_found:
                lines.append(
                    self._formatter.format_waypoint(
                        waypoint=wp, is_initial=True
                    )
                )
                initial_motion_found = True
            else:
                lines.append(
                    self._formatter.format_waypoint(
                        waypoint=wp, is_initial=False
                    )
                )

        lines.append('')
        return '\n'.join(lines)

    def get_version(self) -> str:
        '''
        Returns the exporter version string.

        :return: Semantic version string.
        :exceptions: None.
        '''
        return __version__
