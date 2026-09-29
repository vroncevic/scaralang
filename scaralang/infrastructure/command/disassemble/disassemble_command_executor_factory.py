# -*- coding: UTF-8 -*-

'''
Module
    disassemble_command_executor_factory.py
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
    Factory instantiating DisassembleCommandExecutor instances.
'''

from __future__ import annotations

from scaralang.infrastructure.command.disassemble.disassemble_command_definition import DisassembleCommandDefinition
from scaralang.infrastructure.command.disassemble.disassemble_command_executor import DisassembleCommandExecutor
from scaralang.infrastructure.command.disassemble.format.disassemble_summary_formatter_factory import DisassembleSummaryFormatterFactory
from scaralang.infrastructure.command.disassemble.format.idisassemble_summary_formatter import IDisassembleSummaryFormatter
from scaralang.infrastructure.command.icommand_definition import ICommandDefinition

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DisassembleCommandExecutorFactory:
    '''
        Factory providing DisassembleCommandExecutor instances.

        It defines:

            :methods:
                | create - Builds DisassembleCommandExecutor with injected dependencies.
                | create_default - Builds DisassembleCommandExecutor with default dependencies.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(
        cls,
        *,
        definition: ICommandDefinition,
        summary_formatter: IDisassembleSummaryFormatter,
    ) -> DisassembleCommandExecutor:
        '''
            Builds and returns a DisassembleCommandExecutor with strictly injected dependencies.

            :param definition: Required ICommandDefinition protocol instance.
            :param summary_formatter: Required IDisassembleSummaryFormatter protocol instance.
            :return: Fully wired DisassembleCommandExecutor instance.
            :exceptions: None.
        '''
        return DisassembleCommandExecutor(
            definition=definition,
            summary_formatter=summary_formatter,
        )

    @classmethod
    def create_default(cls) -> DisassembleCommandExecutor:
        '''
            Builds and returns a DisassembleCommandExecutor instance with default dependencies.

            :return: Fully wired DisassembleCommandExecutor instance.
            :exceptions: None.
        '''
        return DisassembleCommandExecutor(
            definition=DisassembleCommandDefinition(),
            summary_formatter=DisassembleSummaryFormatterFactory.create(),
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory version string.

            :return: Factory version string.
            :exceptions: None.
        '''
        return __version__
