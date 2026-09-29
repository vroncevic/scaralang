# -*- coding: UTF-8 -*-

'''
Module
    gcode_exporter_factory_test.py
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
    Unit tests for GCodeExporterFactory class.
'''

from __future__ import annotations

from unittest import TestCase, main

from scaralang.core.service.exporter.gcode.gcode_exporter_factory import GCodeExporterFactory
from scaralang.core.service.exporter.gcode.igcode_exporter import IGCodeExporter

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestGCodeExporterFactory(TestCase):
    '''
        Test cases verifying GCodeExporterFactory.

        It defines:

            :methods:
                | test_create - Verifies factory returns IGCodeExporter.
                | test_get_version - Verifies factory version string.
    '''

    def test_create(self) -> None:
        '''Verifies factory returns IGCodeExporter instance.'''
        exporter = GCodeExporterFactory.create()
        self.assertIsInstance(exporter, IGCodeExporter)

    def test_get_version(self) -> None:
        '''Verifies factory version returns valid string.'''
        self.assertEqual(GCodeExporterFactory.get_version(), '1.0.1')


if __name__ == '__main__':
    main()
