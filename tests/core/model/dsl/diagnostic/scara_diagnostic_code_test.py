# -*- coding: UTF-8 -*-

'''
Module
    scara_diagnostic_code_test.py
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
    Unit tests for ScaraDiagnosticCode enumeration.
'''

from __future__ import annotations

from unittest import TestCase, main

from scaralang.core.model.dsl.diagnostic.scara_diagnostic_code import ScaraDiagnosticCode

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ScaraDiagnosticCodeTest(TestCase):
    '''Unit tests validating ScaraDiagnosticCode enumeration values and counts.'''

    def test_members_count(self) -> None:
        '''Verify that exactly 11 diagnostic codes are defined.'''
        self.assertEqual(len(ScaraDiagnosticCode), 11)

    def test_member_string_values(self) -> None:
        '''Verify that members match their exact uppercase string values.'''
        self.assertEqual(ScaraDiagnosticCode.EMPTY_PROGRAM, 'EMPTY_PROGRAM')
        self.assertEqual(ScaraDiagnosticCode.UNCALIBRATED_MOTION, 'UNCALIBRATED_MOTION')
        self.assertEqual(ScaraDiagnosticCode.DUPLICATE_MOTION, 'DUPLICATE_MOTION')
        self.assertEqual(ScaraDiagnosticCode.TOOL_IN_FLYBY, 'TOOL_IN_FLYBY')
        self.assertEqual(ScaraDiagnosticCode.REDUNDANT_TOOL_CMD, 'REDUNDANT_TOOL_CMD')
        self.assertEqual(ScaraDiagnosticCode.PNEUMATIC_CONFLICT, 'PNEUMATIC_CONFLICT')
        self.assertEqual(ScaraDiagnosticCode.INVALID_ZONE_MODE, 'INVALID_ZONE_MODE')
        self.assertEqual(ScaraDiagnosticCode.INVALID_ZONE_RADIUS, 'INVALID_ZONE_RADIUS')
        self.assertEqual(ScaraDiagnosticCode.DEAD_WAIT, 'DEAD_WAIT')
        self.assertEqual(ScaraDiagnosticCode.INVALID_MOTOR_MODE, 'INVALID_MOTOR_MODE')
        self.assertEqual(ScaraDiagnosticCode.REDUNDANT_MOTOR_CONFIG, 'REDUNDANT_MOTOR_CONFIG')

    def test_lookup_by_value(self) -> None:
        '''Verify string lookup returns matching enum instance.'''
        self.assertIs(
            ScaraDiagnosticCode('DEAD_WAIT'),
            ScaraDiagnosticCode.DEAD_WAIT,
        )


if __name__ == '__main__':
    main()
