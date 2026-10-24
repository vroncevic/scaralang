# -*- coding: UTF-8 -*-

'''
Module
    transmission_test.py
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
    Unit tests for TransmissionParameters kinematics domain model.
'''

from __future__ import annotations

from dataclasses import FrozenInstanceError
from unittest import TestCase, main

from scaralang.core.model.kinematics.profile.transmission import TransmissionParameters

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TransmissionTest(TestCase):
    '''
        Unit tests validating TransmissionParameters purity, immutability, and attribute values.

        It defines:

            :methods:
                | test_instantiation_and_attributes - Verifies field values on initialization.
                | test_frozen_immutability - Verifies frozen dataclass prevents mutation.
    '''

    def test_instantiation_and_attributes(self) -> None:
        '''
            Verify proper initialization and access of TransmissionParameters fields.

            :exceptions: None.
        '''
        params = TransmissionParameters(
            steps_per_rev=200.0,
            microstepping=16.0,
            gear_ratio_j1=4.0,
            gear_ratio_j2=2.0,
            gear_ratio_j4=1.0,
            leadscrew_pitch_z=8.0,
        )
        self.assertEqual(params.steps_per_rev, 200.0)
        self.assertEqual(params.microstepping, 16.0)
        self.assertEqual(params.gear_ratio_j1, 4.0)
        self.assertEqual(params.gear_ratio_j2, 2.0)
        self.assertEqual(params.gear_ratio_j4, 1.0)
        self.assertEqual(params.leadscrew_pitch_z, 8.0)

    def test_frozen_immutability(self) -> None:
        '''
            Verify that modifying attributes raises FrozenInstanceError.

            :exceptions: None.
        '''
        params = TransmissionParameters(
            steps_per_rev=200.0,
            microstepping=16.0,
            gear_ratio_j1=4.0,
            gear_ratio_j2=2.0,
            gear_ratio_j4=1.0,
            leadscrew_pitch_z=8.0,
        )
        with self.assertRaises(FrozenInstanceError):
            setattr(params, 'steps_per_rev', 400.0)


if __name__ == '__main__':
    main()
