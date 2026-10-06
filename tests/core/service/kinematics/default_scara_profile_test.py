# -*- coding: UTF-8 -*-

'''
Module
    default_scara_profile_test.py
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
    Unit tests for DefaultScaraProfile kinematics and transmission profiles.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.model.kinematics.scara_bounds import ScaraBounds
from scaralang.core.model.kinematics.transmission_parameters import TransmissionParameters
from scaralang.core.service.kinematics.default_scara_profile import DefaultScaraProfile

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.6'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestDefaultScaraProfile(TestCase):
    '''
        Test cases verifying DefaultScaraProfile factory methods.

        It defines:

            :methods:
                | test_create_bounds - Verifies generated default ScaraBounds.
                | test_create_transmission - Verifies generated default TransmissionParameters.
                | test_get_version - Verifies profile version string.
    '''

    def test_create_bounds(self) -> None:
        '''
            Verifies default bounds configuration parameters.
        '''
        bounds: ScaraBounds = DefaultScaraProfile.create_bounds()
        self.assertIsInstance(bounds, ScaraBounds)
        self.assertEqual(bounds.links.l1, 150.0)
        self.assertEqual(bounds.links.l2, 150.0)
        self.assertEqual(bounds.vertical.z_min, -50.0)
        self.assertEqual(bounds.vertical.z_max, 50.0)
        self.assertEqual(bounds.speeds.default_speed, 50.0)
        self.assertEqual(bounds.speeds.default_accel, 100.0)
        self.assertEqual(bounds.singularity.deadzone_r_min, 20.0)

    def test_create_transmission(self) -> None:
        '''
            Verifies default transmission configuration parameters.
        '''
        transmission: TransmissionParameters = (
            DefaultScaraProfile.create_transmission()
        )
        self.assertIsInstance(transmission, TransmissionParameters)
        self.assertEqual(transmission.steps_per_rev, 200.0)
        self.assertEqual(transmission.microstepping, 16.0)
        self.assertEqual(transmission.gear_ratio_j1, 4.0)
        self.assertEqual(transmission.gear_ratio_j2, 2.0)
        self.assertEqual(transmission.gear_ratio_j4, 1.0)
        self.assertEqual(transmission.leadscrew_pitch_z, 8.0)

    def test_get_version(self) -> None:
        '''
            Verifies profile version string is present.
        '''
        version: str = DefaultScaraProfile.get_version()
        self.assertTrue(bool(version))


if __name__ == '__main__':
    main()
