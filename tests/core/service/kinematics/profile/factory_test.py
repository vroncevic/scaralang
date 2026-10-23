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
    Unit tests for ProfileFactory dictionary configuration instantiation.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.model.kinematics.profile.bounds import ScaraBounds
from scaralang.core.model.kinematics.profile.transmission import TransmissionParameters
from scaralang.core.service.kinematics.profile.factory import ProfileFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestProfileFactory(TestCase):
    '''
        Test cases verifying ProfileFactory creation methods.

        It defines:

            :methods:
                | test_create_bounds_from_empty_dict - Verifies defaults on empty mapping.
                | test_create_bounds_from_custom_dict - Verifies bounds with custom mapping.
                | test_create_bounds_with_explicit_deadzone - Verifies precalculated deadzone.
                | test_create_transmission_from_empty_dict - Verifies transmission defaults.
                | test_create_transmission_from_custom_dict - Verifies custom transmission.
                | test_get_version - Verifies factory version string.
    '''

    def test_create_bounds_from_empty_dict(self) -> None:
        '''
            Verifies default ScaraBounds when empty mapping is supplied.
        '''
        bounds: ScaraBounds = ProfileFactory.create_bounds_from_dict({})
        self.assertEqual(bounds.links.l1, 150.0)
        self.assertEqual(bounds.links.l2, 150.0)
        self.assertAlmostEqual(bounds.singularity.deadzone_r_min, 77.646, places=2)

    def test_create_bounds_from_custom_dict(self) -> None:
        '''
            Verifies custom ScaraBounds values parsed from dictionary.
        '''
        data: dict[str, object] = {
            'l1': 160.0,
            'l2': 140.0,
            'z_min': -10.0,
            'z_max': 90.0,
            'min_speed': 2.0,
            'max_speed': 300.0,
            'default_speed': 60.0,
            'default_accel': 150.0,
            'max_accel': 600.0,
            'j1_min_rad': -2.5,
            'j1_max_rad': 2.5,
            'j2_min_rad': -2.4,
            'j2_max_rad': 2.4,
            'singularity_outer_margin_mm': 4.0,
            'singularity_inner_margin_mm': 4.0,
            'singularity_theta2_min_rad': 0.1,
        }
        bounds: ScaraBounds = ProfileFactory.create_bounds_from_dict(data)
        self.assertEqual(bounds.links.l1, 160.0)
        self.assertEqual(bounds.links.l2, 140.0)
        self.assertEqual(bounds.vertical.z_min, -10.0)
        self.assertEqual(bounds.vertical.z_max, 90.0)
        self.assertEqual(bounds.speeds.min_speed, 2.0)
        self.assertEqual(bounds.speeds.max_speed, 300.0)
        self.assertEqual(bounds.speeds.default_speed, 60.0)
        self.assertEqual(bounds.speeds.default_accel, 150.0)
        self.assertEqual(bounds.speeds.max_accel, 600.0)
        self.assertEqual(bounds.joints.j1_min_rad, -2.5)
        self.assertEqual(bounds.joints.j1_max_rad, 2.5)
        self.assertEqual(bounds.joints.j2_min_rad, -2.4)
        self.assertEqual(bounds.joints.j2_max_rad, 2.4)
        self.assertEqual(bounds.singularity.singularity_outer_margin_mm, 4.0)
        self.assertEqual(bounds.singularity.singularity_inner_margin_mm, 4.0)
        self.assertEqual(bounds.singularity.singularity_theta2_min_rad, 0.1)
        self.assertTrue(bounds.singularity.deadzone_r_min > 20.0)

    def test_create_bounds_with_explicit_deadzone(self) -> None:
        '''
            Verifies that explicit positive deadzone_r_min overrides calculated value.
        '''
        data: dict[str, object] = {
            'l1': 150.0,
            'l2': 150.0,
            'j2_max_rad': 2.6,
            'deadzone_r_min': 85.5,
        }
        bounds: ScaraBounds = ProfileFactory.create_bounds_from_dict(data)
        self.assertEqual(bounds.singularity.deadzone_r_min, 85.5)

    def test_create_transmission_from_empty_dict(self) -> None:
        '''
            Verifies default TransmissionParameters when empty mapping is supplied.
        '''
        trans: TransmissionParameters = (
            ProfileFactory.create_transmission_from_dict({})
        )
        self.assertEqual(trans.steps_per_rev, 200.0)
        self.assertEqual(trans.microstepping, 16.0)
        self.assertEqual(trans.gear_ratio_j1, 4.0)
        self.assertEqual(trans.gear_ratio_j2, 4.0)
        self.assertEqual(trans.gear_ratio_j4, 1.0)
        self.assertEqual(trans.leadscrew_pitch_z, 8.0)

    def test_create_transmission_from_custom_dict(self) -> None:
        '''
            Verifies custom TransmissionParameters values parsed from dictionary.
        '''
        data: dict[str, object] = {
            'steps_per_rev': 400.0,
            'microstepping': 32.0,
            'gear_ratio_j1': 5.0,
            'gear_ratio_j2': 5.0,
            'gear_ratio_j4': 2.0,
            'leadscrew_pitch_z': 4.0,
        }
        trans: TransmissionParameters = (
            ProfileFactory.create_transmission_from_dict(data)
        )
        self.assertEqual(trans.steps_per_rev, 400.0)
        self.assertEqual(trans.microstepping, 32.0)
        self.assertEqual(trans.gear_ratio_j1, 5.0)
        self.assertEqual(trans.gear_ratio_j2, 5.0)
        self.assertEqual(trans.gear_ratio_j4, 2.0)
        self.assertEqual(trans.leadscrew_pitch_z, 4.0)

    def test_get_version(self) -> None:
        '''
            Verifies factory version string format.
        '''
        version: str = ProfileFactory.get_version()
        self.assertTrue(isinstance(version, str))
        self.assertTrue(len(version) > 0)


if __name__ == '__main__':
    main()
