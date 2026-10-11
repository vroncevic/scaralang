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
    Factory instantiating and wiring configuration command parser components.
'''

from __future__ import annotations

from scaralang.core.service.parser.commands.config.accel import AccelParser
from scaralang.core.service.parser.commands.config.elbow import ElbowParser
from scaralang.core.service.parser.commands.config.motor import MotorParser
from scaralang.core.service.parser.commands.config.override import OverrideParser
from scaralang.core.service.parser.commands.config.provides import ConfigProvides
from scaralang.core.service.parser.commands.config.speed import SpeedParser
from scaralang.core.service.parser.commands.config.tool_orient import ToolOrientParser
from scaralang.core.service.parser.commands.config.zone import ZoneParser

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.8'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ConfigFactory:
    '''
        Factory providing configured ConfigProvides subsystem instances.

        It defines:

            :methods:
                | create - Constructs and wires ConfigProvides container.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(cls) -> ConfigProvides:
        '''
            Constructs and wires ConfigProvides container with command parsers.

            :return: Fully configured ConfigProvides container.
            :exceptions: None.
        '''
        accel_parser = AccelParser()
        elbow_parser = ElbowParser()
        motor_parser = MotorParser()
        override_parser = OverrideParser()
        speed_parser = SpeedParser()
        tool_orient_parser = ToolOrientParser()
        zone_parser = ZoneParser()
        return ConfigProvides(
            accel_parser=accel_parser,
            elbow_parser=elbow_parser,
            motor_parser=motor_parser,
            override_parser=override_parser,
            speed_parser=speed_parser,
            tool_orient_parser=tool_orient_parser,
            zone_parser=zone_parser,
            parsers=(
                elbow_parser,
                motor_parser,
                speed_parser,
                accel_parser,
                override_parser,
                zone_parser,
                tool_orient_parser,
            ),
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory version string.

            :return: Factory version string.
            :exceptions: None.
        '''
        return __version__
