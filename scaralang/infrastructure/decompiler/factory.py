# -*- coding: UTF-8 -*-

'''
Module
    factory.py
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
    Factory providing default full-stack ScaraDecompiler composition.
'''

from __future__ import annotations

from scaralang.core.service.decompiler.dependencies import DecompilerDependencies
from scaralang.core.service.decompiler.factory import DecompilerFactory
from scaralang.core.service.decompiler.frame.dependencies import FrameDependencies
from scaralang.core.service.decompiler.frame.factory import FrameFactory
from scaralang.core.service.decompiler.frame.provides import FrameProvides
from scaralang.core.service.decompiler.idecompiler import IScaraDecompiler
from scaralang.core.service.decompiler.provides import DecompilerProvides
from scaralang.core.service.kinematics.profile.default_scara_profile import DefaultScaraProfile
from scaralang.core.service.kinematics.transmission.factory import JointStepTransmissionConverterFactory
from scaralang.infrastructure.kinematics.factory import DefaultKinematicsFactory
from scaralang.infrastructure.communication.protocol.binary.parser.binary_frame_parser_factory import BinaryFrameParserFactory
from scaralang.infrastructure.communication.protocol.binary.parser.binary_payload_unpacker_factory import BinaryPayloadUnpackerFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.8'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DefaultDecompilerFactory:
    '''
        Factory providing default full-stack ScaraDecompiler composition.

        It defines:

            :methods:
                | create - Builds and returns an IScaraDecompiler with standard defaults.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(cls) -> IScaraDecompiler:
        '''
            Builds and returns an IScaraDecompiler with standard defaults.

            :return: Fully configured IScaraDecompiler protocol instance.
            :exceptions: None.
        '''
        parser = BinaryFrameParserFactory.create_default()
        kinematics = DefaultKinematicsFactory.create().service
        transmission = JointStepTransmissionConverterFactory.create(
            transmission=DefaultScaraProfile.create_transmission()
        )
        unpacker = BinaryPayloadUnpackerFactory.create()

        frame_provides: FrameProvides = FrameFactory.create(
            dependencies=FrameDependencies(
                kinematics=kinematics,
                transmission=transmission,
                unpacker=unpacker,
            )
        )
        decompiler_provides: DecompilerProvides = DecompilerFactory.create(
            dependencies=DecompilerDependencies(
                parser=parser,
                frame_decompiler=frame_provides.decompiler,
            )
        )
        return decompiler_provides.decompiler

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns factory version string representation.

            :return: Factory version string.
            :exceptions: None.
        '''
        return __version__
