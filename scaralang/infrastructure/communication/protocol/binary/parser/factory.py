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
    Factory instantiating and providing binary frame parser subsystem components.
'''

from __future__ import annotations

from scaralang.infrastructure.communication.protocol.binary.parser.assembler.factory import AssemblerFactory
from scaralang.infrastructure.communication.protocol.binary.parser.assembler.provides import AssemblerProvides
from scaralang.infrastructure.communication.protocol.binary.parser.parser import BinaryFrameParser
from scaralang.infrastructure.communication.protocol.binary.parser.provides import ParserProvides
from scaralang.infrastructure.communication.protocol.binary.parser.unpacker.factory import UnpackerFactory
from scaralang.infrastructure.communication.protocol.binary.parser.unpacker.provides import UnpackerProvides

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.8'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ParserFactory:
    '''
        Factory providing Parser subsystem service instances.

        It defines:

            :methods:
                | create - Constructs and wires ParserProvides container.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(cls) -> ParserProvides:
        '''
            Constructs and wires ParserProvides container.

            :return: Fully configured ParserProvides container.
            :exceptions: None.
        '''
        assembler_provides: AssemblerProvides = AssemblerFactory.create()
        unpacker_provides: UnpackerProvides = UnpackerFactory.create()
        parser = BinaryFrameParser(assembler=assembler_provides.assembler)

        return ParserProvides(
            parser=parser,
            unpacker=unpacker_provides.unpacker,
            assembler=assembler_provides.assembler,
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory version string.

            :return: Factory version string.
            :exceptions: None.
        '''
        return __version__
