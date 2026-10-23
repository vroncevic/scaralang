# -*- coding: UTF-8 -*-

'''
Module
    envelope_test.py
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
    Unit tests for WorkspaceEnvelope geometry and operational reach metrics.
'''

from __future__ import annotations

from unittest import TestCase, main

from scaralang.core.model.kinematics.profile.bounds import ScaraBounds
from scaralang.core.service.kinematics.envelope.envelope import WorkspaceEnvelope
from scaralang.core.service.kinematics.envelope.ienvelope import IWorkspaceEnvelope
from scaralang.core.service.kinematics.profile.default_scara_profile import DefaultScaraProfile

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestWorkspaceEnvelope(TestCase):
    '''
        Validates WorkspaceEnvelope reach radii and structural protocol conformance.

        It defines:

            :methods:
                | setUp - Initializes bounds and envelope instance.
                | test_structural_conformance - Verifies conformance to IWorkspaceEnvelope.
                | test_radii_calculations - Verifies r_min, r_max, and safe_r_max.
                | test_get_version - Verifies version string.
    '''

    def setUp(self) -> None:
        '''Initializes standard bounds and WorkspaceEnvelope instance.'''
        self.bounds: ScaraBounds = DefaultScaraProfile.create_bounds()
        self.envelope: WorkspaceEnvelope = WorkspaceEnvelope(bounds=self.bounds)

    def test_structural_conformance(self) -> None:
        '''Verifies WorkspaceEnvelope conforms structurally to IWorkspaceEnvelope.'''
        self.assertIsInstance(self.envelope, IWorkspaceEnvelope)

    def test_radii_calculations(self) -> None:
        '''Verifies reach radii calculations match link geometry and singularity margins.'''
        expected_r_min: float = max(
            abs(self.bounds.links.l1 - self.bounds.links.l2),
            self.bounds.singularity.deadzone_r_min,
        )
        expected_r_max: float = self.bounds.links.l1 + self.bounds.links.l2
        expected_safe_r_max: float = (
            self.bounds.links.l1
            + self.bounds.links.l2
            - self.bounds.singularity.singularity_outer_margin_mm
        )

        self.assertEqual(self.envelope.bounds, self.bounds)
        self.assertEqual(self.envelope.r_min, expected_r_min)
        self.assertEqual(self.envelope.r_max, expected_r_max)
        self.assertEqual(self.envelope.safe_r_max, expected_safe_r_max)

    def test_get_version(self) -> str:
        '''Verifies semantic version string.'''
        self.assertEqual(self.envelope.get_version(), '1.1.0')


if __name__ == '__main__':
    main()
