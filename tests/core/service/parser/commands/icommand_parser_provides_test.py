# -*- coding: UTF-8 -*-

'''
Module
    icommand_parser_provides_test.py
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
    Unit tests for ICommandParserProvides structural protocol.
'''

from __future__ import annotations

from unittest import TestCase, main

from scaralang.core.service.parser.commands.config.factory import ConfigFactory
from scaralang.core.service.parser.commands.flow.factory import FlowFactory
from scaralang.core.service.parser.commands.frame.factory import FrameFactory
from scaralang.core.service.parser.commands.icommand_parser_provides import ICommandParserProvides
from scaralang.core.service.parser.commands.macro.factory import MacroFactory
from scaralang.core.service.parser.commands.motion.factory import MotionFactory
from scaralang.core.service.parser.commands.tool.factory import ToolFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.8'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestICommandParserProvides(TestCase):
    '''
        Tests verifying structural protocol conformance for ICommandParserProvides.

        It defines:

            :methods:
                | test_structural_conformance - Verifies all 6 provides containers satisfy protocol.
                | test_invalid_provides_rejection - Verifies invalid objects are rejected.
    '''

    def test_structural_conformance(self) -> None:
        '''
            Verifies all 6 domain provides containers satisfy ICommandParserProvides.
        '''
        containers = (
            ConfigFactory.create(),
            FlowFactory.create(),
            FrameFactory.create(),
            MacroFactory.create(),
            MotionFactory.create(),
            ToolFactory.create(),
        )
        for container in containers:
            self.assertTrue(
                isinstance(container, ICommandParserProvides),
                f'{type(container).__name__} does not satisfy ICommandParserProvides',
            )
            self.assertGreater(len(container.parsers), 0)

    def test_invalid_provides_rejection(self) -> None:
        '''
            Verifies object lacking required protocol property is rejected.
        '''
        class InvalidProvides:  # pylint: disable=too-few-public-methods
            '''Dummy invalid container lacking parsers property.'''

        self.assertFalse(isinstance(InvalidProvides(), ICommandParserProvides))


if __name__ == '__main__':
    main()
