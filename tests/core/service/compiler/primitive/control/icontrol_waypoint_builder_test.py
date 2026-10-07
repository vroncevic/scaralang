# -*- coding: UTF-8 -*-

'''
Module
    icontrol_waypoint_builder_test.py
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
    Unit tests for IControlWaypointBuilder protocol.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.model.dsl.compiler.control_waypoint_descriptor import ControlWaypointDescriptor
from scaralang.core.model.dsl.compiler.scara_compiler_context import ScaraCompilerContext
from scaralang.core.model.trajectory.waypoint import Waypoint
from scaralang.core.service.compiler.primitive.control.icontrol_waypoint_builder import IControlWaypointBuilder

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.7'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DummyControlWaypointBuilder:
    '''
        Dummy class implementing IControlWaypointBuilder for protocol verification.
    '''

    def build_waypoint(
        self,
        *,
        context: ScaraCompilerContext,
        descriptor: ControlWaypointDescriptor,
    ) -> Waypoint:
        '''
            Dummy implementation of build_waypoint.
        '''
        _ = (context, descriptor)
        return Waypoint(x=0.0, y=0.0, z=0.0, phi=0.0, speed=0.0, name='', command='')

    def get_version(self) -> str:
        '''
            Dummy implementation of get_version.
        '''
        return '1.0.7'


class TestIControlWaypointBuilder(TestCase):
    '''
        Test cases verifying IControlWaypointBuilder protocol.

        It defines:

            :methods:
                | test_runtime_checkable_satisfied - Verifies conforming class satisfies protocol.
                | test_runtime_checkable_not_satisfied - Verifies incomplete class fails check.
    '''

    def test_runtime_checkable_satisfied(self) -> None:
        '''
            Verifies conforming class passes isinstance check.
        '''
        builder = DummyControlWaypointBuilder()
        self.assertIsInstance(builder, IControlWaypointBuilder)

    def test_runtime_checkable_not_satisfied(self) -> None:
        '''
            Verifies non-conforming class fails isinstance check.
        '''
        self.assertFalse(isinstance(object(), IControlWaypointBuilder))


if __name__ == '__main__':
    main()
