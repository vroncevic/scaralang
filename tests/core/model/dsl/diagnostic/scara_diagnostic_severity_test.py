# -*- coding: UTF-8 -*-

'''
Module
    scara_diagnostic_severity_test.py
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
    Unit tests for ScaraDiagnosticSeverity enumeration model.
'''

from __future__ import annotations

from unittest import TestCase, main

from scaralang.core.model.dsl.diagnostic.scara_diagnostic_severity import ScaraDiagnosticSeverity

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ScaraDiagnosticSeverityTest(TestCase):
    '''Unit tests validating ScaraDiagnosticSeverity enumeration members and values.'''

    def test_enumeration_members_count(self) -> None:
        '''Verify total number of defined diagnostic severity levels.'''
        self.assertEqual(len(ScaraDiagnosticSeverity), 3)

    def test_string_representation(self) -> None:
        '''Verify that severity members match expected string representations.'''
        self.assertEqual(ScaraDiagnosticSeverity.ERROR, 'ERROR')
        self.assertEqual(ScaraDiagnosticSeverity.WARNING, 'WARNING')
        self.assertEqual(ScaraDiagnosticSeverity.INFO, 'INFO')

    def test_lookup_by_value(self) -> None:
        '''Verify member lookup from string values.'''
        self.assertIs(
            ScaraDiagnosticSeverity('ERROR'), ScaraDiagnosticSeverity.ERROR
        )
        self.assertIs(
            ScaraDiagnosticSeverity('WARNING'), ScaraDiagnosticSeverity.WARNING
        )
        self.assertIs(
            ScaraDiagnosticSeverity('INFO'), ScaraDiagnosticSeverity.INFO
        )

    def test_invalid_severity_raises_value_error(self) -> None:
        '''Verify that invalid severity level raises ValueError.'''
        with self.assertRaises(ValueError):
            ScaraDiagnosticSeverity('CRITICAL')


if __name__ == '__main__':
    main()
