# -*- coding: UTF-8 -*-

'''
Module
    irepl_line_reader.py
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
    Defines IReplLineReader protocol for reading interactive user input lines.
'''

from __future__ import annotations

from typing import Protocol
from typing import runtime_checkable

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IReplLineReader(Protocol):
    '''
        Protocol for reading user input lines in an interactive REPL session.

        It defines:

            :methods:
                | read_line - Reads a single input line from user or input stream.
    '''

    def read_line(self, *, prompt: str = 'scaralang> ') -> str | None:
        '''
            Reads a single input line from the user.

            :param prompt: Prompt string to display.
            :return: The input line stripped of trailing newline, or None on EOF.
            :exceptions: None.
        '''
