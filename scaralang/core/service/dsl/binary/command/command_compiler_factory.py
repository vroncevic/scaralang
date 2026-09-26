# -*- coding: UTF-8 -*-

'''
Module
    command_compiler_factory.py
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
    Factory for instantiating ICommandCompiler implementations with pure DI.
'''

from __future__ import annotations

from scaralang.core.service.protocol.ibinary_frame_builder import IBinaryFrameBuilder
from scaralang.core.service.dsl.binary.command.command_compiler import CommandCompiler
from scaralang.core.service.dsl.binary.command.icommand_compiler import ICommandCompiler

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class CommandCompilerFactory:
    '''
        Factory providing creation of ICommandCompiler implementations.

        It defines:

            :methods:
                | create - Creates an ICommandCompiler instance via pure DI.
    '''

    @classmethod
    def create(cls, *, frame_builder: IBinaryFrameBuilder) -> ICommandCompiler:
        '''
            Instantiates CommandCompiler with strictly injected collaborators.

            :param frame_builder: Injected IBinaryFrameBuilder instance.
            :return: Configured ICommandCompiler protocol instance.
            :exceptions: None.
        '''
        return CommandCompiler(frame_builder=frame_builder)
