# -*- coding: UTF-8 -*-

'''
Module
    iprovider_test.py
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
    Unit tests for ICommandParserProvider structural protocol.
'''

from __future__ import annotations

from unittest import TestCase, main

from scaralang.core.service.parser.commands.config.factory import ConfigFactory
from scaralang.core.service.parser.commands.flow.factory import FlowFactory
from scaralang.core.service.parser.commands.frame.factory import FrameFactory
from scaralang.core.service.parser.commands.iprovider import ICommandParserProvider
from scaralang.core.service.parser.commands.macro.factory import MacroFactory
from scaralang.core.service.parser.commands.motion.factory import MotionFactory
from scaralang.core.service.parser.commands.tool.factory import ToolFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ICommandParserProviderTest(TestCase):
    '''
        Tests verifying structural protocol conformance for ICommandParserProvider.

        It defines:

            :methods:
                | test_structural_conformance - Verifies all 6 domain factories satisfy protocol.
                | test_invalid_provider_rejection - Verifies invalid objects are rejected.
    '''

    def test_structural_conformance(self) -> None:
        '''
            Verifies all 6 domain factories satisfy ICommandParserProvider.

            :exceptions: None.
        '''
        factories: tuple[type[object], ...] = (
            MotionFactory,
            MacroFactory,
            FrameFactory,
            ConfigFactory,
            FlowFactory,
            ToolFactory,
        )
        for factory in factories:
            self.assertTrue(
                isinstance(factory, ICommandParserProvider),
                f'{factory.__name__} does not satisfy ICommandParserProvider',
            )

    def test_invalid_provider_rejection(self) -> None:
        '''
            Verifies object lacking required protocol methods is rejected.

            :exceptions: None.
        '''
        self.assertFalse(isinstance(object, ICommandParserProvider))


if __name__ == '__main__':
    main()
