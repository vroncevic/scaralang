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
    Unit tests for ToolProvides container.
'''

from __future__ import annotations

from dataclasses import FrozenInstanceError
from unittest import TestCase, main

from scaralang.core.service.parser.commands.icommand_parser import ICommandParser
from scaralang.core.service.parser.commands.tool.provides import ToolProvides
from scaralang.core.service.parser.commands.tool.pump import PumpParser
from scaralang.core.service.parser.commands.tool.tool import ToolParser
from scaralang.core.service.parser.commands.tool.valve import ValveParser

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.8'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestToolProvides(TestCase):
    '''
        Test cases verifying ToolProvides container properties and immutability.

        It defines:

            :methods:
                | test_provides_encapsulation - Verifies attributes and protocol types.
                | test_immutability - Verifies frozen container raises FrozenInstanceError.
    '''

    def test_provides_encapsulation(self) -> None:
        '''
            Verifies attributes and protocol conformance of provided parsers.
        '''
        pump_parser = PumpParser()
        tool_parser = ToolParser()
        valve_parser = ValveParser()
        provides = ToolProvides(
            pump_parser=pump_parser,
            tool_parser=tool_parser,
            valve_parser=valve_parser,
            parsers=(pump_parser, tool_parser, valve_parser),
        )
        self.assertIs(provides.pump_parser, pump_parser)
        self.assertIs(provides.tool_parser, tool_parser)
        self.assertIs(provides.valve_parser, valve_parser)
        self.assertEqual(len(provides.parsers), 3)
        for parser in provides.parsers:
            self.assertIsInstance(parser, ICommandParser)

    def test_immutability(self) -> None:
        '''
            Verifies container immutability on attribute reassignment.
        '''
        pump_parser = PumpParser()
        tool_parser = ToolParser()
        valve_parser = ValveParser()
        provides = ToolProvides(
            pump_parser=pump_parser,
            tool_parser=tool_parser,
            valve_parser=valve_parser,
            parsers=(pump_parser, tool_parser, valve_parser),
        )
        with self.assertRaises(FrozenInstanceError):
            setattr(provides, 'pump_parser', pump_parser)


if __name__ == '__main__':
    main()
