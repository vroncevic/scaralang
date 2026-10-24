# -*- coding: UTF-8 -*-

'''
Module
    exporter_test.py
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
    Unit test cases for ScaraExporter dispatching.
'''

from __future__ import annotations

from unittest import TestCase, main

from scaralang.core.model.dsl.exporter.format import ExportFormat
from scaralang.core.model.exceptions.export import ScaraExportError
from scaralang.core.model.trajectory.plan.waypoint import Waypoint
from scaralang.core.service.exporter.csv.factory import CsvExporterFactory
from scaralang.core.service.exporter.dependencies import ExporterDependencies
from scaralang.core.service.exporter.exporter import ScaraExporter
from scaralang.core.service.exporter.gcode.factory import GcodeExporterFactory
from scaralang.core.service.exporter.json.factory import JsonExporterFactory
from scaralang.core.service.exporter.scara.factory import ScaraPlanExporterFactory
from scaralang.core.service.exporter.svg.factory import SvgExporterFactory
from scaralang.core.service.trajectory.plan.plan import TrajectoryPlan

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestScaraExporter(TestCase):
    '''Test suite validating ScaraExporter format routing and error handling.'''

    def setUp(self) -> None:
        '''Initializes exporter with all standard sub-exporters.'''
        deps = ExporterDependencies(
            gcode_exporter=GcodeExporterFactory.create(),
            csv_exporter=CsvExporterFactory.create(),
            json_exporter=JsonExporterFactory.create(),
            svg_exporter=SvgExporterFactory.create(),
            scara_exporter=ScaraPlanExporterFactory.create(),
        )
        self.exporter = ScaraExporter(dependencies=deps)
        wp = Waypoint(
            name='P1',
            x=50.0,
            y=50.0,
            z=10.0,
            phi=0.0,
            speed=50.0,
            command='',
        )
        self.plan = TrajectoryPlan(waypoints=[wp])

    def test_supported_formats(self) -> None:
        '''Verifies all 5 standard export formats are reported as supported.'''
        formats = self.exporter.supported_formats()
        self.assertIn(ExportFormat.GCODE, formats)
        self.assertIn(ExportFormat.CSV, formats)
        self.assertIn(ExportFormat.JSON, formats)
        self.assertIn(ExportFormat.SVG, formats)
        self.assertIn(ExportFormat.SCARA, formats)

    def test_export_gcode(self) -> None:
        '''Verifies routing export to GcodeExporter.'''
        out = self.exporter.export(plan=self.plan, target_format=ExportFormat.GCODE)
        self.assertIn('G21', out)

    def test_export_csv(self) -> None:
        '''Verifies routing export to CsvExporter.'''
        out = self.exporter.export(plan=self.plan, target_format=ExportFormat.CSV)
        self.assertIn('index,name', out)

    def test_export_json(self) -> None:
        '''Verifies routing export to JsonExporter.'''
        out = self.exporter.export(plan=self.plan, target_format=ExportFormat.JSON)
        self.assertIn('waypoint_count', out)

    def test_export_svg(self) -> None:
        '''Verifies routing export to SvgExporter.'''
        out = self.exporter.export(plan=self.plan, target_format=ExportFormat.SVG)
        self.assertIn('<svg', out)

    def test_export_scara(self) -> None:
        '''Verifies routing export to ScaraPlanExporter.'''
        out = self.exporter.export(plan=self.plan, target_format=ExportFormat.SCARA)
        self.assertIn('SCARA DSL Program', out)

    def test_export_unsupported_format(self) -> None:
        '''Verifies unsupported format raises ScaraExportError.'''
        with self.assertRaises(ScaraExportError):
            self.exporter.export(plan=self.plan, target_format='UNSUPPORTED')  # type: ignore[arg-type]

    def test_get_version(self) -> None:
        '''Verifies version reporting.'''
        self.assertIsInstance(self.exporter.get_version(), str)


if __name__ == '__main__':
    main()
