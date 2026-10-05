# -*- coding: UTF-8 -*-

'''
Module
    joint_step_transmission_converter_factory_test.py
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
    Unit tests for JointStepTransmissionConverterFactory.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.model.kinematics.transmission_parameters import TransmissionParameters
from scaralang.core.service.kinematics.transmission.ijoint_step_transmission_converter import IJointStepTransmissionConverter
from scaralang.core.service.kinematics.transmission.joint_step_transmission_converter_factory import JointStepTransmissionConverterFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestJointStepTransmissionConverterFactory(TestCase):
    '''
        Test cases verifying JointStepTransmissionConverterFactory instantiation.

        It defines:

            :methods:
                | test_create - Verifies factory returns IJointStepTransmissionConverter.
                | test_create_default - Verifies default factory returns IJointStepTransmissionConverter.
                | test_get_version - Verifies factory version string.
    '''

    def test_create(self) -> None:
        '''
            Verifies factory produces valid IJointStepTransmissionConverter instance.
        '''
        transmission = TransmissionParameters(
            steps_per_rev=200.0,
            microstepping=16.0,
            gear_ratio_j1=4.0,
            gear_ratio_j2=2.0,
            gear_ratio_j4=1.0,
            leadscrew_pitch_z=8.0
        )
        converter: IJointStepTransmissionConverter = (
            JointStepTransmissionConverterFactory.create(
                transmission=transmission
            )
        )
        self.assertIsInstance(converter, IJointStepTransmissionConverter)

    def test_create_default(self) -> None:
        '''
            Verifies factory produces IJointStepTransmissionConverter via create_default.
        '''
        converter: IJointStepTransmissionConverter = (
            JointStepTransmissionConverterFactory.create_default()
        )
        self.assertIsInstance(converter, IJointStepTransmissionConverter)

    def test_get_version(self) -> None:
        '''
            Verifies factory version string is non-empty.
        '''
        version: str = JointStepTransmissionConverterFactory.get_version()
        self.assertTrue(bool(version))


if __name__ == '__main__':
    main()
