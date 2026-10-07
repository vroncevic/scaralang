# -*- coding: UTF-8 -*-

'''
Module
    scara_exporter_test.py
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
    Unit tests for ScaraExporter class.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main
from unittest.mock import MagicMock

from scaralang.core.model.dsl.exporter.export_format import ExportFormat
from scaralang.core.model.exceptions.scara_export_error import ScaraExportError
from scaralang.core.service.exporter.export_dispatcher_bundle import ExportDispatcherBundle
from scaralang.core.service.exporter.iscara_exporter import IScaraExporter
from scaralang.core.service.exporter.scara_exporter import ScaraExporter

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.7'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestScaraExporter(TestCase):
    '''
        Test cases verifying ScaraExporter routing and protocol conformance.

        It defines:

            :methods:
                | setUp - Initializes mock collaborators and ScaraExporter instance.
                | test_export_gcode - Verifies dispatch to GCodeExporter.
                | test_export_csv - Verifies dispatch to CsvTrajectoryExporter.
                | test_export_json - Verifies dispatch to JsonTrajectoryExporter.
                | test_export_svg - Verifies dispatch to SvgTrajectoryExporter.
                | test_export_scara - Verifies dispatch to ScaraPlanExporter.
                | test_export_unsupported_format - Verifies ScaraExportError on invalid format.
                | test_supported_formats - Verifies supported formats query.
                | test_protocol_conformance - Verifies protocol satisfaction.
                | test_get_version - Verifies version string retrieval.
    '''

    def setUp(self) -> None:
        '''Sets up mocks and dispatcher instance.'''
        self.mock_gcode = MagicMock()
        self.mock_csv = MagicMock()
        self.mock_json = MagicMock()
        self.mock_svg = MagicMock()
        self.mock_scara = MagicMock()
        bundle = ExportDispatcherBundle(
            gcode_exporter=self.mock_gcode,
            csv_exporter=self.mock_csv,
            json_exporter=self.mock_json,
            svg_exporter=self.mock_svg,
            scara_exporter=self.mock_scara,
        )
        self.dispatcher = ScaraExporter(bundle=bundle)
        self.mock_plan = MagicMock()

    def test_export_gcode(self) -> None:
        '''Verifies GCODE format routes to gcode exporter.'''
        self.mock_gcode.export_gcode.return_value = 'G00'
        res = self.dispatcher.export(plan=self.mock_plan, target_format=ExportFormat.GCODE)
        self.assertEqual(res, 'G00')
        self.mock_gcode.export_gcode.assert_called_once_with(plan=self.mock_plan)

    def test_export_csv(self) -> None:
        '''Verifies CSV format routes to csv exporter.'''
        self.mock_csv.export_csv.return_value = 'csv'
        res = self.dispatcher.export(plan=self.mock_plan, target_format=ExportFormat.CSV)
        self.assertEqual(res, 'csv')
        self.mock_csv.export_csv.assert_called_once_with(plan=self.mock_plan)

    def test_export_json(self) -> None:
        '''Verifies JSON format routes to json exporter.'''
        self.mock_json.export_json.return_value = '{}'
        res = self.dispatcher.export(plan=self.mock_plan, target_format=ExportFormat.JSON)
        self.assertEqual(res, '{}')
        self.mock_json.export_json.assert_called_once_with(plan=self.mock_plan)

    def test_export_svg(self) -> None:
        '''Verifies SVG format routes to svg exporter.'''
        self.mock_svg.export_svg.return_value = '<svg>'
        res = self.dispatcher.export(plan=self.mock_plan, target_format=ExportFormat.SVG)
        self.assertEqual(res, '<svg>')
        self.mock_svg.export_svg.assert_called_once_with(plan=self.mock_plan)

    def test_export_scara(self) -> None:
        '''Verifies SCARA format routes to scara exporter.'''
        self.mock_scara.export_plan.return_value = 'HOME'
        res = self.dispatcher.export(plan=self.mock_plan, target_format=ExportFormat.SCARA)
        self.assertEqual(res, 'HOME')
        self.mock_scara.export_plan.assert_called_once_with(plan=self.mock_plan)

    def test_supported_formats(self) -> None:
        '''Verifies supported formats returns all expected export formats.'''
        formats = self.dispatcher.supported_formats()
        self.assertEqual(len(formats), 5)
        self.assertIn(ExportFormat.GCODE, formats)
        self.assertIn(ExportFormat.CSV, formats)
        self.assertIn(ExportFormat.JSON, formats)
        self.assertIn(ExportFormat.SVG, formats)
        self.assertIn(ExportFormat.SCARA, formats)

    def test_protocol_conformance(self) -> None:
        '''Verifies ScaraExporter satisfies IScaraExporter.'''
        self.assertIsInstance(self.dispatcher, IScaraExporter)

    def test_export_unsupported_format(self) -> None:
        '''Verifies unsupported target format raises ScaraExportError.'''
        fake_format = MagicMock()
        fake_format.name = 'UNKNOWN'
        with self.assertRaises(ScaraExportError):
            self.dispatcher.export(plan=self.mock_plan, target_format=fake_format)

    def test_get_version(self) -> None:
        '''Verifies version retrieval returns valid semantic version.'''
        self.assertEqual(self.dispatcher.get_version(), '1.0.7')


if __name__ == '__main__':
    main()
