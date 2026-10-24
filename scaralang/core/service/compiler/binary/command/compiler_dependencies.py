# -*- coding: UTF-8 -*-

'''
Module
    compiler_dependencies.py
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
    Parameter bundle encapsulating collaborators for CommandCompiler.
'''

from __future__ import annotations

from dataclasses import dataclass

from scaralang.core.service.compiler.binary.command.actuator.ibuilder import IActuatorFrameBuilder
from scaralang.core.service.compiler.binary.command.tokens.iparser import ITokenParser
from scaralang.core.service.compiler.binary.command.tool.ibuilder import IToolFrameBuilder
from scaralang.core.service.protocol.ipacker import IBinaryFramePacker
from scaralang.core.service.protocol.isystem_builder import IBinarySystemFrameBuilder

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(frozen=True, slots=True)
class CommandCompilerDependencies:
    '''
        Encapsulates collaborators injected into CommandCompiler.

        It defines:

            :attributes:
                | frame_builder - System binary frame builder protocol.
                | frame_packer - Binary wire frame packer protocol.
                | tool_frame_builder - Pneumatic tool frame builder protocol.
                | actuator_frame_builder - Actuator mode frame builder protocol.
                | token_parser - Semantic command token parser protocol.
    '''

    frame_builder: IBinarySystemFrameBuilder
    frame_packer: IBinaryFramePacker
    tool_frame_builder: IToolFrameBuilder
    actuator_frame_builder: IActuatorFrameBuilder
    token_parser: ITokenParser
