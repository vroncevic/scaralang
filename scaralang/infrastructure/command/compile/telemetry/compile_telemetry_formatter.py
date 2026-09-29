# -*- coding: UTF-8 -*-

'''
Module
    compile_telemetry_formatter.py
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
    Defines CompileTelemetryFormatter rendering binary compilation telemetry reports.
'''

from __future__ import annotations

from scaralang.core.model.dsl.binary.binary_program_telemetry import BinaryProgramTelemetry

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class CompileTelemetryFormatter:
    '''
        Formats binary program execution telemetry into human-readable CLI report lines.

        It defines:

            :methods:
                | format_telemetry - Renders formatted multi-line telemetry report.
    '''

    def format_telemetry(self, *, telemetry: BinaryProgramTelemetry) -> str:
        '''
            Renders formatted multi-line telemetry report for CLI presentation.

            :param telemetry: BinaryProgramTelemetry domain model.
            :return: Formatted multi-line telemetry report string.
            :exceptions: None.
        '''
        telemetry_lines: list[str] = [
            'Compilation Telemetry:',
            f'  Source Instructions: {telemetry.source_instructions}',
            f'  Compiled Steps:      {telemetry.compiled_steps}',
            (
                f'  Estimated Duration:  {telemetry.duration_s:.3f} s '
                f'({telemetry.duration_us} µs)'
            ),
            (
                f'  Axis Peak Steps:     J1={telemetry.peak_j1_steps}, '
                f'J2={telemetry.peak_j2_steps}, Z={telemetry.peak_z_steps}, '
                f'J4={telemetry.peak_j4_steps}'
            ),
            f'  Total Wire Bytes:    {telemetry.total_wire_bytes} B',
        ]

        return '\n'.join(telemetry_lines)
