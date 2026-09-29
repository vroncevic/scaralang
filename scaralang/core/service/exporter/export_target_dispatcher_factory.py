# -*- coding: UTF-8 -*-

'''
Module
    export_target_dispatcher_factory.py
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
    Factory instantiating and wiring ExportTargetDispatcher instances.
'''

from __future__ import annotations

from scaralang.core.service.exporter.csv.csv_trajectory_exporter_factory import CsvTrajectoryExporterFactory
from scaralang.core.service.exporter.export_dispatcher_bundle import ExportDispatcherBundle
from scaralang.core.service.exporter.export_target_dispatcher import ExportTargetDispatcher
from scaralang.core.service.exporter.gcode.gcode_exporter_factory import GCodeExporterFactory
from scaralang.core.service.exporter.iexport_target_dispatcher import IExportTargetDispatcher
from scaralang.core.service.exporter.json.json_trajectory_exporter_factory import JsonTrajectoryExporterFactory
from scaralang.core.service.exporter.scara.scara_plan_exporter_factory import ScaraPlanExporterFactory
from scaralang.core.service.exporter.svg.svg_trajectory_exporter_factory import SvgTrajectoryExporterFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ExportTargetDispatcherFactory:
    '''
        Factory providing wired IExportTargetDispatcher instances.

        It defines:

            :methods:
                | create - Builds ExportTargetDispatcher with injected format exporter bundle.
                | create_default - Builds ExportTargetDispatcher with default sub-exporters.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(cls, *, bundle: ExportDispatcherBundle) -> IExportTargetDispatcher:
        '''
            Builds and returns an IExportTargetDispatcher protocol instance.

            :param bundle: Injected ExportDispatcherBundle collaborator container.
            :return: Fully wired IExportTargetDispatcher protocol instance.
            :exceptions: None.
        '''
        return ExportTargetDispatcher(bundle=bundle)

    @classmethod
    def create_default(cls) -> IExportTargetDispatcher:
        '''
            Builds and returns an IExportTargetDispatcher with standard format exporters.

            :return: Fully wired IExportTargetDispatcher protocol instance.
            :exceptions: None.
        '''
        bundle = ExportDispatcherBundle(
            gcode_exporter=GCodeExporterFactory.create(),
            csv_exporter=CsvTrajectoryExporterFactory.create(),
            json_exporter=JsonTrajectoryExporterFactory.create(),
            svg_exporter=SvgTrajectoryExporterFactory.create(),
            scara_exporter=ScaraPlanExporterFactory.create(),
        )

        return cls.create(bundle=bundle)

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory version string.

            :return: Factory version string.
            :exceptions: None.
        '''
        return __version__
