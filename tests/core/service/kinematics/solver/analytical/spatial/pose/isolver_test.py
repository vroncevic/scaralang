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
    Unit tests for ISpatialPoseKinematicsSolver protocol contract.
'''

from __future__ import annotations

from typing import Protocol
from unittest import TestCase
from unittest import main

from scaralang.core.service.kinematics.solver.analytical.spatial.pose.isolver import ISpatialPoseKinematicsSolver

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestISpatialPoseKinematicsSolver(TestCase):
    '''
        Validates ISpatialPoseKinematicsSolver protocol contract.

        It defines:

            :methods:
                | test_is_protocol - Verifies ISpatialPoseKinematicsSolver is a Protocol.
                | test_required_methods - Verifies protocol method definitions.
    '''

    def test_is_protocol(self) -> None:
        '''
            Verifies that ISpatialPoseKinematicsSolver is a runtime checkable Protocol.

            :exceptions: None.
        '''
        self.assertTrue(issubclass(ISpatialPoseKinematicsSolver, Protocol))

    def test_required_methods(self) -> None:
        '''
            Verifies that protocol defines expected methods.

            :exceptions: None.
        '''
        expected_members: tuple[str, ...] = (
            'solve_fk_4d',
            'solve_ik_4d',
            'get_version',
        )

        for member in expected_members:
            self.assertTrue(
                hasattr(ISpatialPoseKinematicsSolver, member),
                f'ISpatialPoseKinematicsSolver missing contract member: {member}',
            )


if __name__ == '__main__':
    main()
