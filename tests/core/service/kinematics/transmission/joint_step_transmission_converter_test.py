# -*- coding: UTF-8 -*-

'''
Module
    joint_step_transmission_converter_test.py
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
    Unit tests for JointStepTransmissionConverter bidirectional mapping.
'''

from __future__ import annotations

from math import pi
from unittest import TestCase
from unittest import main

from scaralang.core.model.kinematics.transmission_parameters import TransmissionParameters
from scaralang.core.service.kinematics.transmission.ijoint_step_transmission_converter import IJointStepTransmissionConverter
from scaralang.core.service.kinematics.transmission.joint_step_transmission_converter import JointStepTransmissionConverter

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestJointStepTransmissionConverter(TestCase):
    '''
        Test cases verifying JointStepTransmissionConverter conversion accuracy.

        It defines:

            :methods:
                | setUp - Initializes test transmission parameters and converter.
                | test_structural_protocol_conformance - Verifies runtime protocol compliance.
                | test_steps_per_rad - Verifies radian step scaling factor calculation.
                | test_steps_per_mm_z - Verifies linear Z step scaling factor calculation.
                | test_angles_to_steps - Verifies forward conversion from angles to steps.
                | test_steps_to_angles - Verifies reverse conversion from steps to angles.
                | test_round_trip_conversion - Verifies bidirectional mapping accuracy.
    '''

    def setUp(self) -> None:
        '''
            Sets up transmission parameters and converter instance.
        '''
        self.transmission = TransmissionParameters(
            steps_per_rev=200.0,
            microstepping=16.0,
            gear_ratio_j1=4.0,
            gear_ratio_j2=2.0,
            gear_ratio_j4=1.0,
            leadscrew_pitch_z=8.0
        )
        self.converter = JointStepTransmissionConverter(
            transmission=self.transmission
        )

    def test_structural_protocol_conformance(self) -> None:
        '''
            Verifies that converter structurally conforms to IJointStepTransmissionConverter.
        '''
        self.assertIsInstance(self.converter, IJointStepTransmissionConverter)

    def test_steps_per_rad(self) -> None:
        '''
            Verifies steps per radian calculation.
        '''
        # (200 * 16 * 4.0) / (2 * pi) = 12800 / (2 * pi) = 2037.183
        steps_rad_j1: float = self.converter.steps_per_rad(self.transmission.gear_ratio_j1)
        expected_j1: float = (3200.0 * 4.0) / (2.0 * pi)
        self.assertAlmostEqual(steps_rad_j1, expected_j1, places=3)

    def test_steps_per_mm_z(self) -> None:
        '''
            Verifies steps per mm for vertical axis.
        '''
        # (200 * 16) / 8.0 = 3200 / 8 = 400.0 steps/mm
        steps_mm_z: float = self.converter.steps_per_mm_z()
        self.assertEqual(steps_mm_z, 400.0)

    def test_angles_to_steps(self) -> None:
        '''
            Verifies conversion from continuous joint angles to integer motor steps.
        '''
        steps: tuple[int, int, int, int] = self.converter.angles_to_steps(
            0.0, 0.0, 10.0, 0.0
        )
        self.assertEqual(steps[0], 0)
        self.assertEqual(steps[1], 0)
        self.assertEqual(steps[2], 4000)
        self.assertEqual(steps[3], 0)

    def test_steps_to_angles(self) -> None:
        '''
            Verifies conversion from motor steps to continuous joint angles.
        '''
        angles: tuple[float, float, float, float] = self.converter.steps_to_angles(
            0, 0, 4000, 0
        )
        self.assertAlmostEqual(angles[0], 0.0, places=5)
        self.assertAlmostEqual(angles[1], 0.0, places=5)
        self.assertAlmostEqual(angles[2], 10.0, places=5)
        self.assertAlmostEqual(angles[3], 0.0, places=5)

    def test_round_trip_conversion(self) -> None:
        '''
            Verifies bidirectional round-trip conversion fidelity.
        '''
        orig_th1: float = 0.5
        orig_th2: float = -0.75
        orig_z: float = 25.5
        orig_th4: float = 1.2

        steps: tuple[int, int, int, int] = self.converter.angles_to_steps(
            orig_th1, orig_th2, orig_z, orig_th4
        )
        recovered: tuple[float, float, float, float] = self.converter.steps_to_angles(
            *steps
        )

        self.assertAlmostEqual(recovered[0], orig_th1, places=3)
        self.assertAlmostEqual(recovered[1], orig_th2, places=3)
        self.assertAlmostEqual(recovered[2], orig_z, places=3)
        self.assertAlmostEqual(recovered[3], orig_th4, places=3)


if __name__ == '__main__':
    main()
