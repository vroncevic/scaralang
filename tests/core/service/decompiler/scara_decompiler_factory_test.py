# -*- coding: UTF-8 -*-

'''
Module
    scara_decompiler_factory_test.py
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
    Unit tests for ScaraDecompilerFactory.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.service.decompiler.frame_decompiler_factory import FrameDecompilerFactory
from scaralang.core.service.decompiler.scara_decompiler import ScaraDecompiler
from scaralang.core.service.decompiler.scara_decompiler_factory import ScaraDecompilerFactory
from scaralang.core.service.kinematics.kinematics_service_factory import KinematicsServiceFactory
from scaralang.core.service.kinematics.transmission.joint_step_transmission_converter_factory import JointStepTransmissionConverterFactory
from scaralang.infrastructure.communication.protocol.binary.parser.binary_frame_parser_factory import BinaryFrameParserFactory
from scaralang.infrastructure.communication.protocol.binary.parser.binary_payload_unpacker_factory import BinaryPayloadUnpackerFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.6'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestScaraDecompilerFactory(TestCase):
    '''Test suite verifying ScaraDecompilerFactory instantiation and versioning.'''

    def test_create(self) -> None:
        '''Verifies factory creates configured ScaraDecompiler instance.'''
        kinematics = KinematicsServiceFactory.create_default()
        transmission = JointStepTransmissionConverterFactory.create_default()
        unpacker = BinaryPayloadUnpackerFactory.create()
        frame_decompiler = FrameDecompilerFactory.create(
            kinematics=kinematics,
            transmission=transmission,
            unpacker=unpacker,
        )
        parser = BinaryFrameParserFactory.create()
        decompiler: ScaraDecompiler = ScaraDecompilerFactory.create(
            parser=parser,
            frame_decompiler=frame_decompiler,
        )
        self.assertIsInstance(decompiler, ScaraDecompiler)

    def test_create_default(self) -> None:
        '''Verifies factory creates default ScaraDecompiler instance.'''
        decompiler: ScaraDecompiler = ScaraDecompilerFactory.create_default()
        self.assertIsInstance(decompiler, ScaraDecompiler)

    def test_get_version(self) -> None:
        '''Verifies factory version string retrieval.'''
        self.assertEqual(ScaraDecompilerFactory.get_version(), '1.0.6')


if __name__ == '__main__':
    main()
