# -*- coding: UTF-8 -*-

'''
Module
    planner_test.py
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
    Unit tests for ElbowReconfigurationPlanner class.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.model.exceptions.kinematics import ScaraKinematicsError
from scaralang.core.model.kinematics.solver.dls import DlsConfig
from scaralang.core.model.kinematics.solver.elbow import ElbowConfig
from scaralang.core.model.kinematics.profile.bounds import ScaraBounds
from scaralang.core.model.trajectory.plan.reconfiguration import ReconfigurationRequest
from scaralang.core.model.trajectory.plan.waypoint import Waypoint
from scaralang.core.service.kinematics.dependencies import KinematicsDependencies
from scaralang.core.service.kinematics.factory import KinematicsFactory
from scaralang.core.service.kinematics.profile.default_scara_profile import DefaultScaraProfile
from scaralang.core.service.trajectory.reconfiguration.dependencies import ReconfigurationDependencies
from scaralang.core.service.trajectory.reconfiguration.planner import ElbowReconfigurationPlanner

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestElbowReconfigurationPlanner(TestCase):
    '''
        Test cases for ElbowReconfigurationPlanner kinematic transition maneuvers.

        It defines:

            :methods:
                | setUp - Prepares planner instance and robot kinematic bounds.
                | test_is_reconfiguration_required - Verifies reconfiguration check.
                | test_plan_same_elbow_returns_empty - Verifies no maneuver for same elbow.
                | test_plan_reconfiguration_success - Verifies 3-phase transition generation.
                | test_plan_reconfiguration_in_place_flip - Verifies in-place pose flipping.
                | test_plan_unreachable_point_raises - Verifies reachability validation error.
                | test_plan_invalid_z_safe_raises - Verifies vertical bounds validation.
                | test_get_version - Verifies version string retrieval.
    '''

    planner: ElbowReconfigurationPlanner

    def setUp(self) -> None:
        '''
            Prepares robot kinematics model and planner component.

            :exceptions: None.
        '''
        bounds: ScaraBounds = DefaultScaraProfile.create_bounds()
        dls_config: DlsConfig = DefaultScaraProfile.create_dls_config()
        kinematics = KinematicsFactory.create(
            dependencies=KinematicsDependencies(
                bounds=bounds,
                dls_config=dls_config,
            )
        )
        deps = ReconfigurationDependencies(
            planar=kinematics.planar,
            workspace=kinematics.workspace,
        )
        self.planner = ElbowReconfigurationPlanner(dependencies=deps)

    def test_is_reconfiguration_required(self) -> None:
        '''
            Verifies reconfiguration check between elbow configurations.

            :exceptions: None.
        '''
        self.assertFalse(
            self.planner.is_reconfiguration_required(
                ElbowConfig.RIGHT, ElbowConfig.RIGHT
            )
        )
        self.assertFalse(
            self.planner.is_reconfiguration_required(
                ElbowConfig.LEFT, ElbowConfig.LEFT
            )
        )
        self.assertTrue(
            self.planner.is_reconfiguration_required(
                ElbowConfig.RIGHT, ElbowConfig.LEFT
            )
        )
        self.assertTrue(
            self.planner.is_reconfiguration_required(
                ElbowConfig.LEFT, ElbowConfig.RIGHT
            )
        )

    def test_plan_same_elbow_returns_empty(self) -> None:
        '''
            Verifies no maneuver is planned when elbow configurations match.

            :exceptions: None.
        '''
        wp_from = Waypoint(
            x=150.0,
            y=100.0,
            z=0.0,
            phi=0.0,
            speed=30.0,
            name='P1',
            command='MOVE',
        )
        wp_to = Waypoint(
            x=120.0,
            y=80.0,
            z=0.0,
            phi=0.0,
            speed=30.0,
            name='P2',
            command='MOVE',
        )
        req = ReconfigurationRequest(
            from_waypoint=wp_from,
            to_waypoint=wp_to,
            from_elbow=ElbowConfig.RIGHT,
            to_elbow=ElbowConfig.RIGHT,
            z_safe=25.0,
        )
        result = self.planner.plan_reconfiguration(req)
        self.assertEqual(result, [])

    def test_plan_reconfiguration_success(self) -> None:
        '''
            Verifies successful generation of retract, transit, and align waypoints.

            :exceptions: None.
        '''
        wp_from = Waypoint(
            x=150.0,
            y=100.0,
            z=0.0,
            phi=10.0,
            speed=30.0,
            name='P1',
            command='MOVE',
        )
        # P39 is reachable in LEFT configuration
        wp_to = Waypoint(
            x=-248.3,
            y=-87.8,
            z=5.0,
            phi=20.0,
            speed=40.0,
            name='P39',
            command='MOVE',
        )
        req = ReconfigurationRequest(
            from_waypoint=wp_from,
            to_waypoint=wp_to,
            from_elbow=ElbowConfig.RIGHT,
            to_elbow=ElbowConfig.LEFT,
            z_safe=35.0,
        )
        result = self.planner.plan_reconfiguration(req)
        self.assertEqual(len(result), 3)

        retract, transit, align = result[0], result[1], result[2]
        self.assertEqual(retract.x, wp_from.x)
        self.assertEqual(retract.y, wp_from.y)
        self.assertEqual(retract.z, 35.0)
        self.assertEqual(retract.command, 'RECONFIG_RETRACT')

        self.assertEqual(transit.z, 35.0)
        self.assertEqual(transit.command, 'RECONFIG_TRANSIT')

        self.assertEqual(align.x, wp_to.x)
        self.assertEqual(align.y, wp_to.y)
        self.assertEqual(align.z, 35.0)
        self.assertEqual(align.command, 'RECONFIG_ALIGN')

    def test_plan_reconfiguration_in_place_flip(self) -> None:
        '''
            Verifies in-place elbow flipping at the same Cartesian coordinate.

            :exceptions: None.
        '''
        wp = Waypoint(
            x=150.0,
            y=100.0,
            z=0.0,
            phi=0.0,
            speed=30.0,
            name='P_FLIP',
            command='MOVE',
        )
        req = ReconfigurationRequest(
            from_waypoint=wp,
            to_waypoint=wp,
            from_elbow=ElbowConfig.RIGHT,
            to_elbow=ElbowConfig.LEFT,
            z_safe=30.0,
        )
        result = self.planner.plan_reconfiguration(req)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].x, wp.x)
        self.assertEqual(result[2].x, wp.x)

    def test_plan_unreachable_point_raises(self) -> None:
        '''
            Verifies ScaraKinematicsError when a waypoint is unreachable for given elbow.

            :exceptions: None.
        '''
        wp_valid = Waypoint(
            x=150.0,
            y=100.0,
            z=0.0,
            phi=0.0,
            speed=30.0,
            name='P1',
            command='MOVE',
        )
        # P39 is unreachable in RIGHT configuration
        wp_unreachable = Waypoint(
            x=-248.3,
            y=-87.8,
            z=0.0,
            phi=0.0,
            speed=30.0,
            name='P39_BAD',
            command='MOVE',
        )
        req_start_bad = ReconfigurationRequest(
            from_waypoint=wp_unreachable,
            to_waypoint=wp_valid,
            from_elbow=ElbowConfig.RIGHT,
            to_elbow=ElbowConfig.LEFT,
            z_safe=25.0,
        )
        with self.assertRaises(ScaraKinematicsError):
            self.planner.plan_reconfiguration(req_start_bad)

        req_target_bad = ReconfigurationRequest(
            from_waypoint=wp_valid,
            to_waypoint=wp_unreachable,
            from_elbow=ElbowConfig.LEFT,
            to_elbow=ElbowConfig.RIGHT,
            z_safe=25.0,
        )
        with self.assertRaises(ScaraKinematicsError):
            self.planner.plan_reconfiguration(req_target_bad)

    def test_plan_invalid_z_safe_raises(self) -> None:
        '''
            Verifies ScaraKinematicsError when z_safe violates vertical bounds.

            :exceptions: None.
        '''
        wp1 = Waypoint(
            x=150.0,
            y=100.0,
            z=0.0,
            phi=0.0,
            speed=30.0,
            name='P1',
            command='MOVE',
        )
        wp2 = Waypoint(
            x=150.0,
            y=100.0,
            z=0.0,
            phi=0.0,
            speed=30.0,
            name='P2',
            command='MOVE',
        )
        req_overflow = ReconfigurationRequest(
            from_waypoint=wp1,
            to_waypoint=wp2,
            from_elbow=ElbowConfig.RIGHT,
            to_elbow=ElbowConfig.LEFT,
            z_safe=100.0,
        )
        with self.assertRaises(ScaraKinematicsError):
            self.planner.plan_reconfiguration(req_overflow)

    def test_get_version(self) -> None:
        '''
            Verifies component version string retrieval.

            :exceptions: None.
        '''
        version = self.planner.get_version()
        self.assertIsInstance(version, str)
        self.assertTrue(len(version) > 0)


if __name__ == '__main__':
    main()
