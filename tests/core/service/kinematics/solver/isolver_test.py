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
    Unit tests for IKinematicsSolver structural protocol conformance.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.model.kinematics.link_dimensions import LinkDimensions
from scaralang.core.service.kinematics.solver.factory import KinematicsSolverFactory
from scaralang.core.service.kinematics.solver.isolver import IKinematicsSolver
from scaralang.core.service.kinematics.solver.solver import KinematicsSolver

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.8'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestIKinematicsSolver(TestCase):
    '''
        Test cases verifying IKinematicsSolver protocol structural subtyping.

        It defines:

            :methods:
                | test_structural_conformance - Verifies KinematicsSolver satisfies protocol.
                | test_factory_return_conformance - Verifies factory returns protocol instance.
    '''

    def test_structural_conformance(self) -> None:
        '''Verifies concrete KinematicsSolver satisfies IKinematicsSolver protocol.'''
        links = LinkDimensions(l1=150.0, l2=120.0)
        solver = KinematicsSolver(links=links)
        self.assertIsInstance(solver, IKinematicsSolver)

    def test_factory_return_conformance(self) -> None:
        '''Verifies factory returns instance satisfying IKinematicsSolver protocol.'''
        links = LinkDimensions(l1=150.0, l2=120.0)
        solver: IKinematicsSolver = KinematicsSolverFactory.create(links=links)
        self.assertIsInstance(solver, IKinematicsSolver)


if __name__ == '__main__':
    main()
