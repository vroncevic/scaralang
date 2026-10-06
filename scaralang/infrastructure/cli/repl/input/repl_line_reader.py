# -*- coding: UTF-8 -*-

'''
Module
    repl_line_reader.py
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
    Concrete implementation of interactive REPL line reader.
'''

from __future__ import annotations

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.6'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ReplLineReader:
    '''
        Line reader adapter reading interactive input from standard terminal input.

        It defines:

            :methods:
                | read_line - Reads a single input line from user terminal.
                | get_version - Returns line reader version string.
    '''

    def read_line(self, *, prompt: str = 'scaralang> ') -> str | None:
        '''
            Reads a single input line from standard terminal input.

            :param prompt: Prompt string to display.
            :return: The input line stripped of trailing newline, or None on EOF.
            :exceptions: None.
        '''
        try:
            raw_input: str = input(prompt)
            return raw_input.strip()

        except (EOFError, KeyboardInterrupt):
            return None

    def get_version(self) -> str:
        '''
            Returns line reader component version.

            :return: Version string.
            :exceptions: None.
        '''
        return __version__
