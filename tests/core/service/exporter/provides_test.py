# -*- coding: UTF-8 -*-

'''
Module
    provides_test.py
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
    Unit test cases for ExporterProvides dataclass.
'''

from __future__ import annotations

from dataclasses import FrozenInstanceError
from unittest import TestCase

from scaralang.core.service.exporter.csv.factory import CsvExporterFactory
from scaralang.core.service.exporter.dependencies import ExporterDependencies
from scaralang.core.service.exporter.exporter import ScaraExporter
from scaralang.core.service.exporter.gcode.factory import GcodeExporterFactory
from scaralang.core.service.exporter.json.factory import JsonExporterFactory
from scaralang.core.service.exporter.provides import ExporterProvides
from scaralang.core.service.exporter.scara.factory import ScaraPlanExporterFactory
from scaralang.core.service.exporter.svg.factory import SvgExporterFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.9'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestExporterProvides(TestCase):
    '''Test suite validating ExporterProvides attributes and immutability.'''

    def test_instantiation_and_access(self) -> None:
        '''Verifies attributes are correctly assigned and accessible.'''
        deps = ExporterDependencies(
            gcode_exporter=GcodeExporterFactory.create(),
            csv_exporter=CsvExporterFactory.create(),
            json_exporter=JsonExporterFactory.create(),
            svg_exporter=SvgExporterFactory.create(),
            scara_exporter=ScaraPlanExporterFactory.create(),
        )
        exporter = ScaraExporter(dependencies=deps)
        provides = ExporterProvides(exporter=exporter)
        self.assertIs(provides.exporter, exporter)

    def test_immutability(self) -> None:
        '''Verifies frozen dataclass raises error when mutated.'''
        deps = ExporterDependencies(
            gcode_exporter=GcodeExporterFactory.create(),
            csv_exporter=CsvExporterFactory.create(),
            json_exporter=JsonExporterFactory.create(),
            svg_exporter=SvgExporterFactory.create(),
            scara_exporter=ScaraPlanExporterFactory.create(),
        )
        exporter = ScaraExporter(dependencies=deps)
        provides = ExporterProvides(exporter=exporter)
        with self.assertRaises(FrozenInstanceError):
            provides.exporter = exporter  # type: ignore[misc]
