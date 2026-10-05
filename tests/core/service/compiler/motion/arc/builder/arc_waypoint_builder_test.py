# -*- coding: UTF-8 -*-

'''
Module
    arc_waypoint_builder_test.py
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
    Unit tests for ArcWaypointBuilder.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.model.dsl.ast.tool_orient_mode import ToolOrientMode
from scaralang.core.model.dsl.compiler.compiler_pose_state import CompilerPoseState
from scaralang.core.model.dsl.compiler.compiler_speed_state import CompilerSpeedState
from scaralang.core.model.dsl.compiler.scara_compiler_context import ScaraCompilerContext
from scaralang.core.model.kinematics.point_2d import Point2D
from scaralang.core.model.trajectory.arc_point import ArcPoint
from scaralang.core.service.compiler.motion.arc.builder.arc_waypoint_builder import ArcWaypointBuilder
from scaralang.core.service.compiler.motion.arc.builder.iarc_waypoint_builder import IArcWaypointBuilder

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.5'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestArcWaypointBuilder(TestCase):
    '''
        Test cases verifying ArcWaypointBuilder.

        It defines:

            :methods:
                | setUp - Initializes builder and initial context.
                | test_structural_conformance - Verifies protocol check.
                | test_get_version - Verifies get_version returns valid version string.
                | test_build_waypoints_fixed_orientation - Tests waypoints with fixed phi.
                | test_build_waypoints_tangential_orientation - Tests waypoints with tangential phi.
    '''

    def setUp(self) -> None:
        '''
            Prepares builder instance.
        '''
        self.builder = ArcWaypointBuilder()
        self.context = ScaraCompilerContext(
            pose=CompilerPoseState(
                current_x=0.0,
                current_y=0.0,
                current_z=5.0,
                current_phi=45.0,
            ),
            speed=CompilerSpeedState(
                current_speed=60.0,
            ),
            tool_orient_mode=ToolOrientMode.FIXED,
        )

    def test_structural_conformance(self) -> None:
        '''
            Verifies structural conformance to IArcWaypointBuilder.
        '''
        self.assertIsInstance(self.builder, IArcWaypointBuilder)

    def test_get_version(self) -> None:
        '''
            Verifies get_version returns valid version string.
        '''
        self.assertEqual(self.builder.get_version(), '1.0.5')


    def test_build_waypoints_fixed_orientation(self) -> None:
        '''
            Verifies that waypoints inherit current_phi when in fixed orientation mode.
        '''
        arc_points = (
            ArcPoint(point=Point2D(x=10.0, y=20.0), heading_deg=90.0),
            ArcPoint(point=Point2D(x=30.0, y=40.0), heading_deg=180.0),
        )
        waypoints = self.builder.build_waypoints(
            arc_points=arc_points,
            target_z=15.0,
            speed=50.0,
            context=self.context,
        )
        self.assertEqual(len(waypoints), 2)
        self.assertEqual(waypoints[0].x, 10.0)
        self.assertEqual(waypoints[0].y, 20.0)
        self.assertEqual(waypoints[0].z, 15.0)
        self.assertEqual(waypoints[0].phi, 45.0)
        self.assertEqual(waypoints[0].speed, 50.0)

    def test_build_waypoints_tangential_orientation(self) -> None:
        '''
            Verifies that waypoints use tangent angle when in tangential mode.
        '''
        self.context.tool_orient_mode = ToolOrientMode.TANGENTIAL
        arc_points = (
            ArcPoint(point=Point2D(x=10.0, y=20.0), heading_deg=90.0),
            ArcPoint(point=Point2D(x=30.0, y=40.0), heading_deg=180.0),
        )
        waypoints = self.builder.build_waypoints(
            arc_points=arc_points,
            target_z=15.0,
            speed=50.0,
            context=self.context,
        )
        self.assertEqual(len(waypoints), 2)
        self.assertEqual(waypoints[0].phi, 90.0)
        self.assertEqual(waypoints[1].phi, 180.0)


if __name__ == '__main__':
    main()
