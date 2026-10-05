# -*- coding: UTF-8 -*-

'''
Module
    executor_factory.py
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
    Factory instantiating InfoCommandExecutor instances.
'''

from __future__ import annotations

from scaralang.core.service.info.iscara_info_provider import IScaraInfoProvider
from scaralang.core.service.info.scara_info_provider_factory import ScaraInfoProviderFactory
from scaralang.infrastructure.command.icommand_definition import ICommandDefinition
from scaralang.infrastructure.command.info.definition import InfoCommandDefinition
from scaralang.infrastructure.command.info.executor import InfoCommandExecutor

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.5'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class InfoCommandExecutorFactory:
    '''
        Factory providing InfoCommandExecutor instances.

        It defines:

            :methods:
                | create - Builds InfoCommandExecutor with injected definition and service.
                | create_default - Builds InfoCommandExecutor with default definition and service.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(
        cls,
        *,
        definition: ICommandDefinition,
        service: IScaraInfoProvider,
    ) -> InfoCommandExecutor:
        '''
            Builds and returns an InfoCommandExecutor with strictly injected definition.

            :param definition: Required ICommandDefinition protocol instance.
            :param service: Required IScaraInfoProvider protocol instance.
            :return: Fully wired InfoCommandExecutor instance.
            :exceptions: None.
        '''
        return InfoCommandExecutor(
            definition=definition,
            service=service,
        )

    @classmethod
    def create_default(cls) -> InfoCommandExecutor:
        '''
            Builds and returns an InfoCommandExecutor instance with default dependencies.

            :return: Fully wired InfoCommandExecutor instance.
            :exceptions: None.
        '''
        return InfoCommandExecutor(
            definition=InfoCommandDefinition(),
            service=ScaraInfoProviderFactory.create_default(),
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory version string.

            :return: Factory version string.
            :exceptions: None.
        '''
        return __version__
