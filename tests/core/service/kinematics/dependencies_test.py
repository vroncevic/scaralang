# -*- coding: UTF-8 -*-

'''
Module
    dependencies_test.py
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
    Unit tests for KinematicsDependencies dataclass.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.model.kinematics.solver.dls import DlsConfig
from scaralang.core.model.kinematics.profile.bounds import ScaraBounds
from scaralang.core.service.kinematics.dependencies import KinematicsDependencies
from scaralang.core.service.kinematics.profile.default_scara_profile import DefaultScaraProfile

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestKinematicsDependencies(TestCase):
    '''
        Test cases verifying KinematicsDependencies behavior and immutability.

        It defines:

            :methods:
                | test_instantiation_and_attributes - Verifies initialization and fields.
                | test_immutability - Verifies frozen dataclass immutability.
    '''

    def test_instantiation_and_attributes(self) -> None:
        '''
            Verifies initialization and fields.

            :exceptions: None.
        '''
        bounds: ScaraBounds = DefaultScaraProfile.create_bounds()
        dls_config: DlsConfig = DefaultScaraProfile.create_dls_config()
        deps = KinematicsDependencies(bounds=bounds, dls_config=dls_config)
        self.assertIs(deps.bounds, bounds)
        self.assertIs(deps.dls_config, dls_config)

    def test_immutability(self) -> None:
        '''
            Verifies frozen dataclass immutability.

            :exceptions: None.
        '''
        bounds: ScaraBounds = DefaultScaraProfile.create_bounds()
        dls_config: DlsConfig = DefaultScaraProfile.create_dls_config()
        deps = KinematicsDependencies(bounds=bounds, dls_config=dls_config)
        with self.assertRaises(AttributeError):
            deps.bounds = bounds  # type: ignore[misc]


if __name__ == '__main__':
    main()
