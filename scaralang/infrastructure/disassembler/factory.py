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
    Factory providing default full-stack ScaraDisassembler composition.
'''

from __future__ import annotations

from scaralang.core.service.disassembler.dependencies import DisassemblerDependencies
from scaralang.core.service.disassembler.factory import DisassemblerFactory
from scaralang.core.service.disassembler.frame.dependencies import FrameDependencies
from scaralang.core.service.disassembler.frame.factory import FrameFactory
from scaralang.core.service.disassembler.frame.provides import FrameProvides
from scaralang.core.service.disassembler.idisassembler import IScaraDisassembler
from scaralang.core.service.disassembler.provides import DisassemblerProvides
from scaralang.infrastructure.protocol.parser.factory import ParserFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DefaultDisassemblerFactory:
    '''
        Factory providing default full-stack ScaraDisassembler composition.

        It defines:

            :methods:
                | create - Builds and returns an IScaraDisassembler with standard defaults.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(cls) -> IScaraDisassembler:
        '''
            Builds and returns an IScaraDisassembler with standard defaults.

            :return: Fully configured IScaraDisassembler protocol instance.
            :exceptions: None.
        '''
        parser_provides = ParserFactory.create()
        parser = parser_provides.parser

        frame_provides: FrameProvides = FrameFactory.create(
            dependencies=FrameDependencies(
                motion_unpacker=parser_provides.motion_unpacker,
                actuator_unpacker=parser_provides.actuator_unpacker,
            )
        )
        disassembler_provides: DisassemblerProvides = DisassemblerFactory.create(
            dependencies=DisassemblerDependencies(
                parser=parser,
                detail_decoder=frame_provides.decoder,
            )
        )

        return disassembler_provides.disassembler

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns factory version string representation.

            :return: Factory version string.
            :exceptions: None.
        '''
        return __version__
