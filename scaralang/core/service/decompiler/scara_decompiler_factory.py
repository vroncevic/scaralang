# -*- coding: UTF-8 -*-

'''
Module
    scara_decompiler_factory.py
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
    Factory service constructing ScaraDecompiler instances.
'''

from __future__ import annotations

from scaralang.core.service.decompiler.frame_decompiler_factory import FrameDecompilerFactory
from scaralang.core.service.decompiler.iframe_decompiler import IFrameDecompiler
from scaralang.core.service.decompiler.scara_decompiler import ScaraDecompiler
from scaralang.core.service.kinematics.default_scara_profile import DefaultScaraProfile
from scaralang.core.service.kinematics.kinematics_service_factory import KinematicsServiceFactory
from scaralang.core.service.kinematics.transmission.joint_step_transmission_converter_factory import JointStepTransmissionConverterFactory
from scaralang.core.service.protocol.ibinary_frame_parser import IBinaryFrameParser
from scaralang.infrastructure.communication.protocol.binary.parser.binary_frame_parser_factory import BinaryFrameParserFactory
from scaralang.infrastructure.communication.protocol.binary.parser.binary_payload_unpacker_factory import BinaryPayloadUnpackerFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.7'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ScaraDecompilerFactory:
    '''
        Factory providing instantiation of ScaraDecompiler service.

        It defines:

            :methods:
                | create - Instantiates configured ScaraDecompiler.
                | create_default - Instantiates ScaraDecompiler with standard defaults.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(
        cls,
        *,
        parser: IBinaryFrameParser,
        frame_decompiler: IFrameDecompiler,
    ) -> ScaraDecompiler:
        '''
            Instantiates configured ScaraDecompiler service.

            :param parser: Required IBinaryFrameParser implementation.
            :param frame_decompiler: Required IFrameDecompiler implementation.
            :return: Fully configured ScaraDecompiler instance.
            :exceptions: None.
        '''
        return ScaraDecompiler(
            parser=parser,
            frame_decompiler=frame_decompiler,
        )

    @classmethod
    def create_default(cls) -> ScaraDecompiler:
        '''
            Instantiates ScaraDecompiler service with default collaborators.

            :return: Fully configured ScaraDecompiler instance.
            :exceptions: None.
        '''
        parser = BinaryFrameParserFactory.create_default()
        bounds = DefaultScaraProfile.create_bounds()
        kinematics = KinematicsServiceFactory.create(bounds=bounds)
        transmission = JointStepTransmissionConverterFactory.create_default()
        unpacker = BinaryPayloadUnpackerFactory.create()
        frame_decompiler = FrameDecompilerFactory.create(
            kinematics=kinematics,
            transmission=transmission,
            unpacker=unpacker,
        )

        return ScaraDecompiler(
            parser=parser,
            frame_decompiler=frame_decompiler,
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory version string.

            :return: Factory version string.
            :exceptions: None.
        '''
        return __version__
