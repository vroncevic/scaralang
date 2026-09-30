# -*- coding: UTF-8 -*-

'''
Module
    macro_command_parser_factory.py
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
    Factory instantiating macro command parser handlers.
'''

from __future__ import annotations

from scaralang.core.service.parser.commands.icommand_parser import ICommandParser
from scaralang.core.service.parser.commands.macro.jump_command_parser import JumpCommandParser
from scaralang.core.service.parser.commands.macro.pallet_def_command_parser import PalletDefCommandParser
from scaralang.core.service.parser.commands.macro.pallet_move_command_parser import PalletMoveCommandParser

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class MacroCommandParserFactory:
    '''
        Factory providing instantiated macro domain command parsers.

        It defines:

            :methods:
                | create_handlers - Instantiates and returns all macro command parsers.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create_handlers(cls) -> tuple[ICommandParser, ...]:
        '''
            Builds and returns all macro command parser handlers.

            :return: Tuple of ICommandParser protocol instances.
            :exceptions: None.
        '''
        return (
            JumpCommandParser(),
            PalletDefCommandParser(),
            PalletMoveCommandParser(),
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns factory component version.

            :return: Version string.
        '''
        return __version__
