# -*- coding: UTF-8 -*-

'''
Module
    evaluator_test.py
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
    Unit tests for WorkspaceBoundsEvaluator workspace reach and joint checks.
'''

from __future__ import annotations

from math import radians
from unittest import TestCase
from unittest import main

from scaralang.core.model.kinematics.joint_angle_bounds import JointAngleBounds
from scaralang.core.model.kinematics.point_2d import Point2D
from scaralang.core.model.kinematics.point_3d import Point3D
from scaralang.core.model.kinematics.scara_bounds import ScaraBounds
from scaralang.core.model.kinematics.singularity_margins import SingularityMargins
from scaralang.core.service.kinematics.profile.default_scara_profile import DefaultScaraProfile
from scaralang.core.service.kinematics.solver.planar.factory import PlanarKinematicsSolverFactory
from scaralang.core.service.kinematics.solver.planar.isolver import IPlanarKinematicsSolver
from scaralang.core.service.kinematics.workspace.factory import WorkspaceFactory
from scaralang.core.service.kinematics.workspace.ievaluator import IWorkspaceBoundsEvaluator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.9'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestWorkspaceBoundsEvaluator(TestCase):
    '''
        Validates WorkspaceBoundsEvaluator workspace annular reach and joint limits.

        It defines:

            :methods:
                | setUp - Initializes standard bounds and evaluator instance.
                | test_is_in_workspace_valid - Verifies valid workspace point.
                | test_is_in_workspace_exceeds_max_reach - Verifies reach beyond r_max.
                | test_is_in_workspace_inside_deadzone - Verifies point inside inner deadzone.
                | test_is_in_workspace_z_out_of_range - Verifies elevation limits violation.
                | test_is_joint_reachable_valid - Verifies reachable valid point.
                | test_is_joint_reachable_unreachable - Verifies mathematical reachability rejection.
                | test_is_joint_reachable_j1_limit - Verifies joint 1 angular limit violation.
                | test_is_joint_reachable_j2_limit - Verifies joint 2 angular limit violation.
                | test_is_joint_reachable_singularity - Verifies singularity deadband rejection.
                | test_get_bounds - Verifies bounds accessor.
                | test_get_version - Verifies version string accessor.
    '''

    def setUp(self) -> None:
        '''Initializes standard bounds and evaluator instance.'''
        self.bounds: ScaraBounds = DefaultScaraProfile.create_bounds()
        planar: IPlanarKinematicsSolver = PlanarKinematicsSolverFactory.create(
            links=self.bounds.links
        )
        self.evaluator: IWorkspaceBoundsEvaluator = (
            WorkspaceFactory.create(bounds=self.bounds, planar=planar)
        )

    def test_is_in_workspace_valid(self) -> None:
        '''Verifies valid Cartesian coordinate inside annular workspace.'''
        valid, msg = self.evaluator.is_in_workspace(Point3D(x=150.0, y=100.0, z=25.0))
        self.assertTrue(valid)
        self.assertIn('within Cartesian workspace', msg)

    def test_is_in_workspace_exceeds_max_reach(self) -> None:
        '''Verifies rejection when radius exceeds r_max.'''
        valid, msg = self.evaluator.is_in_workspace(Point3D(x=300.0, y=300.0, z=25.0))
        self.assertFalse(valid)
        self.assertIn('exceeds maximum reach', msg)

    def test_is_in_workspace_inside_deadzone(self) -> None:
        '''Verifies rejection when radius is inside inner deadzone.'''
        valid, msg = self.evaluator.is_in_workspace(Point3D(x=10.0, y=10.0, z=25.0))
        self.assertFalse(valid)
        self.assertIn('inside deadzone', msg)

    def test_is_in_workspace_z_out_of_range(self) -> None:
        '''Verifies rejection when elevation Z is below z_min or above z_max.'''
        valid_low, msg_low = self.evaluator.is_in_workspace(Point3D(x=150.0, y=100.0, z=-60.0))
        self.assertFalse(valid_low)
        self.assertIn('Elevation Z', msg_low)

        valid_high, msg_high = self.evaluator.is_in_workspace(Point3D(x=150.0, y=100.0, z=100.0))
        self.assertFalse(valid_high)
        self.assertIn('Elevation Z', msg_high)

    def test_is_joint_reachable_valid(self) -> None:
        '''Verifies reachable valid 2D planar position.'''
        reachable, reasons = self.evaluator.is_joint_reachable(Point2D(x=150.0, y=100.0))
        self.assertTrue(reachable)
        self.assertEqual(len(reasons), 0)

    def test_is_joint_reachable_unreachable(self) -> None:
        '''Verifies rejection for points outside arm reach.'''
        reachable, reasons = self.evaluator.is_joint_reachable(Point2D(x=400.0, y=400.0))
        self.assertFalse(reachable)
        self.assertTrue(any('Mathematically unreachable' in r for r in reasons))

    def test_is_joint_reachable_j1_limit(self) -> None:
        '''Verifies rejection when shoulder joint J1 exceeds angular bounds.'''
        restricted_joints = JointAngleBounds(
            j1_min_rad=radians(0.0),
            j1_max_rad=radians(10.0),
            j2_min_rad=radians(-145.0),
            j2_max_rad=radians(145.0),
        )
        restricted_bounds = ScaraBounds(
            links=self.bounds.links,
            vertical=self.bounds.vertical,
            speeds=self.bounds.speeds,
            joints=restricted_joints,
            singularity=self.bounds.singularity,
        )
        planar = PlanarKinematicsSolverFactory.create(
            links=restricted_bounds.links,
        )
        evaluator = WorkspaceFactory.create(
            bounds=restricted_bounds,
            planar=planar,
        )
        reachable, reasons = evaluator.is_joint_reachable(Point2D(x=-150.0, y=100.0))
        self.assertFalse(reachable)
        self.assertTrue(any('J1 angle' in r for r in reasons))

    def test_is_joint_reachable_j2_limit(self) -> None:
        '''Verifies rejection when elbow joint J2 exceeds angular bounds.'''
        restricted_joints = JointAngleBounds(
            j1_min_rad=radians(-150.0),
            j1_max_rad=radians(150.0),
            j2_min_rad=radians(-10.0),
            j2_max_rad=radians(10.0),
        )
        restricted_bounds = ScaraBounds(
            links=self.bounds.links,
            vertical=self.bounds.vertical,
            speeds=self.bounds.speeds,
            joints=restricted_joints,
            singularity=SingularityMargins(
                singularity_outer_margin_mm=5.0,
                singularity_inner_margin_mm=5.0,
                singularity_theta2_min_rad=radians(1.0),
                deadzone_r_min=20.0,
            ),
        )
        planar = PlanarKinematicsSolverFactory.create(
            links=restricted_bounds.links,
        )
        evaluator = WorkspaceFactory.create(
            bounds=restricted_bounds,
            planar=planar,
        )
        reachable, reasons = evaluator.is_joint_reachable(Point2D(x=200.0, y=0.0))
        self.assertFalse(reachable)
        self.assertTrue(any('J2 angle' in r for r in reasons))

    def test_is_joint_reachable_singularity(self) -> None:
        '''Verifies rejection when arm is extended straight out into singularity deadband.'''
        singularity_bounds = ScaraBounds(
            links=self.bounds.links,
            vertical=self.bounds.vertical,
            speeds=self.bounds.speeds,
            joints=self.bounds.joints,
            singularity=SingularityMargins(
                singularity_outer_margin_mm=5.0,
                singularity_inner_margin_mm=5.0,
                singularity_theta2_min_rad=radians(10.0),
                deadzone_r_min=20.0,
            ),
        )
        planar = PlanarKinematicsSolverFactory.create(
            links=singularity_bounds.links,
        )
        evaluator = WorkspaceFactory.create(
            bounds=singularity_bounds,
            planar=planar,
        )
        reachable, reasons = evaluator.is_joint_reachable(Point2D(x=299.8, y=0.0))
        self.assertFalse(reachable)
        self.assertTrue(any('singularity deadband' in r for r in reasons))

    def test_get_bounds(self) -> None:
        '''Verifies access to underlying robot ScaraBounds model.'''
        self.assertEqual(self.evaluator.get_bounds(), self.bounds)

    def test_get_version(self) -> None:
        '''Verifies version string accessor.'''
        version = self.evaluator.get_version()
        self.assertIsInstance(version, str)
        self.assertTrue(len(version) > 0)


if __name__ == '__main__':
    main()
