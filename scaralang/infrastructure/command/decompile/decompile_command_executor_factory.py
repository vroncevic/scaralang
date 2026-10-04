# -*- coding: UTF-8 -*-

'''
Module
    decompile_command_executor_factory.py
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
    Factory instantiating DecompileCommandExecutor instances.
'''

from __future__ import annotations

from scaralang.core.service.decompiler.iscara_decompiler import IScaraDecompiler
from scaralang.core.service.decompiler.scara_decompiler_factory import ScaraDecompilerFactory
from scaralang.infrastructure.command.decompile.decompile_command_definition import DecompileCommandDefinition
from scaralang.infrastructure.command.decompile.decompile_command_executor import DecompileCommandExecutor
from scaralang.infrastructure.command.icommand_definition import ICommandDefinition

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DecompileCommandExecutorFactory:
    '''
        Factory providing DecompileCommandExecutor instances.

        It defines:

            :methods:
                | create - Builds DecompileCommandExecutor with injected dependencies.
                | create_default - Builds DecompileCommandExecutor with default dependencies.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(
        cls,
        *,
        definition: ICommandDefinition,
        service: IScaraDecompiler,
    ) -> DecompileCommandExecutor:
        '''
            Builds and returns a DecompileCommandExecutor with strictly injected dependencies.

            :param definition: Required ICommandDefinition protocol instance.
            :param service: Required IScaraDecompiler protocol instance.
            :return: Fully wired DecompileCommandExecutor instance.
            :exceptions: None.
        '''
        return DecompileCommandExecutor(
            definition=definition,
            service=service,
        )

    @classmethod
    def create_default(cls) -> DecompileCommandExecutor:
        '''
            Builds and returns a DecompileCommandExecutor instance with default dependencies.

            :return: Fully wired DecompileCommandExecutor instance.
            :exceptions: None.
        '''
        return DecompileCommandExecutor(
            definition=DecompileCommandDefinition(),
            service=ScaraDecompilerFactory.create_default(),
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory version string.

            :return: Factory version string.
            :exceptions: None.
        '''
        return __version__
