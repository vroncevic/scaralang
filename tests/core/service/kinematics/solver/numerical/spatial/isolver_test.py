# -*- coding: UTF-8 -*-

'''
Module
    isolver_test.py
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
    Unit tests for INumericalSpatialKinematicsSolver structural protocol.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.model.kinematics.pose.cartesian import CartesianPose
from scaralang.core.model.kinematics.solver.status import IkStatus
from scaralang.core.model.kinematics.solver.solution import ScaraJoints
from scaralang.core.service.kinematics.solver.numerical.spatial.isolver import INumericalSpatialKinematicsSolver

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DummyNumericalSpatialSolver:
    '''
        Dummy class implementing INumericalSpatialKinematicsSolver protocol structurally.

        It defines:

            :methods:
                | solve_dls_4d - Solves mock 4-DOF numerical inverse kinematics.
                | get_version - Returns mock version string.
    '''

    def solve_dls_4d(
        self,
        target_pose: CartesianPose,
        initial_joints: ScaraJoints,
    ) -> ScaraJoints:
        '''
            Mock solve_dls_4d implementation.

            :param target_pose: Target pose.
            :param initial_joints: Initial joints.
            :return: ScaraJoints result.
            :exceptions: None.
        '''
        del initial_joints
        return ScaraJoints(
            theta1=0.0,
            theta2=0.0,
            z=target_pose.z,
            theta4=target_pose.phi,
            reachable=True,
            status=IkStatus.SUCCESS,
        )

    def get_version(self) -> str:
        '''
            Mock get_version implementation.

            :return: Version string representation.
            :exceptions: None.
        '''
        return '1.1.1'


class TestINumericalSpatialKinematicsSolver(TestCase):
    '''
        Test cases verifying INumericalSpatialKinematicsSolver structural protocol.

        It defines:

            :methods:
                | test_protocol_conformance - Verifies dummy class conforms to protocol.
                | test_non_conforming_class - Verifies non-conforming object fails check.
    '''

    def test_protocol_conformance(self) -> None:
        '''
            Verifies structural conformance to INumericalSpatialKinematicsSolver.

            :exceptions: None.
        '''
        solver = DummyNumericalSpatialSolver()
        self.assertIsInstance(solver, INumericalSpatialKinematicsSolver)

    def test_non_conforming_class(self) -> None:
        '''
            Verifies that non-conforming object fails protocol check.

            :exceptions: None.
        '''
        self.assertNotIsInstance(object(), INumericalSpatialKinematicsSolver)


if __name__ == '__main__':
    main()
