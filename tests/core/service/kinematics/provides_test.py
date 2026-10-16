# -*- coding: UTF-8 -*-

'''
Module
    provides_test.py
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
    Unit tests for KinematicsProvides output data transfer object.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main
from unittest.mock import MagicMock

from scaralang.core.service.kinematics.envelope.ienvelope import IWorkspaceEnvelope
from scaralang.core.service.kinematics.provides import KinematicsProvides
from scaralang.core.service.kinematics.solver.planar.isolver import IPlanarKinematicsSolver
from scaralang.core.service.kinematics.solver.spatial.isolver import ISpatialKinematicsSolver
from scaralang.core.service.kinematics.workspace.ievaluator import IWorkspaceBoundsEvaluator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.9'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestKinematicsProvides(TestCase):
    '''
        Test cases verifying KinematicsProvides behavior and immutability.

        It defines:

            :methods:
                | test_instantiation_and_attributes - Verifies initialization and fields.
                | test_immutability - Verifies frozen dataclass immutability.
    '''

    def test_instantiation_and_attributes(self) -> None:
        '''Verifies initialization and fields.'''
        mock_envelope = MagicMock(spec=IWorkspaceEnvelope)
        mock_planar = MagicMock(spec=IPlanarKinematicsSolver)
        mock_spatial = MagicMock(spec=ISpatialKinematicsSolver)
        mock_workspace = MagicMock(spec=IWorkspaceBoundsEvaluator)

        provides = KinematicsProvides(
            envelope=mock_envelope,
            planar=mock_planar,
            spatial=mock_spatial,
            workspace=mock_workspace,
        )
        self.assertIs(provides.envelope, mock_envelope)
        self.assertIs(provides.planar, mock_planar)
        self.assertIs(provides.spatial, mock_spatial)
        self.assertIs(provides.workspace, mock_workspace)

    def test_immutability(self) -> None:
        '''Verifies frozen dataclass immutability.'''
        mock_envelope = MagicMock(spec=IWorkspaceEnvelope)
        mock_planar = MagicMock(spec=IPlanarKinematicsSolver)
        mock_spatial = MagicMock(spec=ISpatialKinematicsSolver)
        mock_workspace = MagicMock(spec=IWorkspaceBoundsEvaluator)

        provides = KinematicsProvides(
            envelope=mock_envelope,
            planar=mock_planar,
            spatial=mock_spatial,
            workspace=mock_workspace,
        )
        with self.assertRaises(AttributeError):
            provides.planar = mock_planar  # type: ignore[misc]


if __name__ == '__main__':
    main()
