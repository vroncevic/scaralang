# -*- coding: UTF-8 -*-

'''
Module
    scara_diagnostic_formatter_test.py
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
    Unit tests for ScaraDiagnosticFormatter.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.model.dsl.diagnostic.scara_diagnostic import ScaraDiagnostic
from scaralang.core.model.dsl.diagnostic.scara_diagnostic_severity import ScaraDiagnosticSeverity
from scaralang.core.service.linter.diagnostic.scara_diagnostic_formatter import ScaraDiagnosticFormatter

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestScaraDiagnosticFormatter(TestCase):
    '''
        Unit tests validating formatting of ScaraDiagnostic reports.

        It defines:

            :methods:
                | setUp - Initializes formatter test fixture.
                | test_format_error - Verifies formatting an ERROR severity diagnostic.
                | test_format_warning - Verifies formatting a WARNING severity diagnostic.
                | test_format_info_without_command - Verifies formatting an INFO diagnostic.
                | test_get_version - Verifies formatter version string.
    '''

    def setUp(self) -> None:
        '''Initializes formatter test fixture.'''
        self.formatter: ScaraDiagnosticFormatter = ScaraDiagnosticFormatter()

    def test_format_error(self) -> None:
        '''
            Verify formatting an ERROR severity diagnostic.
        '''
        diag = ScaraDiagnostic(
            code='ERR01',
            severity=ScaraDiagnosticSeverity.ERROR,
            message='Invalid coordinate syntax',
            line=15,
            command='MOVE_L',
        )
        report = self.formatter.format_report(diagnostic=diag)
        self.assertIn('❌ [ERROR]', report)
        self.assertIn('Line 15:', report)
        self.assertIn('[ERR01]', report)
        self.assertIn('Invalid coordinate syntax', report)

    def test_format_warning(self) -> None:
        '''
            Verify formatting a WARNING severity diagnostic.
        '''
        diag = ScaraDiagnostic(
            code='WARN02',
            severity=ScaraDiagnosticSeverity.WARNING,
            message='Near reach limit',
            line=8,
            command='MOVE_J',
        )
        report = self.formatter.format_report(diagnostic=diag)
        self.assertIn('⚠️ [WARN]', report)
        self.assertIn('Line 8:', report)
        self.assertIn('[WARN02]', report)
        self.assertIn('Near reach limit', report)

    def test_format_info_without_command(self) -> None:
        '''
            Verify formatting an INFO severity diagnostic without command.
        '''
        diag = ScaraDiagnostic(
            code='INFO03',
            severity=ScaraDiagnosticSeverity.INFO,
            message='Optimization note',
            line=1,
            command='',
        )
        report = self.formatter.format_report(diagnostic=diag)
        self.assertIn('ℹ️ [INFO]', report)
        self.assertIn('Line 1:', report)
        self.assertIn('[INFO03]', report)
        self.assertIn('Optimization note', report)

    def test_get_version(self) -> None:
        '''
            Verifies formatter returns correct version string.
        '''
        self.assertEqual(self.formatter.get_version(), '1.0.3')

if __name__ == '__main__':
    main()
