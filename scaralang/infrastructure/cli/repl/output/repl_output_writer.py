# -*- coding: UTF-8 -*-

'''
Module
    repl_output_writer.py
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
    Concrete implementation of interactive REPL terminal output writer.
'''

from __future__ import annotations

from sys import stdout

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.5'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ReplOutputWriter:
    '''
        Output writer adapter emitting interactive responses to terminal stdout.

        It defines:

            :methods:
                | write - Emits an output text string via sys.stdout stream.
                | get_version - Returns output writer version string.
    '''

    def write(self, text: str) -> None:
        '''
            Emits an output text string via sys.stdout stream.

            :param text: Text string to emit.
            :exceptions: None.
        '''
        stdout.write(f'{text}\n')
        stdout.flush()

    def get_version(self) -> str:
        '''
            Returns output writer component version.

            :return: Version string.
            :exceptions: None.
        '''
        return __version__
