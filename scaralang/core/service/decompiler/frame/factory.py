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
    Factory providing FrameDecompiler component.
'''

from __future__ import annotations

from scaralang.core.service.decompiler.frame.dependencies import FrameDependencies
from scaralang.core.service.decompiler.frame.frame import FrameDecompiler
from scaralang.core.service.decompiler.frame.provides import FrameProvides

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class FrameFactory:
    '''
        Factory providing FrameDecompiler component.

        It defines:

            :methods:
                | create - Instantiates FrameDecompiler with injected dependencies.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(cls, dependencies: FrameDependencies) -> FrameProvides:
        '''
            Instantiates FrameDecompiler with injected dependencies.

            :param dependencies: Required FrameDependencies bundle.
            :return: Initialized FrameProvides bundle.
            :exceptions: None.
        '''
        return FrameProvides(
            decompiler=FrameDecompiler(
                planar=dependencies.planar,
                transmission=dependencies.transmission,
                motion_unpacker=dependencies.motion_unpacker,
                actuator_unpacker=dependencies.actuator_unpacker,
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
