# -*- coding: UTF-8 -*-

'''
Module
    icommand_token_parser.py
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
    Defines structural runtime-checkable protocol ICommandTokenParser.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from scaralang.core.model.dsl.binary.parsed_command_token import ParsedCommandToken

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.6'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class ICommandTokenParser(Protocol):
    '''
        Structural protocol defining contract for waypoint command token parsing.

        It defines:

            :attributes:
                | name - Unique identifier of the command token parser.
            :methods:
                | parse - Parses raw command token string into structured ParsedCommandToken.
    '''

    @property
    def name(self) -> str:
        '''
            Returns the unique component name.

            :return: String component identifier.
        '''

    def parse(self, *, command: str) -> ParsedCommandToken:
        '''
            Parses raw command string token into structured ParsedCommandToken.

            :param command: Raw command token string from waypoint.
            :return: Structured ParsedCommandToken instance.
        '''
