# -*- coding: UTF-8 -*-

'''
Module
    itool_waypoint_builder_test.py
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
    Unit tests for IToolWaypointBuilder protocol.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.model.dsl.ast.command_type import ScaraCommandType
from scaralang.core.model.dsl.ast.pneumatic_state import PneumaticState
from scaralang.core.model.dsl.compiler.scara_compiler_context import ScaraCompilerContext
from scaralang.core.model.trajectory.waypoint import Waypoint
from scaralang.core.service.compiler.primitive.tool.itool_waypoint_builder import IToolWaypointBuilder

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DummyToolWaypointBuilder:
    '''
        Dummy class implementing IToolWaypointBuilder for protocol verification.
    '''

    def build_waypoint(
        self,
        *,
        context: ScaraCompilerContext,
        tool_type: ScaraCommandType,
        state: PneumaticState,
    ) -> Waypoint:
        '''
            Dummy implementation of build_waypoint.
        '''
        _ = context
        _ = tool_type
        _ = state
        return Waypoint(x=0.0, y=0.0, z=0.0, phi=0.0, speed=0.0, name='', command='')


class IncompleteToolWaypointBuilder:
    '''
        Incomplete dummy class missing build_waypoint method.
    '''


class TestIToolWaypointBuilder(TestCase):
    '''
        Test cases verifying IToolWaypointBuilder protocol.

        It defines:

            :methods:
                | test_runtime_checkable_satisfied - Verifies conforming class satisfies protocol.
                | test_runtime_checkable_not_satisfied - Verifies incomplete class fails check.
    '''

    def test_runtime_checkable_satisfied(self) -> None:
        '''
            Verifies conforming class passes isinstance check.
        '''
        builder = DummyToolWaypointBuilder()
        self.assertIsInstance(builder, IToolWaypointBuilder)

    def test_runtime_checkable_not_satisfied(self) -> None:
        '''
            Verifies non-conforming class fails isinstance check.
        '''
        builder = IncompleteToolWaypointBuilder()
        self.assertNotIsInstance(builder, IToolWaypointBuilder)


if __name__ == '__main__':
    main()
