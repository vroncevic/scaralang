# -*- coding: UTF-8 -*-

'''
Module
    disassembled_frame.py
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
    Defines DisassembledFrame domain model representing decoded binary frame telemetry.
'''

from __future__ import annotations

from dataclasses import dataclass

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.6'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(frozen=True, slots=True, kw_only=True)
class DisassembledFrame:
    '''
        Domain model representing decoded binary frame information.

        It defines:

            :attributes:
                | index - Sequential frame index in stream or file.
                | seq_num - Binary protocol sequence counter value.
                | msg_id - Numeric message identifier.
                | msg_name - Symbolic name of the message.
                | detail - Human-readable parameter decomposition.
    '''

    index: int
    seq_num: int
    msg_id: int
    msg_name: str
    detail: str
