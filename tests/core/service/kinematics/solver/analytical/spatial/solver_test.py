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
    Unit tests for SpatialKinematicsSolver calculations and vertical limit validation.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main
from scaralang.core.model.kinematics.pose.cartesian import CartesianPose
from scaralang.core.model.kinematics.solver.status import IkStatus
from scaralang.core.model.kinematics.profile.link import LinkDimensions
from scaralang.core.model.kinematics.pose.point_3d import Point3D
from scaralang.core.model.kinematics.solver.solution_3d import ScaraJoints3D
from scaralang.core.model.kinematics.solver.solution import ScaraJoints
from scaralang.core.model.kinematics.profile.vertical import VerticalBounds
from scaralang.core.service.kinematics.solver.analytical.planar.factory import PlanarKinematicsSolverFactory
from scaralang.core.service.kinematics.solver.analytical.planar.solver import PlanarKinematicsSolver
from scaralang.core.service.kinematics.solver.analytical.spatial.factory import SpatialKinematicsSolverFactory
from scaralang.core.service.kinematics.solver.analytical.spatial.solver import SpatialKinematicsSolver

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestSpatialKinematicsSolver(TestCase):
    '''
        Validates SpatialKinematicsSolver 3D and 4-DOF calculations and vertical limits.

        It defines:

            :methods:
                | setUp - Initializes planar solver and spatial solver with vertical bounds.
                | test_solve_fk_3d - Verifies 3D forward kinematics point calculation.
                | test_solve_ik_3d_roundtrip - Verifies 3D IK roundtrip with FK.
                | test_solve_ik_3d_unreachable_xy - Confirms status for unreachable XY point.
                | test_solve_ik_3d_vertical_limits - Confirms status for Z outside vertical limits.
                | test_solve_fk_4d - Verifies 4-DOF forward kinematics pose calculation.
                | test_solve_ik_4d_roundtrip - Verifies 4-DOF IK roundtrip equivalence.
                | test_solve_ik_4d_vertical_limits - Confirms status for pose Z violation.
                | test_get_version - Verifies component version string.
    '''

    def setUp(self) -> None:
        '''Sets up planar solver, vertical limits, and spatial solver instance.'''
        links = LinkDimensions(l1=150.0, l2=120.0)
        planar: PlanarKinematicsSolver = PlanarKinematicsSolverFactory.create(links=links)
        vertical = VerticalBounds(z_min=-50.0, z_max=50.0)
        self.solver: SpatialKinematicsSolver = SpatialKinematicsSolverFactory.create(
            planar=planar, vertical=vertical
        )

    def test_solve_fk_3d(self) -> None:
        '''Verifies 3D forward kinematics point calculation.'''
        point: Point3D = self.solver.solve_fk_3d(0.0, 0.0, 25.0)
        self.assertAlmostEqual(point.x, 270.0, places=4)
        self.assertAlmostEqual(point.y, 0.0, places=4)
        self.assertAlmostEqual(point.z, 25.0, places=4)

    def test_solve_ik_3d_roundtrip(self) -> None:
        '''Verifies 3D IK roundtrip consistency with FK.'''
        target = Point3D(x=150.0, y=100.0, z=30.0)
        res: ScaraJoints3D = self.solver.solve_ik_3d(target, elbow_left=False)
        self.assertTrue(res.reachable)
        self.assertEqual(res.status, IkStatus.SUCCESS)
        reconstructed = self.solver.solve_fk_3d(res.theta1, res.theta2, res.z)
        self.assertAlmostEqual(reconstructed.x, target.x, places=4)
        self.assertAlmostEqual(reconstructed.y, target.y, places=4)
        self.assertAlmostEqual(reconstructed.z, target.z, places=4)

    def test_solve_ik_3d_unreachable_xy(self) -> None:
        '''Confirms status for target points outside planar reach.'''
        unreachable = Point3D(x=350.0, y=350.0, z=10.0)
        res: ScaraJoints3D = self.solver.solve_ik_3d(unreachable)
        self.assertFalse(res.reachable)
        self.assertEqual(res.status, IkStatus.OUT_OF_REACH)

    def test_solve_ik_3d_vertical_limits(self) -> None:
        '''Confirms status when point Z exceeds vertical bounds.'''
        out_of_bounds = Point3D(x=150.0, y=100.0, z=-100.0)
        res: ScaraJoints3D = self.solver.solve_ik_3d(out_of_bounds)
        self.assertFalse(res.reachable)
        self.assertEqual(res.status, IkStatus.Z_LIMIT_EXCEEDED)

    def test_solve_fk_4d(self) -> None:
        '''Verifies 4-DOF forward kinematics pose calculation.'''
        pose: CartesianPose = self.solver.solve_fk_4d(0.0, 0.0, 15.0, 0.75)
        self.assertAlmostEqual(pose.x, 270.0, places=4)
        self.assertAlmostEqual(pose.y, 0.0, places=4)
        self.assertAlmostEqual(pose.z, 15.0, places=4)
        self.assertAlmostEqual(pose.phi, 0.75, places=4)

    def test_solve_ik_4d_roundtrip(self) -> None:
        '''Verifies 4-DOF IK roundtrip equivalence.'''
        target = CartesianPose(x=150.0, y=100.0, z=-20.0, phi=0.5)
        res: ScaraJoints = self.solver.solve_ik_4d(target, elbow_left=False)
        self.assertTrue(res.reachable)
        self.assertEqual(res.status, IkStatus.SUCCESS)
        reconstructed = self.solver.solve_fk_4d(res.theta1, res.theta2, res.z, res.theta4)
        self.assertAlmostEqual(reconstructed.x, target.x, places=4)
        self.assertAlmostEqual(reconstructed.y, target.y, places=4)
        self.assertAlmostEqual(reconstructed.z, target.z, places=4)
        self.assertAlmostEqual(reconstructed.phi, target.phi, places=4)

    def test_solve_ik_4d_vertical_limits(self) -> None:
        '''Confirms status when pose Z exceeds vertical bounds.'''
        out_of_bounds = CartesianPose(x=150.0, y=100.0, z=100.0, phi=0.0)
        res: ScaraJoints = self.solver.solve_ik_4d(out_of_bounds)
        self.assertFalse(res.reachable)
        self.assertEqual(res.status, IkStatus.Z_LIMIT_EXCEEDED)

    def test_get_version(self) -> None:
        '''Verifies component get_version returns valid version string.'''
        version: str = self.solver.get_version()
        self.assertIsInstance(version, str)
        self.assertEqual(version, '1.1.1')


if __name__ == '__main__':
    main()
