# -*- coding: UTF-8 -*-

'''
Module
    provides_test.py
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
    Unit tests for ConfigProvides container.
'''

from __future__ import annotations

from dataclasses import FrozenInstanceError
from unittest import TestCase, main

from scaralang.core.service.parser.commands.config.accel import AccelParser
from scaralang.core.service.parser.commands.config.elbow import ElbowParser
from scaralang.core.service.parser.commands.config.motor import MotorParser
from scaralang.core.service.parser.commands.config.override import OverrideParser
from scaralang.core.service.parser.commands.config.provides import ConfigProvides
from scaralang.core.service.parser.commands.config.speed import SpeedParser
from scaralang.core.service.parser.commands.config.tool_orient import ToolOrientParser
from scaralang.core.service.parser.commands.config.zone import ZoneParser
from scaralang.core.service.parser.commands.icommand_parser import ICommandParser

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.8'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestConfigProvides(TestCase):
    '''
        Test cases verifying ConfigProvides container properties and immutability.

        It defines:

            :methods:
                | test_provides_encapsulation - Verifies attributes and protocol types.
                | test_immutability - Verifies frozen container raises FrozenInstanceError.
    '''

    def test_provides_encapsulation(self) -> None:
        '''
            Verifies attributes and protocol conformance of provided parsers.
        '''
        accel_parser = AccelParser()
        elbow_parser = ElbowParser()
        motor_parser = MotorParser()
        override_parser = OverrideParser()
        speed_parser = SpeedParser()
        tool_orient_parser = ToolOrientParser()
        zone_parser = ZoneParser()
        provides = ConfigProvides(
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
        self.assertIs(provides.accel_parser, accel_parser)
        self.assertIs(provides.elbow_parser, elbow_parser)
        self.assertIs(provides.motor_parser, motor_parser)
        self.assertIs(provides.override_parser, override_parser)
        self.assertIs(provides.speed_parser, speed_parser)
        self.assertIs(provides.tool_orient_parser, tool_orient_parser)
        self.assertIs(provides.zone_parser, zone_parser)
        self.assertEqual(len(provides.parsers), 7)
        for parser in provides.parsers:
            self.assertIsInstance(parser, ICommandParser)

    def test_immutability(self) -> None:
        '''
            Verifies container immutability on attribute reassignment.
        '''
        accel_parser = AccelParser()
        elbow_parser = ElbowParser()
        motor_parser = MotorParser()
        override_parser = OverrideParser()
        speed_parser = SpeedParser()
        tool_orient_parser = ToolOrientParser()
        zone_parser = ZoneParser()
        provides = ConfigProvides(
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
        with self.assertRaises(FrozenInstanceError):
            setattr(provides, 'accel_parser', accel_parser)


if __name__ == '__main__':
    main()
