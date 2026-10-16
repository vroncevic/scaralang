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
    Factory instantiating info command subsystem components.
'''

from __future__ import annotations

from scaralang.infrastructure.command.info.definition import InfoCommandDefinition
from scaralang.infrastructure.command.info.executor import InfoCommandExecutor
from scaralang.infrastructure.command.info.provides import InfoProvides
from scaralang.infrastructure.info.factory import DefaultInfoFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.9'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class InfoFactory:
    '''
        Factory providing Info command subsystem instances.

        It defines:

            :methods:
                | create - Constructs and wires InfoProvides container.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(cls) -> InfoProvides:
        '''
            Constructs and wires InfoProvides container with configured collaborators.

            :return: Fully configured InfoProvides container.
            :exceptions: None.
        '''
        definition: InfoCommandDefinition = InfoCommandDefinition()
        executor: InfoCommandExecutor = InfoCommandExecutor(
            definition=definition,
            service=DefaultInfoFactory.create(),
        )

        return InfoProvides(
            executor=executor,
            definition=definition,
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory version string.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return __version__
