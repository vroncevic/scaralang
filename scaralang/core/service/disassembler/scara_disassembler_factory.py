# -*- coding: UTF-8 -*-

'''
Module
    scara_disassembler_factory.py
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
    Factory service constructing ScaraDisassembler instances.
'''

from __future__ import annotations

from scaralang.core.service.disassembler.iframe_detail_decoder import IFrameDetailDecoder
from scaralang.core.service.disassembler.iscara_disassembler import IScaraDisassembler
from scaralang.core.service.disassembler.scara_disassembler import ScaraDisassembler
from scaralang.core.service.protocol.ibinary_frame_parser import IBinaryFrameParser

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ScaraDisassemblerFactory:
    '''
        Factory service constructing ScaraDisassembler instances.

        It defines:

            :methods:
                | create - Constructs and returns an IScaraDisassembler instance.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(
        cls,
        *,
        parser: IBinaryFrameParser,
        detail_decoder: IFrameDetailDecoder
    ) -> IScaraDisassembler:
        '''
            Constructs and returns an IScaraDisassembler instance.

            :param parser: Frame parsing protocol strategy.
            :param detail_decoder: Frame detail decoder strategy.
            :return: Fully wired IScaraDisassembler instance.
        '''
        return ScaraDisassembler(parser=parser, detail_decoder=detail_decoder)

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns factory version string.

            :return: Version string representation.
        '''
        return __version__
