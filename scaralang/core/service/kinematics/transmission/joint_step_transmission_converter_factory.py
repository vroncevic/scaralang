# -*- coding: UTF-8 -*-

'''
Module
    joint_step_transmission_converter_factory.py
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
    Factory instantiating JointStepTransmissionConverter component.
'''

from __future__ import annotations

from scaralang.core.model.kinematics.transmission_parameters import TransmissionParameters
from scaralang.core.service.kinematics.default_scara_profile import DefaultScaraProfile
from scaralang.core.service.kinematics.transmission.ijoint_step_transmission_converter import IJointStepTransmissionConverter
from scaralang.core.service.kinematics.transmission.joint_step_transmission_converter import JointStepTransmissionConverter

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class JointStepTransmissionConverterFactory:
    '''
        Factory instantiating JointStepTransmissionConverter component.

        It defines:

            :methods:
                | create - Instantiates converter with transmission parameters.
                | create_default - Instantiates converter with default transmission parameters.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(
        cls,
        *,
        transmission: TransmissionParameters
    ) -> IJointStepTransmissionConverter:
        '''
            Instantiates converter with transmission parameters.

            :param transmission: Injected TransmissionParameters instance.
            :return: IJointStepTransmissionConverter protocol instance.
            :exceptions: None.
        '''
        return JointStepTransmissionConverter(transmission=transmission)

    @classmethod
    def create_default(cls) -> IJointStepTransmissionConverter:
        '''
            Instantiates converter with default TransmissionParameters profile.

            :return: IJointStepTransmissionConverter protocol instance.
            :exceptions: None.
        '''
        return cls.create(transmission=DefaultScaraProfile.create_transmission())

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory version string.

            :return: Factory version string.
            :exceptions: None.
        '''
        return __version__
