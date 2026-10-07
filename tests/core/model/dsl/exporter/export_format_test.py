# -*- coding: UTF-8 -*-

'''
Module
    export_format_test.py
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
    Unit tests for ExportFormat enumeration model.
'''

from __future__ import annotations

from unittest import TestCase, main

from scaralang.core.model.dsl.exporter.export_format import ExportFormat

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.7'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ExportFormatTest(TestCase):
    '''Unit tests validating ExportFormat enumeration members and string values.'''

    def test_enumeration_members_count(self) -> None:
        '''Verify total number of defined export formats.'''
        self.assertEqual(len(ExportFormat), 5)

    def test_string_representation(self) -> None:
        '''Verify that export format members match expected string values.'''
        self.assertEqual(ExportFormat.GCODE, 'GCODE')
        self.assertEqual(ExportFormat.CSV, 'CSV')
        self.assertEqual(ExportFormat.JSON, 'JSON')
        self.assertEqual(ExportFormat.SVG, 'SVG')
        self.assertEqual(ExportFormat.SCARA, 'SCARA')

    def test_lookup_by_value(self) -> None:
        '''Verify member lookup from string values.'''
        self.assertIs(ExportFormat('GCODE'), ExportFormat.GCODE)
        self.assertIs(ExportFormat('CSV'), ExportFormat.CSV)
        self.assertIs(ExportFormat('JSON'), ExportFormat.JSON)
        self.assertIs(ExportFormat('SVG'), ExportFormat.SVG)
        self.assertIs(ExportFormat('SCARA'), ExportFormat.SCARA)


if __name__ == '__main__':
    main()
