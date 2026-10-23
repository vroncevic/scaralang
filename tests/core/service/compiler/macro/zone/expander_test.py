# -*- coding: UTF-8 -*-

'''
Module
    expander_test.py
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
    Unit tests for ZoneMacroExpander implementation.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.model.dsl.ast.command_type import ScaraCommandType
from scaralang.core.model.dsl.ast.instruction import ScaraInstruction
from scaralang.core.model.dsl.compiler.context import CompilerContext
from scaralang.core.service.compiler.context.factory import CompilerContextFactory
from scaralang.core.service.compiler.macro.zone.expander import ZoneMacroExpander

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestZoneMacroExpander(TestCase):
    '''
        Test cases verifying ZoneMacroExpander behavior.

        It defines:

            :methods:
                | setUp - Prepares ZoneMacroExpander test fixture.
                | test_can_expand - Verifies can_expand matches ZONE_DEF.
                | test_expand_returns_empty_tuple - Verifies expand returns empty tuple.
                | test_get_version - Verifies implementation version string.
    '''

    def setUp(self) -> None:
        '''
            Prepares ZoneMacroExpander test fixture.

            :exceptions: None.
        '''
        self._expander = ZoneMacroExpander()
        self._context: CompilerContext = CompilerContextFactory.create()

    def test_can_expand(self) -> None:
        '''
            Verifies can_expand returns True for ZONE_DEF and False for other commands.

            :exceptions: None.
        '''
        zone_inst = ScaraInstruction(
            command_type=ScaraCommandType.ZONE_DEF,
            line_number=1,
            raw_text='ZONE_DEF WALL BOX X_MIN=10.0 X_MAX=50.0 Y_MIN=-20.0 Y_MAX=30.0',
            parameters={},
        )
        move_inst = ScaraInstruction(
            command_type=ScaraCommandType.MOVE_L,
            line_number=2,
            raw_text='MOVE_L X=10.0 Y=20.0',
            parameters={},
        )
        self.assertTrue(self._expander.can_expand(instruction=zone_inst))
        self.assertFalse(self._expander.can_expand(instruction=move_inst))

    def test_expand_returns_empty_tuple(self) -> None:
        '''
            Verifies expand consumes ZONE_DEF returning empty instruction tuple.

            :exceptions: None.
        '''
        zone_inst = ScaraInstruction(
            command_type=ScaraCommandType.ZONE_DEF,
            line_number=1,
            raw_text='ZONE_DEF WALL BOX X_MIN=10.0 X_MAX=50.0 Y_MIN=-20.0 Y_MAX=30.0',
            parameters={},
        )
        expanded = self._expander.expand(
            instruction=zone_inst, context=self._context
        )
        self.assertEqual(expanded, ())

    def test_get_version(self) -> None:
        '''
            Verifies get_version returns implementation version string.

            :exceptions: None.
        '''
        self.assertEqual(self._expander.get_version(), __version__)


if __name__ == '__main__':
    main()
