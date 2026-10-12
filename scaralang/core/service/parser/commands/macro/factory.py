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
    Factory instantiating and wiring macro command parser components.
'''

from __future__ import annotations

from scaralang.core.service.parser.commands.macro.jump import JumpParser
from scaralang.core.service.parser.commands.macro.pallet_def import PalletDefParser
from scaralang.core.service.parser.commands.macro.pallet_move import PalletMoveParser
from scaralang.core.service.parser.commands.macro.provides import MacroProvides

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.8'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class MacroFactory:
    '''
        Factory providing configured MacroProvides subsystem instances.

        It defines:

            :methods:
                | create - Constructs and wires MacroProvides container.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(cls) -> MacroProvides:
        '''
            Constructs and wires MacroProvides container with command parsers.

            :return: Fully configured MacroProvides container.
            :exceptions: None.
        '''
        jump_parser = JumpParser()
        pallet_def_parser = PalletDefParser()
        pallet_move_parser = PalletMoveParser()
        return MacroProvides(
            jump_parser=jump_parser,
            pallet_def_parser=pallet_def_parser,
            pallet_move_parser=pallet_move_parser,
            parsers=(jump_parser, pallet_def_parser, pallet_move_parser),
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory version string.

            :return: Factory version string.
            :exceptions: None.
        '''
        return __version__
