# -*- coding: UTF-8 -*-

'''
Module
    export_target_dispatcher.py
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
    Dispatches trajectory export operations to format-specific exporter services.
'''

from __future__ import annotations

from typing import Final

from scaralang.core.model.dsl.exporter.export_format import ExportFormat
from scaralang.core.service.exporter.export_dispatcher_bundle import ExportDispatcherBundle
from scaralang.core.service.exporter.csv.icsv_trajectory_exporter import ICsvTrajectoryExporter
from scaralang.core.service.exporter.gcode.igcode_exporter import IGCodeExporter
from scaralang.core.service.exporter.json.ijson_trajectory_exporter import IJsonTrajectoryExporter
from scaralang.core.service.exporter.scara.iscara_plan_exporter import IScaraPlanExporter
from scaralang.core.service.exporter.svg.isvg_trajectory_exporter import ISvgTrajectoryExporter
from scaralang.core.service.trajectory.plan.itrajectory_plan import ITrajectoryPlan

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ExportTargetDispatcher:
    '''
        Dispatches trajectory plans to target-specific exporters based on format enum.

        It defines:

            :attributes:
                | _gcode_exporter - G-code exporter protocol instance.
                | _csv_exporter - CSV trajectory exporter protocol instance.
                | _json_exporter - JSON trajectory exporter protocol instance.
                | _svg_exporter - SVG vector exporter protocol instance.
                | _scara_exporter - Canonical SCARA DSL exporter protocol instance.
            :methods:
                | __init__ - Initializes dispatcher with injected collaborator bundle.
                | export - Routes trajectory plan to target exporter.
                | supported_formats - Returns collection of supported export format enums.
    '''

    _gcode_exporter: IGCodeExporter
    _csv_exporter: ICsvTrajectoryExporter
    _json_exporter: IJsonTrajectoryExporter
    _svg_exporter: ISvgTrajectoryExporter
    _scara_exporter: IScaraPlanExporter

    def __init__(self, *, bundle: ExportDispatcherBundle) -> None:
        '''
            Initializes ExportTargetDispatcher with format exporter collaborator bundle.

            :param bundle: Injected ExportDispatcherBundle protocol container.
            :exceptions: None.
        '''
        self._gcode_exporter: Final[IGCodeExporter] = bundle.gcode_exporter
        self._csv_exporter: Final[ICsvTrajectoryExporter] = bundle.csv_exporter
        self._json_exporter: Final[IJsonTrajectoryExporter] = bundle.json_exporter
        self._svg_exporter: Final[ISvgTrajectoryExporter] = bundle.svg_exporter
        self._scara_exporter: Final[IScaraPlanExporter] = bundle.scara_exporter

    def supported_formats(self) -> tuple[ExportFormat, ...]:
        '''
            Returns collection of all export formats supported by dispatcher.

            :return: Tuple of supported ExportFormat enum values.
            :exceptions: None.
        '''
        return (
            ExportFormat.GCODE,
            ExportFormat.CSV,
            ExportFormat.JSON,
            ExportFormat.SVG,
            ExportFormat.SCARA,
        )

    def export(
        self, *, plan: ITrajectoryPlan, target_format: ExportFormat
    ) -> str:
        '''
            Serializes trajectory plan into selected target export format string.

            :param plan: Validated ITrajectoryPlan protocol instance.
            :param target_format: Target format enum identifier.
            :return: Formatted export string.
            :exceptions: None.
        '''
        match target_format:
            case ExportFormat.GCODE:
                return self._gcode_exporter.export_gcode(plan=plan)
            case ExportFormat.CSV:
                return self._csv_exporter.export_csv(plan=plan)
            case ExportFormat.JSON:
                return self._json_exporter.export_json(plan=plan)
            case ExportFormat.SVG:
                return self._svg_exporter.export_svg(plan=plan)
            case ExportFormat.SCARA:
                return self._scara_exporter.export_plan(plan=plan)
