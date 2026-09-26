# -*- coding: UTF-8 -*-

'''
Module
    scara_parser_factory.py
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
    Factory instantiating and wiring ScaraParser with tokenizer and command handlers.
'''

from __future__ import annotations

from collections.abc import Sequence

from scaralang.core.service.dsl.lexer.iscara_lexer import IScaraLexer
from scaralang.core.service.dsl.parser.commands.approach_retract_parser import ApproachRetractParser
from scaralang.core.service.dsl.parser.commands.arc_command_parser import ArcCommandParser
from scaralang.core.service.dsl.parser.commands.config_command_parser import ConfigCommandParser
from scaralang.core.service.dsl.parser.commands.flow_command_parser import FlowCommandParser
from scaralang.core.service.dsl.parser.commands.frame_command_parser import FrameCommandParser
from scaralang.core.service.dsl.parser.commands.jog_command_parser import JogCommandParser
from scaralang.core.service.dsl.parser.commands.jump_command_parser import JumpCommandParser
from scaralang.core.service.dsl.parser.commands.motion_command_parser import MotionCommandParser
from scaralang.core.service.dsl.parser.commands.pallet_command_parser import PalletCommandParser
from scaralang.core.service.dsl.parser.commands.probe_command_parser import ProbeCommandParser
from scaralang.core.service.dsl.parser.commands.tool_command_parser import ToolCommandParser
from scaralang.core.service.dsl.parser.commands.tool_orient_command_parser import ToolOrientCommandParser
from scaralang.core.service.dsl.parser.commands.zone_command_parser import ZoneCommandParser
from scaralang.core.service.dsl.parser.icommand_parser import ICommandParser
from scaralang.core.service.dsl.parser.iscara_parser import IScaraParser
from scaralang.core.service.dsl.parser.scara_parser import ScaraParser
from scaralang.core.service.dsl.ast.program_factory import ProgramFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ScaraParserFactory:
    '''
        Factory providing wired IScaraParser instances.

        It defines:

            :methods:
                | create - Builds and wires ScaraParser with tokenizer and default command handlers.
                | create_with_handlers - Builds ScaraParser with explicit custom command handlers.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(cls, *, lexer: IScaraLexer) -> IScaraParser:
        '''
            Builds and wires ScaraParser with injected tokenizer and default command handlers.

            :param lexer: Injected IScaraLexer instance.
            :return: IScaraParser structural protocol instance.
            :exceptions: None.
        '''
        return ScaraParser(
            lexer=lexer,
            handlers=(
                MotionCommandParser(),
                JumpCommandParser(),
                ArcCommandParser(),
                ApproachRetractParser(),
                ConfigCommandParser(),
                PalletCommandParser(),
                FrameCommandParser(),
                ToolCommandParser(),
                FlowCommandParser(),
                JogCommandParser(),
                ProbeCommandParser(),
                ZoneCommandParser(),
                ToolOrientCommandParser(),
            ),
            program_factory=ProgramFactory(),
        )

    @classmethod
    def create_with_handlers(cls, *, lexer: IScaraLexer, handlers: Sequence[ICommandParser]) -> IScaraParser:
        '''
            Builds and wires ScaraParser with injected tokenizer and explicit custom command handlers.

            :param lexer: Injected IScaraLexer instance.
            :param handlers: Explicit sequence of custom ICommandParser handlers.
            :return: IScaraParser structural protocol instance.
            :exceptions: None.
        '''
        return ScaraParser(lexer=lexer, handlers=handlers, program_factory=ProgramFactory())

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory version string.

            :return: Factory version string.
            :exceptions: None.
        '''
        return __version__
