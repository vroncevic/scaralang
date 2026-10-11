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
    Unit tests for KinematicsSolver analytical FK/IK calculations.
'''

from __future__ import annotations

from math import pi
from unittest import TestCase
from unittest import main

from scaralang.core.model.kinematics.link_dimensions import LinkDimensions
from scaralang.core.model.kinematics.point_2d import Point2D
from scaralang.core.service.kinematics.solver.factory import KinematicsSolverFactory
from scaralang.core.service.kinematics.solver.isolver import IKinematicsSolver

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.8'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestKinematicsSolver(TestCase):
    '''
        Validates KinematicsSolver analytical calculations.

        It defines:

            :methods:
                | setUp - Initializes KinematicsSolver instance via factory.
                | test_solve_fk - Verifies forward kinematics point calculations.
                | test_solve_fk_pose - Verifies elbow and tool joint positions.
                | test_solve_ik_roundtrip - Verifies FK(IK(point)) returns original point.
                | test_solve_ik_unreachable - Confirms None for unreachable points.
                | test_get_version - Verifies component version string.
    '''

    def setUp(self) -> None:
        '''Sets up link dimensions and initializes solver via factory.'''
        links = LinkDimensions(l1=150.0, l2=120.0)
        self.solver: IKinematicsSolver = KinematicsSolverFactory.create(links=links)

    def test_solve_fk(self) -> None:
        '''Verifies forward kinematics point calculations.'''
        tool: Point2D = self.solver.solve_fk(0.0, 0.0)
        self.assertAlmostEqual(tool.x, 270.0, places=4)
        self.assertAlmostEqual(tool.y, 0.0, places=4)

        tool_90: Point2D = self.solver.solve_fk(pi / 2.0, 0.0)
        self.assertAlmostEqual(tool_90.x, 0.0, places=4)
        self.assertAlmostEqual(tool_90.y, 270.0, places=4)

    def test_solve_fk_pose(self) -> None:
        '''Verifies elbow and tool joint positions.'''
        elbow, tool = self.solver.solve_fk_pose(0.0, pi / 2.0)
        self.assertAlmostEqual(elbow.x, 150.0, places=4)
        self.assertAlmostEqual(elbow.y, 0.0, places=4)
        self.assertAlmostEqual(tool.x, 150.0, places=4)
        self.assertAlmostEqual(tool.y, 120.0, places=4)

    def test_solve_ik_roundtrip(self) -> None:
        '''Verifies FK(IK(point)) returns original point for both elbow configs.'''
        target = Point2D(x=150.0, y=100.0)
        angles_right = self.solver.solve_ik(target, elbow_left=False)
        self.assertIsNotNone(angles_right)
        assert angles_right is not None
        reconstructed_right = self.solver.solve_fk(*angles_right)
        self.assertAlmostEqual(reconstructed_right.x, target.x, places=4)
        self.assertAlmostEqual(reconstructed_right.y, target.y, places=4)

        angles_left = self.solver.solve_ik(target, elbow_left=True)
        self.assertIsNotNone(angles_left)
        assert angles_left is not None
        reconstructed_left = self.solver.solve_fk(*angles_left)
        self.assertAlmostEqual(reconstructed_left.x, target.x, places=4)
        self.assertAlmostEqual(reconstructed_left.y, target.y, places=4)

    def test_solve_ik_unreachable(self) -> None:
        '''Confirms None for unreachable points beyond max reach.'''
        unreachable = Point2D(x=300.0, y=300.0)
        self.assertIsNone(self.solver.solve_ik(unreachable))

    def test_solve_ik_negative_quadrant_wrap(self) -> None:
        '''Confirms angle normalization when theta1 is below -pi.'''
        target = Point2D(x=-120.0, y=-100.0)
        angles = self.solver.solve_ik(target, elbow_left=False)
        self.assertIsNotNone(angles)
        assert angles is not None
        reconstructed = self.solver.solve_fk(*angles)
        self.assertAlmostEqual(reconstructed.x, target.x, places=4)
        self.assertAlmostEqual(reconstructed.y, target.y, places=4)

    def test_get_version(self) -> None:
        '''Verifies component get_version returns valid version string.'''
        version: str = self.solver.get_version()
        self.assertIsInstance(version, str)
        self.assertTrue(len(version) > 0)


if __name__ == '__main__':
    main()
