# -*- coding: UTF-8 -*-

'''
Module
    disassembly_summary.py
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
    Defines DisassemblySummary pure immutable domain model.
'''

from __future__ import annotations

from dataclasses import dataclass

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.5'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(frozen=True, slots=True, kw_only=True)
class DisassemblySummary:
    '''
        Domain value object encapsulating decoded frame statistics.

        It defines:

            :attributes:
                | total_bytes - Total raw byte count processed from binary input.
                | decoded_frames - Total count of valid decoded binary frames.
                | motion_frames - Count of kinematic motion and step commands.
                | tool_commands - Count of end-effector pump and valve actuations.
                | wait_delays - Count of dwell and delay instructions.
                | system_frames - Count of system state and diagnostic commands.
    '''

    total_bytes: int
    decoded_frames: int
    motion_frames: int
    tool_commands: int
    wait_delays: int
    system_frames: int
