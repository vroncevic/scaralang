# -*- coding: UTF-8 -*-

'''
Module
    kinematics_service_test.py
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
    Unit tests for KinematicsService analytical kinematics and workspace calculations.
'''

from __future__ import annotations

from math import isclose
from math import pi
from math import radians
from unittest import TestCase
from unittest import main

from scaralang.core.model.kinematics.joint_angle_bounds import JointAngleBounds
from scaralang.core.model.kinematics.link_dimensions import LinkDimensions
from scaralang.core.model.kinematics.point_2d import Point2D
from scaralang.core.model.kinematics.point_3d import Point3D
from scaralang.core.model.kinematics.scara_bounds import ScaraBounds
from scaralang.core.model.kinematics.singularity_margins import SingularityMargins
from scaralang.core.model.kinematics.speed_limits import SpeedLimits
from scaralang.core.model.kinematics.vertical_bounds import VerticalBounds
from scaralang.core.service.kinematics.ikinematics_service import IKinematicsService
from scaralang.core.service.kinematics.kinematics_service import KinematicsService

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestKinematicsService(TestCase):
    '''
        Validates KinematicsService forward/inverse kinematics and workspace boundary logic.

        It defines:

            :methods:
                | setUp - Prepares default bounds and service instance.
                | test_protocol_conformance - Verifies runtime Protocol check.
                | test_reach_radii_calculation - Checks r_min and r_max calculation.
                | test_forward_kinematics - Verifies FK analytical coordinate output.
                | test_solve_fk_pose - Verifies FK analytical joint and tool pose coordinates.
                | test_inverse_kinematics_roundtrip - Verifies FK(IK(x, y)) roundtrip equivalence.
                | test_inverse_kinematics_unreachable - Confirms None for points beyond reach.
                | test_is_in_workspace - Tests annular distance and vertical height checks.
                | test_is_joint_reachable - Tests angular joint limits and singularity deadband.
                | test_is_joint_reachable_singularity - Tests reachability rejection in singularity deadband.
                | test_is_joint_reachable_j2_limit - Tests reachability rejection on J2 angular limit.
    '''

    def setUp(self) -> None:
        '''
            Sets up standard SCARA geometry bounds and initializes KinematicsService.
        '''
        self.bounds = ScaraBounds(
            links=LinkDimensions(l1=150.0, l2=120.0),
            vertical=VerticalBounds(z_min=0.0, z_max=50.0),
            speeds=SpeedLimits(
                min_speed=1.0,
                max_speed=200.0,
                default_speed=50.0,
                default_accel=100.0,
                max_accel=500.0,
            ),
            joints=JointAngleBounds(
                j1_min_rad=radians(-150.0),
                j1_max_rad=radians(150.0),
                j2_min_rad=radians(-145.0),
                j2_max_rad=radians(145.0),
            ),
            singularity=SingularityMargins(
                singularity_outer_margin_mm=5.0,
                singularity_inner_margin_mm=5.0,
                singularity_theta2_min_rad=radians(5.0),
                deadzone_r_min=20.0,
            ),
        )
        self.service = KinematicsService(bounds=self.bounds)

    def test_protocol_conformance(self) -> None:
        '''
            Verifies that KinematicsService conforms to IKinematicsService runtime Protocol.
        '''
        self.assertIsInstance(self.service, IKinematicsService)

    def test_reach_radii_calculation(self) -> None:
        '''
            Verifies that minimum and maximum reach radii match link length calculations.
        '''
        self.assertAlmostEqual(self.service.r_min, 30.0)
        self.assertAlmostEqual(self.service.r_max, 270.0)
        self.assertEqual(self.service.bounds.links.l1, 150.0)
        self.assertEqual(self.service.bounds.links.l2, 120.0)

    def test_forward_kinematics(self) -> None:
        '''
            Tests forward kinematics at zero and 90-degree arm configurations.
        '''
        tool = self.service.solve_fk(0.0, 0.0)
        self.assertAlmostEqual(tool.x, 270.0)
        self.assertAlmostEqual(tool.y, 0.0)

        tool90 = self.service.solve_fk(pi / 2.0, 0.0)
        self.assertAlmostEqual(tool90.x, 0.0)
        self.assertAlmostEqual(tool90.y, 270.0)

    def test_solve_fk_pose(self) -> None:
        '''
            Tests forward kinematics link pose coordinates for elbow and tool.
        '''
        elbow, tool = self.service.solve_fk_pose(0.0, 0.0)
        self.assertAlmostEqual(elbow.x, 150.0)
        self.assertAlmostEqual(elbow.y, 0.0)
        self.assertAlmostEqual(tool.x, 270.0)
        self.assertAlmostEqual(tool.y, 0.0)

        elbow90, tool90 = self.service.solve_fk_pose(pi / 2.0, 0.0)
        self.assertAlmostEqual(elbow90.x, 0.0)
        self.assertAlmostEqual(elbow90.y, 150.0)
        self.assertAlmostEqual(tool90.x, 0.0)
        self.assertAlmostEqual(tool90.y, 270.0)

    def test_inverse_kinematics_roundtrip(self) -> None:
        '''
            Tests analytical IK roundtrip consistency with FK for both elbow configurations.
        '''
        target_pt = Point2D(x=120.0, y=100.0)

        for elbow_left in (False, True):
            ik_res = self.service.solve_ik(point=target_pt, elbow_left=elbow_left)
            self.assertIsNotNone(ik_res)
            theta1, theta2 = ik_res
            fk_pt = self.service.solve_fk(theta1, theta2)
            self.assertTrue(isclose(fk_pt.x, target_pt.x, abs_tol=1e-3))
            self.assertTrue(isclose(fk_pt.y, target_pt.y, abs_tol=1e-3))

    def test_inverse_kinematics_unreachable(self) -> None:
        '''
            Tests that points outside the kinematic reach envelope return None.
        '''
        ik_res = self.service.solve_ik(Point2D(x=300.0, y=300.0))
        self.assertIsNone(ik_res)

        ik_res_origin = self.service.solve_ik(Point2D(x=5.0, y=0.0))
        self.assertIsNone(ik_res_origin)

    def test_is_in_workspace(self) -> None:
        '''
            Tests workspace envelope evaluation for annular deadband, outer reach, and Z limits.
        '''
        valid, msg = self.service.is_in_workspace(Point3D(x=150.0, y=50.0, z=25.0))
        self.assertTrue(valid)
        self.assertIn('within Cartesian workspace', msg)

        out_reach, msg_reach = self.service.is_in_workspace(
            Point3D(x=200.0, y=200.0, z=10.0)
        )
        self.assertFalse(out_reach)
        self.assertIn('exceeds maximum reach', msg_reach)

        deadzone, msg_dead = self.service.is_in_workspace(
            Point3D(x=10.0, y=10.0, z=10.0)
        )
        self.assertFalse(deadzone)
        self.assertIn('inside deadzone', msg_dead)

        z_err, msg_z = self.service.is_in_workspace(
            Point3D(x=150.0, y=50.0, z=60.0)
        )
        self.assertFalse(z_err)
        self.assertIn('Elevation Z', msg_z)

    def test_is_joint_reachable(self) -> None:
        '''
            Tests joint angular limits and singularity deadband reachability evaluation.
        '''
        reachable, reasons = self.service.is_joint_reachable(Point2D(x=150.0, y=50.0))
        self.assertTrue(reachable)
        self.assertEqual(len(reasons), 0)

        unreachable_far, reasons_far = self.service.is_joint_reachable(
            Point2D(x=350.0, y=0.0)
        )
        self.assertFalse(unreachable_far)
        self.assertGreater(len(reasons_far), 0)

        unreachable_rear, reasons_rear = self.service.is_joint_reachable(
            Point2D(x=-250.0, y=0.0)
        )
        self.assertFalse(unreachable_rear)
        self.assertGreater(len(reasons_rear), 0)

    def test_is_joint_reachable_singularity(self) -> None:
        '''
            Verifies reachability failure when point falls in singularity deadband.
        '''
        reachable, reasons = self.service.is_joint_reachable(Point2D(x=269.8, y=0.0))
        self.assertFalse(reachable)
        self.assertIn('J2 in singularity deadband', reasons)

    def test_is_joint_reachable_j2_limit(self) -> None:
        '''
            Verifies reachability failure when required J2 angle exceeds joint limits.
        '''
        restricted_bounds = ScaraBounds(
            links=LinkDimensions(l1=150.0, l2=120.0),
            vertical=VerticalBounds(z_min=0.0, z_max=50.0),
            speeds=SpeedLimits(
                min_speed=1.0,
                max_speed=200.0,
                default_speed=50.0,
                default_accel=100.0,
                max_accel=500.0,
            ),
            joints=JointAngleBounds(
                j1_min_rad=radians(-150.0),
                j1_max_rad=radians(150.0),
                j2_min_rad=radians(-10.0),
                j2_max_rad=radians(10.0),
            ),
            singularity=SingularityMargins(
                singularity_outer_margin_mm=5.0,
                singularity_inner_margin_mm=5.0,
                singularity_theta2_min_rad=radians(1.0),
                deadzone_r_min=20.0,
            ),
        )
        service = KinematicsService(bounds=restricted_bounds)
        reachable, reasons = service.is_joint_reachable(Point2D(x=200.0, y=0.0))
        self.assertFalse(reachable)
        self.assertTrue(any('J2 angle' in r for r in reasons))


if __name__ == '__main__':
    main()
