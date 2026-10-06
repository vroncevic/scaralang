# -*- coding: UTF-8 -*-

'''
Module
    export_dispatcher_bundle.py
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
    Defines collaborator bundle dataclass for ScaraExporter.
'''

from __future__ import annotations

from dataclasses import dataclass

from scaralang.core.service.exporter.csv.icsv_trajectory_exporter import ICsvTrajectoryExporter
from scaralang.core.service.exporter.gcode.igcode_exporter import IGCodeExporter
from scaralang.core.service.exporter.json.ijson_trajectory_exporter import IJsonTrajectoryExporter
from scaralang.core.service.exporter.scara.iscara_plan_exporter import IScaraPlanExporter
from scaralang.core.service.exporter.svg.isvg_trajectory_exporter import ISvgTrajectoryExporter

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.6'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(frozen=True, slots=True, kw_only=True)
class ExportDispatcherBundle:
    '''
        Bundle containing format exporter collaborators required by ScaraExporter.

        It defines:

            :attributes:
                | gcode_exporter - Injected IGCodeExporter protocol instance.
                | csv_exporter - Injected ICsvTrajectoryExporter protocol instance.
                | json_exporter - Injected IJsonTrajectoryExporter protocol instance.
                | svg_exporter - Injected ISvgTrajectoryExporter protocol instance.
                | scara_exporter - Injected IScaraPlanExporter protocol instance.
            :methods: None.
    '''

    gcode_exporter: IGCodeExporter
    csv_exporter: ICsvTrajectoryExporter
    json_exporter: IJsonTrajectoryExporter
    svg_exporter: ISvgTrajectoryExporter
    scara_exporter: IScaraPlanExporter
