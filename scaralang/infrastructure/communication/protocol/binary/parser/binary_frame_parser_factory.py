# -*- coding: UTF-8 -*-

'''
Module
    binary_frame_parser_factory.py
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
    Factory instantiating and providing IBinaryFrameParser component.
'''

from __future__ import annotations

from scaralang.core.service.protocol.ibinary_frame_parser import IBinaryFrameParser
from scaralang.infrastructure.communication.protocol.binary.parser.binary_frame_assembler_factory import BinaryFrameAssemblerFactory
from scaralang.infrastructure.communication.protocol.binary.parser.binary_frame_parser import BinaryFrameParser
from scaralang.infrastructure.communication.protocol.binary.parser.ibinary_frame_assembler import IBinaryFrameAssembler

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class BinaryFrameParserFactory:
    '''
        Factory providing IBinaryFrameParser component instantiation.

        It defines:

            :methods:
                | create - Builds and returns a new default IBinaryFrameParser instance.
                | create_default - Builds and returns a new IBinaryFrameParser with default assembler.
                | create_with_assembler - Builds and returns an IBinaryFrameParser with injected assembler.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(cls) -> IBinaryFrameParser:
        '''
            Builds and returns an IBinaryFrameParser instance.

            :return: Instantiated IBinaryFrameParser instance.
            :exceptions: None.
        '''
        return BinaryFrameParser(
            assembler=BinaryFrameAssemblerFactory.create()
        )

    @classmethod
    def create_default(cls) -> IBinaryFrameParser:
        '''
            Builds and returns an IBinaryFrameParser instance with default assembler.

            :return: Instantiated IBinaryFrameParser instance.
            :exceptions: None.
        '''
        return cls.create()

    @classmethod
    def create_with_assembler(
        cls,
        *,
        assembler: IBinaryFrameAssembler,
    ) -> IBinaryFrameParser:
        '''
            Builds and returns an IBinaryFrameParser instance with injected assembler.

            :param assembler: Injected frame assembler collaborator.
            :return: Instantiated IBinaryFrameParser instance.
            :exceptions: None.
        '''
        return BinaryFrameParser(assembler=assembler)

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory version string.

            :return: Factory version string.
            :exceptions: None.
        '''
        return __version__
