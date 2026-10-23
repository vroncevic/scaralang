# -*- coding: UTF-8 -*-

'''
Module
    solver_test.py
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
    Unit tests for PlanarKinematicsSolver calculations.
'''

from __future__ import annotations

from math import pi
from unittest import TestCase
from unittest import main

from scaralang.core.model.kinematics.solver.status import IkStatus
from scaralang.core.model.kinematics.profile.link import LinkDimensions
from scaralang.core.model.kinematics.pose.point_2d import Point2D
from scaralang.core.model.kinematics.solver.solution_2d import ScaraJoints2D
from scaralang.core.service.kinematics.solver.analytical.planar.factory import PlanarKinematicsSolverFactory
from scaralang.core.service.kinematics.solver.analytical.planar.isolver import IPlanarKinematicsSolver

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestPlanarKinematicsSolver(TestCase):
    '''
        Validates PlanarKinematicsSolver analytical calculations.

        It defines:

            :methods:
                | setUp - Sets up link dimensions and initializes solver via factory.
                | test_solve_fk_2d - Verifies forward kinematics point calculations.
                | test_solve_fk_pose_2d - Verifies elbow and tool joint positions.
                | test_solve_ik_2d_roundtrip - Verifies FK(IK(point)) returns original point.
                | test_solve_ik_2d_unreachable - Confirms unreachable status for points outside reach.
                | test_solve_ik_2d_inner_deadzone - Confirms inner deadzone status for points too close.
                | test_solve_ik_2d_negative_quadrant_wrap - Confirms angle normalization below -pi.
                | test_get_version - Verifies component version string.
    '''

    def setUp(self) -> None:
        '''Sets up link dimensions and initializes solver via factory.'''
        links = LinkDimensions(l1=150.0, l2=120.0)
        self.solver: IPlanarKinematicsSolver = PlanarKinematicsSolverFactory.create(links=links)

    def test_solve_fk_2d(self) -> None:
        '''Verifies forward kinematics point calculations.'''
        tool: Point2D = self.solver.solve_fk_2d(0.0, 0.0)
        self.assertAlmostEqual(tool.x, 270.0, places=4)
        self.assertAlmostEqual(tool.y, 0.0, places=4)

        tool_90: Point2D = self.solver.solve_fk_2d(pi / 2.0, 0.0)
        self.assertAlmostEqual(tool_90.x, 0.0, places=4)
        self.assertAlmostEqual(tool_90.y, 270.0, places=4)

    def test_solve_fk_pose_2d(self) -> None:
        '''Verifies elbow and tool joint positions.'''
        elbow, tool = self.solver.solve_fk_pose_2d(0.0, pi / 2.0)
        self.assertAlmostEqual(elbow.x, 150.0, places=4)
        self.assertAlmostEqual(elbow.y, 0.0, places=4)
        self.assertAlmostEqual(tool.x, 150.0, places=4)
        self.assertAlmostEqual(tool.y, 120.0, places=4)

    def test_solve_ik_2d_roundtrip(self) -> None:
        '''Verifies that forward kinematics reconstructs original target point from solved angles.'''
        target = Point2D(x=150.0, y=100.0)
        joints: ScaraJoints2D = self.solver.solve_ik_2d(target, elbow_left=False)
        self.assertTrue(joints.reachable)
        self.assertEqual(joints.status, IkStatus.SUCCESS)
        reconstructed: Point2D = self.solver.solve_fk_2d(joints.theta1, joints.theta2)
        self.assertAlmostEqual(reconstructed.x, target.x, places=4)
        self.assertAlmostEqual(reconstructed.y, target.y, places=4)

    def test_solve_ik_2d_unreachable(self) -> None:
        '''Confirms unreachable status is returned for target points outside mechanical reach.'''
        unreachable = Point2D(x=350.0, y=350.0)
        joints: ScaraJoints2D = self.solver.solve_ik_2d(unreachable)
        self.assertFalse(joints.reachable)
        self.assertEqual(joints.status, IkStatus.OUT_OF_REACH)

    def test_solve_ik_2d_inner_deadzone(self) -> None:
        '''Confirms inner deadzone status is returned for target points inside inner radius.'''
        deadzone = Point2D(x=5.0, y=0.0)
        joints: ScaraJoints2D = self.solver.solve_ik_2d(deadzone)
        self.assertFalse(joints.reachable)
        self.assertEqual(joints.status, IkStatus.INNER_DEADZONE)

    def test_solve_ik_2d_negative_quadrant_wrap(self) -> None:
        '''Verifies theta1 angle normalization when raw angle drops below -pi.'''
        target = Point2D(x=-150.0, y=-50.0)
        joints: ScaraJoints2D = self.solver.solve_ik_2d(target, elbow_left=True)
        self.assertTrue(joints.reachable)
        reconstructed = self.solver.solve_fk_2d(joints.theta1, joints.theta2)
        self.assertAlmostEqual(reconstructed.x, target.x, places=4)
        self.assertAlmostEqual(reconstructed.y, target.y, places=4)

    def test_get_version(self) -> None:
        '''Verifies component get_version returns valid version string.'''
        version: str = self.solver.get_version()
        self.assertIsInstance(version, str)
        self.assertTrue(len(version) > 0)


if __name__ == '__main__':
    main()
