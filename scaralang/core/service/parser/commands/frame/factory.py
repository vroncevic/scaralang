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
    Factory instantiating and wiring frame command parser components.
'''

from __future__ import annotations

from scaralang.core.service.parser.commands.frame.provides import FrameProvides
from scaralang.core.service.parser.commands.frame.reset import FrameResetParser
from scaralang.core.service.parser.commands.frame.set import FrameSetParser

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.9'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class FrameFactory:
    '''
        Factory providing configured FrameProvides subsystem instances.

        It defines:

            :methods:
                | create - Constructs and wires FrameProvides container.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(cls) -> FrameProvides:
        '''
            Constructs and wires FrameProvides container with command parsers.

            :return: Fully configured FrameProvides container.
            :exceptions: None.
        '''
        reset_parser = FrameResetParser()
        set_parser = FrameSetParser()

        return FrameProvides(
            reset_parser=reset_parser,
            set_parser=set_parser,
            parsers=(reset_parser, set_parser),
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory version string.

            :return: Factory version string.
            :exceptions: None.
        '''
        return __version__
