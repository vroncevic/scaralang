# -*- coding: UTF-8 -*-

'''
Module
    frame_decompiler_factory.py
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
    Factory service constructing FrameDecompiler instances.
'''

from __future__ import annotations

from scaralang.core.service.decompiler.frame_decompiler import FrameDecompiler
from scaralang.core.service.kinematics.ikinematics_service import IKinematicsService
from scaralang.core.service.kinematics.transmission.ijoint_step_transmission_converter import IJointStepTransmissionConverter
from scaralang.core.service.protocol.ibinary_payload_unpacker import IBinaryPayloadUnpacker

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.6'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class FrameDecompilerFactory:
    '''
        Factory providing instantiation of FrameDecompiler service.

        It defines:

            :methods:
                | create - Instantiates configured FrameDecompiler.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(
        cls,
        *,
        kinematics: IKinematicsService,
        transmission: IJointStepTransmissionConverter,
        unpacker: IBinaryPayloadUnpacker,
    ) -> FrameDecompiler:
        '''
            Instantiates configured FrameDecompiler service.

            :param kinematics: Required IKinematicsService implementation.
            :param transmission: Required IJointStepTransmissionConverter implementation.
            :param unpacker: Required IBinaryPayloadUnpacker implementation.
            :return: Fully configured FrameDecompiler instance.
            :exceptions: None.
        '''
        return FrameDecompiler(
            kinematics=kinematics,
            transmission=transmission,
            unpacker=unpacker,
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory version string.

            :return: Factory version string.
            :exceptions: None.
        '''
        return __version__
