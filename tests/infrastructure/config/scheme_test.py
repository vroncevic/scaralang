# -*- coding: UTF-8 -*-

'''
Module
    scheme_test.py
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
    Unit tests for canonical scara_geometry_scheme.json schema validation.
'''

from __future__ import annotations

from json import load
from os.path import abspath, dirname, exists, join
from unittest import TestCase, main

from scaralang.infrastructure import __file__ as infra_init_file

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestScaraGeometryScheme(TestCase):
    '''
        Test cases verifying canonical scara_geometry_scheme.json definition.

        It defines:

            :methods:
                | test_scheme_file_exists - Verifies schema file is present in config.
                | test_scheme_attributes - Verifies exactly 26 canonical attributes with float types.
    '''

    def test_scheme_file_exists(self) -> None:
        '''
            Verifies schema file is present in package config directory.
        '''
        config_dir: str = join(dirname(abspath(infra_init_file)), 'config')
        scheme_path: str = join(config_dir, 'scara_geometry_scheme.json')
        self.assertTrue(exists(scheme_path))

    def test_scheme_attributes(self) -> None:
        '''
            Verifies schema defines exactly 26 canonical attributes with float types.
        '''
        config_dir: str = join(dirname(abspath(infra_init_file)), 'config')
        scheme_path: str = join(config_dir, 'scara_geometry_scheme.json')
        with open(scheme_path, 'r', encoding='utf-8') as f:
            data: dict[str, str] = load(f)

        self.assertEqual(len(data), 26)
        expected_keys: tuple[str, ...] = (
            'l1', 'l2', 'z_min', 'z_max',
            'min_speed', 'max_speed', 'default_speed', 'default_accel', 'max_accel',
            'j1_min_rad', 'j1_max_rad', 'j2_min_rad', 'j2_max_rad',
            'singularity_outer_margin_mm', 'singularity_inner_margin_mm',
            'singularity_theta2_min_rad', 'deadzone_r_min',
            'home_offset_j1', 'home_offset_j2', 'homing_rate_hz',
            'steps_per_rev', 'microstepping',
            'gear_ratio_j1', 'gear_ratio_j2', 'gear_ratio_j4', 'leadscrew_pitch_z'
        )
        for key in expected_keys:
            self.assertIn(key, data)
            self.assertEqual(data[key], 'float')


if __name__ == '__main__':
    main()
