# -*- coding: UTF-8 -*-

'''
Module
    iservice_test.py
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
    Unit tests for IWorkspaceBoundaryService structural protocol conformance.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.service.kinematics.workspace.boundary.factory import BoundaryFactory
from scaralang.core.service.kinematics.workspace.boundary.iservice import IWorkspaceBoundaryService
from scaralang.core.service.kinematics.workspace.boundary.provides import BoundaryProvides
from scaralang.core.service.kinematics.workspace.boundary.service import WorkspaceBoundaryService

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.9'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestIWorkspaceBoundaryService(TestCase):
    '''
        Test cases verifying IWorkspaceBoundaryService protocol structural subtyping.

        It defines:

            :methods:
                | test_structural_conformance - Verifies WorkspaceBoundaryService satisfies protocol.
                | test_factory_return_conformance - Verifies factory returns protocol instance.
    '''

    def test_structural_conformance(self) -> None:
        '''
            Verifies concrete WorkspaceBoundaryService satisfies IWorkspaceBoundaryService.
        '''
        service = WorkspaceBoundaryService()
        self.assertTrue(isinstance(service, IWorkspaceBoundaryService))

    def test_factory_return_conformance(self) -> None:
        '''
            Verifies BoundaryFactory returns BoundaryProvides with IWorkspaceBoundaryService.
        '''
        provides: BoundaryProvides = BoundaryFactory.create()
        self.assertTrue(isinstance(provides.service, IWorkspaceBoundaryService))


if __name__ == '__main__':
    main()
