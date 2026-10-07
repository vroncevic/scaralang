# -*- coding: UTF-8 -*-

'''
Module
    disassemble_summary_formatter.py
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
    Defines DisassembleSummaryFormatter rendering binary disassembly summary reports.
'''

from __future__ import annotations

from scaralang.core.model.dsl.binary.disassembly_summary import DisassemblySummary

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.7'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DisassembleSummaryFormatter:
    '''
        Formats binary disassembly summary domain model into human-readable CLI report lines.

        It defines:

            :methods:
                | format_summary - Renders formatted multi-line disassembly summary report.
                | get_version - Returns the component version string.
    '''

    def format_summary(self, *, summary: DisassemblySummary) -> str:
        '''
            Renders formatted multi-line disassembly summary report for CLI presentation.

            :param summary: DisassemblySummary domain model.
            :return: Formatted multi-line summary report string.
            :exceptions: None.
        '''
        summary_lines: list[str] = [
            'Disassembly Summary:',
            f'  Total Bytes Parsed:   {summary.total_bytes} B',
            f'  Total Decoded Frames: {summary.decoded_frames}',
            f'  Motion Frames:        {summary.motion_frames}',
            f'  Tool Commands:        {summary.tool_commands}',
            f'  Wait / Delays:        {summary.wait_delays}',
            f'  System Frames:        {summary.system_frames}',
        ]

        return '\n'.join(summary_lines)

    def get_version(self) -> str:
        '''
            Returns the component version string.

            :return: The version string.
        '''
        return __version__
