# -*- coding: UTF-8 -*-

'''
Module
    factory_test.py
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
    Unit tests for WorkspaceFactory component.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.model.kinematics.profile.bounds import ScaraBounds
from scaralang.core.service.kinematics.profile.default_scara_profile import DefaultScaraProfile
from scaralang.core.service.kinematics.solver.analytical.planar.factory import PlanarKinematicsSolverFactory
from scaralang.core.service.kinematics.solver.analytical.planar.isolver import IPlanarKinematicsSolver
from scaralang.core.service.kinematics.workspace.factory import WorkspaceFactory
from scaralang.core.service.kinematics.workspace.ievaluator import IWorkspaceBoundsEvaluator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestWorkspaceFactory(TestCase):
    '''
        Validates WorkspaceFactory instantiations and wiring.

        It defines:

            :methods:
                | test_create_with_collaborators - Verifies instantiation with explicit solver.
                | test_get_version - Verifies factory version string.
    '''

    def test_create_with_collaborators(self) -> None:
        '''Verifies factory builds evaluator with explicit bounds and planar solver.'''
        bounds: ScaraBounds = DefaultScaraProfile.create_bounds()
        planar: IPlanarKinematicsSolver = PlanarKinematicsSolverFactory.create(
            links=bounds.links
        )
        evaluator: IWorkspaceBoundsEvaluator = WorkspaceFactory.create(
            bounds=bounds,
            planar=planar,
        )
        self.assertIsInstance(evaluator, IWorkspaceBoundsEvaluator)
        self.assertEqual(evaluator.get_bounds(), bounds)

    def test_get_version(self) -> None:
        '''Verifies factory returns version string.'''
        version = WorkspaceFactory.get_version()
        self.assertIsInstance(version, str)
        self.assertTrue(len(version) > 0)


if __name__ == '__main__':
    main()
