# -*- coding: UTF-8 -*-

'''
Module
    compile_telemetry_formatter_test.py
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
    Unit tests for CompileTelemetryFormatter.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.model.dsl.binary.axis_peak_steps import AxisPeakSteps
from scaralang.core.model.dsl.binary.binary_program_telemetry import BinaryProgramTelemetry
from scaralang.infrastructure.command.compile.telemetry.compile_telemetry_formatter import CompileTelemetryFormatter
from scaralang.infrastructure.command.compile.telemetry.icompile_telemetry_formatter import ICompileTelemetryFormatter

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestCompileTelemetryFormatter(TestCase):
    '''Test cases verifying CompileTelemetryFormatter formatting functionality.'''

    def setUp(self) -> None:
        '''Initializes formatter instance.'''
        self.formatter = CompileTelemetryFormatter()

    def test_implements_protocol(self) -> None:
        '''Verifies structural protocol compliance.'''
        self.assertIsInstance(self.formatter, ICompileTelemetryFormatter)

    def test_get_version(self) -> None:
        '''Verifies formatter version string retrieval.'''
        self.assertEqual(self.formatter.get_version(), '1.0.3')

    def test_format_telemetry(self) -> None:
        '''Verifies formatting of BinaryProgramTelemetry model.'''
        telemetry = BinaryProgramTelemetry(
            source_instructions=3,
            compiled_steps=12,
            duration_us=450000,
            duration_s=0.450,
            peak_steps=AxisPeakSteps(
                peak_j1_steps=1500,
                peak_j2_steps=900,
                peak_z_steps=200,
                peak_j4_steps=50,
            ),
            total_wire_bytes=240,
        )
        result: str = self.formatter.format_telemetry(telemetry=telemetry)
        self.assertIn('Compilation Telemetry:', result)
        self.assertIn('Source Instructions: 3', result)
        self.assertIn('Compiled Steps:      12', result)
        self.assertIn('Estimated Duration:  0.450 s (450000 µs)', result)
        self.assertIn('Axis Peak Steps:     J1=1500, J2=900, Z=200, J4=50', result)
        self.assertIn('Total Wire Bytes:    240 B', result)


if __name__ == '__main__':
    main()
