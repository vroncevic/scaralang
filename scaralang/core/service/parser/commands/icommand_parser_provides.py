# -*- coding: UTF-8 -*-

'''
Module
    icommand_parser_provides.py
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
    Protocol defining the domain command parser provides container contract.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from scaralang.core.service.parser.commands.icommand_parser import ICommandParser

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.9'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class ICommandParserProvides(Protocol):
    '''
        Protocol contract for domain provides containers exposing command parsers.

        It defines:

            :properties:
                | parsers - Sequence of all registered domain command parsers.
    '''

    @property
    def parsers(self) -> tuple[ICommandParser, ...]:
        '''
            Gets all registered domain command parsers.

            :return: Tuple of ICommandParser protocol instances.
        '''
