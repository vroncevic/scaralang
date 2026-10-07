# -*- coding: UTF-8 -*-

'''
Module
    scara_exporter_factory_test.py
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
    Unit tests for ScaraExporterFactory class.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main
from unittest.mock import MagicMock

from scaralang.core.service.exporter.export_dispatcher_bundle import ExportDispatcherBundle
from scaralang.core.service.exporter.iscara_exporter import IScaraExporter
from scaralang.core.service.exporter.scara_exporter_factory import ScaraExporterFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.7'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestScaraExporterFactory(TestCase):
    '''
        Test cases verifying ScaraExporterFactory.

        It defines:

            :methods:
                | test_create - Verifies factory returns IScaraExporter with bundle.
                | test_create_default - Verifies factory returns default IScaraExporter.
                | test_get_version - Verifies factory version string.
    '''

    def test_create(self) -> None:
        '''Verifies factory returns IScaraExporter instance with bundle.'''
        bundle = ExportDispatcherBundle(
            gcode_exporter=MagicMock(),
            csv_exporter=MagicMock(),
            json_exporter=MagicMock(),
            svg_exporter=MagicMock(),
            scara_exporter=MagicMock(),
        )
        exporter = ScaraExporterFactory.create(bundle=bundle)
        self.assertIsInstance(exporter, IScaraExporter)

    def test_create_default(self) -> None:
        '''Verifies factory returns default IScaraExporter instance.'''
        exporter = ScaraExporterFactory.create_default()
        self.assertIsInstance(exporter, IScaraExporter)

    def test_get_version(self) -> None:
        '''Verifies factory version returns valid string.'''
        self.assertEqual(
            ScaraExporterFactory.get_version(), '1.0.7'
        )


if __name__ == '__main__':
    main()
