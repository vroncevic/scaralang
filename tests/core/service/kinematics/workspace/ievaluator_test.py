# -*- coding: UTF-8 -*-

'''
Module
    ievaluator_test.py
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
    Unit tests for IWorkspaceBoundsEvaluator structural protocol conformance.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.model.kinematics.scara_bounds import ScaraBounds
from scaralang.core.service.kinematics.profile.default_scara_profile import DefaultScaraProfile
from scaralang.core.service.kinematics.solver.factory import KinematicsSolverFactory
from scaralang.core.service.kinematics.solver.isolver import IKinematicsSolver
from scaralang.core.service.kinematics.workspace.evaluator import WorkspaceBoundsEvaluator
from scaralang.core.service.kinematics.workspace.factory import WorkspaceBoundsEvaluatorFactory
from scaralang.core.service.kinematics.workspace.ievaluator import IWorkspaceBoundsEvaluator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.8'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestIWorkspaceBoundsEvaluator(TestCase):
    '''
        Test cases verifying IWorkspaceBoundsEvaluator protocol structural subtyping.

        It defines:

            :methods:
                | test_structural_conformance - Verifies WorkspaceBoundsEvaluator satisfies protocol.
                | test_factory_return_conformance - Verifies factory returns protocol instance.
    '''

    def test_structural_conformance(self) -> None:
        '''Verifies concrete WorkspaceBoundsEvaluator satisfies IWorkspaceBoundsEvaluator protocol.'''
        bounds: ScaraBounds = DefaultScaraProfile.create_bounds()
        solver: IKinematicsSolver = KinematicsSolverFactory.create(links=bounds.links)
        evaluator = WorkspaceBoundsEvaluator(bounds=bounds, solver=solver)
        self.assertIsInstance(evaluator, IWorkspaceBoundsEvaluator)

    def test_factory_return_conformance(self) -> None:
        '''Verifies factory returns instance satisfying IWorkspaceBoundsEvaluator protocol.'''
        bounds: ScaraBounds = DefaultScaraProfile.create_bounds()
        solver: IKinematicsSolver = KinematicsSolverFactory.create(links=bounds.links)
        evaluator: IWorkspaceBoundsEvaluator = (
            WorkspaceBoundsEvaluatorFactory.create(bounds=bounds, solver=solver)
        )
        self.assertIsInstance(evaluator, IWorkspaceBoundsEvaluator)


if __name__ == '__main__':
    main()
