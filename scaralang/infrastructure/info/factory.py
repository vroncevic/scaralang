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
    Factory instantiating default IScaraInfoProvider instances for infrastructure.
'''

from __future__ import annotations

from scaralang.core.service.info.factory import InfoFactory
from scaralang.core.service.info.iinfo import IScaraInfoProvider
from scaralang.core.service.info.provides import InfoProvides

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DefaultInfoFactory:
    '''
        Factory providing default IScaraInfoProvider instances for infrastructure.

        It defines:

            :methods:
                | create - Constructs default IScaraInfoProvider instance.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(cls) -> IScaraInfoProvider:
        '''
            Constructs default IScaraInfoProvider instance.

            :return: Configured IScaraInfoProvider service.
            :exceptions: None.
        '''
        provides: InfoProvides = InfoFactory.create()

        return provides.provider

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns factory version string.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return __version__
