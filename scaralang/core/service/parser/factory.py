# -*- coding: UTF-8 -*-

'''
Module
    factory.py
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
    Factory instantiating and wiring ParserProvides output bundle.
'''

from __future__ import annotations

from scaralang.core.service.parser.dependencies import ParserDependencies
from scaralang.core.service.parser.parser import ScaraParser
from scaralang.core.service.parser.provides import ParserProvides

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ParserFactory:
    '''
        Factory providing ParserProvides output bundle.

        It defines:

            :methods:
                | create - Returns a new ParserProvides bundle.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(cls, dependencies: ParserDependencies) -> ParserProvides:
        '''
            Builds and returns a ParserProvides output bundle.

            :param dependencies: Injected ParserDependencies bundle.
            :return: ParserProvides output bundle instance.
            :exceptions: None.
        '''
        return ParserProvides(
            parser=ScaraParser(
                lexer=dependencies.lexer,
                line_splitter=dependencies.line_splitter,
                line_parser=dependencies.line_parser,
            )
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory version string.

            :return: Factory version string.
            :exceptions: None.
        '''
        return __version__
