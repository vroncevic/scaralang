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
    Factory instantiating disassemble command subsystem components.
'''

from __future__ import annotations

from scaralang.core.service.disassembler.summary.factory import SummaryFactory
from scaralang.core.service.disassembler.summary.provides import SummaryProvides
from scaralang.infrastructure.command.disassemble.definition import DisassembleCommandDefinition
from scaralang.infrastructure.command.disassemble.dependencies import DisassembleDependencies
from scaralang.infrastructure.command.disassemble.error.factory import ErrorFactory
from scaralang.infrastructure.command.disassemble.error.provides import ErrorProvides
from scaralang.infrastructure.command.disassemble.executor import DisassembleCommandExecutor
from scaralang.infrastructure.command.disassemble.format.factory import FormatFactory
from scaralang.infrastructure.command.disassemble.format.provides import FormatProvides
from scaralang.infrastructure.command.disassemble.provides import DisassembleProvides
from scaralang.infrastructure.disassembler.factory import DefaultDisassemblerFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DisassembleFactory:
    '''
        Factory providing Disassemble command subsystem instances.

        It defines:

            :methods:
                | create - Constructs and wires DisassembleProvides container.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(cls) -> DisassembleProvides:
        '''
            Constructs and wires DisassembleProvides container with configured collaborators.

            :return: Fully configured DisassembleProvides container.
            :exceptions: None.
        '''
        definition: DisassembleCommandDefinition = DisassembleCommandDefinition()
        format_provides: FormatProvides = FormatFactory.create()
        error_provides: ErrorProvides = ErrorFactory.create()
        summary_provides: SummaryProvides = SummaryFactory.create()
        deps: DisassembleDependencies = DisassembleDependencies(
            service=DefaultDisassemblerFactory.create(),
            summary_formatter=format_provides.formatter,
            error_handler=error_provides.handler,
            summary_calculator=summary_provides.calculator,
        )
        executor: DisassembleCommandExecutor = DisassembleCommandExecutor(
            definition=definition,
            dependencies=deps,
        )

        return DisassembleProvides(
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
