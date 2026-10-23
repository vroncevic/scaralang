# -*- coding: UTF-8 -*-

'''
Module
    decompiler_test.py
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
    Unit tests for ScaraDecompiler service.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.model.protocol.frame import BinaryFrame
from scaralang.core.model.protocol.message import MessageId
from scaralang.core.service.decompiler.decompiler import ScaraDecompiler
from scaralang.core.service.decompiler.frame.dependencies import FrameDependencies
from scaralang.core.service.decompiler.frame.factory import FrameFactory
from scaralang.core.service.decompiler.frame.provides import FrameProvides
from scaralang.core.service.decompiler.idecompiler import IScaraDecompiler
from scaralang.core.service.kinematics.profile.default_scara_profile import DefaultScaraProfile
from scaralang.core.service.kinematics.transmission.factory import TransmissionFactory
from scaralang.infrastructure.protocol.builder.factory import BuilderFactory
from scaralang.infrastructure.protocol.parser.factory import ParserFactory
from scaralang.infrastructure.kinematics.factory import DefaultKinematicsFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestScaraDecompiler(TestCase):
    '''Test suite verifying ScaraDecompiler binary stream translation operations.'''

    def setUp(self) -> None:
        '''Initializes parser, frame decompiler, and decompiler fixtures.'''
        kinematics = DefaultKinematicsFactory.create()
        transmission = TransmissionFactory.create(
            transmission=DefaultScaraProfile.create_transmission()
        )
        parser_provides = ParserFactory.create()
        frame_provides: FrameProvides = FrameFactory.create(
            dependencies=FrameDependencies(
                planar=kinematics.planar,
                transmission=transmission,
                motion_unpacker=parser_provides.motion_unpacker,
                actuator_unpacker=parser_provides.actuator_unpacker,
            )
        )
        parser = parser_provides.parser
        self.decompiler: ScaraDecompiler = ScaraDecompiler(
            parser=parser,
            frame_decompiler=frame_provides.decompiler,
        )

    def test_implements_protocol(self) -> None:
        '''Verifies structural protocol compliance.'''
        self.assertTrue(isinstance(self.decompiler, IScaraDecompiler))

    def test_get_version(self) -> None:
        '''Verifies scara decompiler version string retrieval.'''
        self.assertEqual(self.decompiler.get_version(), '1.1.0')

    def test_decompile_empty_data(self) -> None:
        '''Verifies empty byte data returns empty string.'''
        self.assertEqual(self.decompiler.decompile_bytes(data=b''), '')

    def test_decompile_empty_frames(self) -> None:
        '''Verifies empty frame tuple returns empty string.'''
        self.assertEqual(self.decompiler.decompile_frames(frames=()), '')

    def test_decompile_frames(self) -> None:
        '''Verifies decompiling tuple of BinaryFrames into DSL script.'''
        frames = (
            BinaryFrame(seq_num=1, msg_id=MessageId.CMD_HOME, payload=b'', crc16=0),
            BinaryFrame(seq_num=2, msg_id=MessageId.CMD_ENABLE, payload=b'', crc16=0),
        )
        script: str = self.decompiler.decompile_frames(frames=frames)
        self.assertIn('HOME', script)
        self.assertIn('ENABLE', script)
        self.assertIn('# Frame Count: 2', script)

    def test_decompile_bytes_roundtrip(self) -> None:
        '''Verifies building wire bytes and decompiling back to DSL script.'''
        builder_provides = BuilderFactory.create()
        frame: BinaryFrame = builder_provides.system.build_system_cmd(msg_id=MessageId.CMD_HOME, seq_num=1)
        raw_bytes: bytes = builder_provides.packer.pack_frame(frame=frame)
        script: str = self.decompiler.decompile_bytes(data=raw_bytes)
        self.assertIn('HOME', script)
        self.assertIn('# Frame Count: 1', script)


if __name__ == '__main__':
    main()
