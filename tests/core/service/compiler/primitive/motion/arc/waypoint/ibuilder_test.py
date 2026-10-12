# -*- coding: UTF-8 -*-

'''
Module
    ibuilder_test.py
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
    Unit tests for IArcWaypointBuilder protocol.
'''

from __future__ import annotations

from collections.abc import Sequence
from unittest import TestCase, main

from scaralang.core.model.dsl.compiler.scara_compiler_context import ScaraCompilerContext
from scaralang.core.model.trajectory.arc_point import ArcPoint
from scaralang.core.model.trajectory.waypoint import Waypoint
from scaralang.core.service.compiler.primitive.motion.arc.waypoint.ibuilder import IArcWaypointBuilder

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.8'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DummyArcWaypointBuilder:
    '''
        Dummy class implementing IArcWaypointBuilder for protocol verification.
    '''

    def build_waypoints(
        self,
        *,
        arc_points: Sequence[ArcPoint],
        target_z: float,
        speed: float,
        context: ScaraCompilerContext,
    ) -> tuple[Waypoint, ...]:
        '''
            Dummy implementation of build_waypoints.
        '''
        _ = arc_points
        _ = target_z
        _ = speed
        _ = context
        return ()

    def get_version(self) -> str:
        '''
            Dummy implementation of get_version.
        '''
        return '1.0.0'


class IncompleteArcWaypointBuilder:  # pylint: disable=too-few-public-methods
    '''
        Incomplete dummy class missing build_waypoints method.
    '''

    def get_version(self) -> str:
        '''
            Dummy implementation of get_version.
        '''
        return '1.0.0'


class TestIArcWaypointBuilder(TestCase):
    '''
        Test cases verifying IArcWaypointBuilder protocol.

        It defines:

            :methods:
                | test_runtime_checkable_satisfied - Verifies conforming class satisfies protocol.
                | test_runtime_checkable_not_satisfied - Verifies incomplete class fails check.
    '''

    def test_runtime_checkable_satisfied(self) -> None:
        '''
            Verifies conforming class passes isinstance check.
        '''
        builder = DummyArcWaypointBuilder()
        self.assertIsInstance(builder, IArcWaypointBuilder)

    def test_runtime_checkable_not_satisfied(self) -> None:
        '''
            Verifies non-conforming class fails isinstance check.
        '''
        builder = IncompleteArcWaypointBuilder()
        self.assertNotIsInstance(builder, IArcWaypointBuilder)


if __name__ == '__main__':
    main()
