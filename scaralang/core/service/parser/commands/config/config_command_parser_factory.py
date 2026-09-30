# -*- coding: UTF-8 -*-

'''
Module
    config_command_parser_factory.py
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
    Factory instantiating configuration command parser handlers.
'''

from __future__ import annotations

from scaralang.core.service.parser.commands.config.accel_config_parser import AccelConfigParser
from scaralang.core.service.parser.commands.config.elbow_config_parser import ElbowConfigParser
from scaralang.core.service.parser.commands.config.motor_config_parser import MotorConfigParser
from scaralang.core.service.parser.commands.config.override_config_parser import OverrideConfigParser
from scaralang.core.service.parser.commands.config.speed_config_parser import SpeedConfigParser
from scaralang.core.service.parser.commands.config.tool_orient_command_parser import ToolOrientCommandParser
from scaralang.core.service.parser.commands.config.zone_command_parser import ZoneCommandParser
from scaralang.core.service.parser.commands.icommand_parser import ICommandParser

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ConfigCommandParserFactory:
    '''
        Factory providing instantiated configuration domain command parsers.

        It defines:

            :methods:
                | create_handlers - Instantiates and returns all configuration command parsers.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create_handlers(cls) -> tuple[ICommandParser, ...]:
        '''
            Builds and returns all configuration command parser handlers.

            :return: Tuple of ICommandParser protocol instances.
            :exceptions: None.
        '''
        return (
            ElbowConfigParser(),
            MotorConfigParser(),
            SpeedConfigParser(),
            AccelConfigParser(),
            OverrideConfigParser(),
            ZoneCommandParser(),
            ToolOrientCommandParser(),
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns factory component version.

            :return: Version string.
        '''
        return __version__
