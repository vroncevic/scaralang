# -*- coding: UTF-8 -*-

'''
Module
    repl_line_reader_factory.py
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
    Factory instantiating ReplLineReader instances.
'''

from __future__ import annotations

from collections.abc import Callable

from scaralang.infrastructure.cli.repl.input.repl_line_reader import ReplLineReader

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ReplLineReaderFactory:
    '''
        Factory providing ReplLineReader instances.

        It defines:

            :methods:
                | create - Builds ReplLineReader with strictly injected reader function.
                | create_default - Builds ReplLineReader with standard input reader.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(
        cls,
        *,
        reader_func: Callable[[str], str],
    ) -> ReplLineReader:
        '''
            Builds and returns a ReplLineReader with strictly injected reader function.

            :param reader_func: Required custom callable taking prompt and returning string.
            :return: Instantiated ReplLineReader instance.
            :exceptions: None.
        '''
        return ReplLineReader(reader_func=reader_func)

    @classmethod
    def create_default(cls) -> ReplLineReader:
        '''
            Builds and returns a ReplLineReader instance with standard input.

            :return: Instantiated ReplLineReader instance.
            :exceptions: None.
        '''
        return ReplLineReader(reader_func=input)

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory version string.

            :return: Factory version string.
            :exceptions: None.
        '''
        return __version__
