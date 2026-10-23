# -*- coding: UTF-8 -*-

'''
Module
    factory_test.py
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
    Unit tests for DecompilerFactory.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.service.decompiler.dependencies import DecompilerDependencies
from scaralang.core.service.decompiler.factory import DecompilerFactory
from scaralang.core.service.decompiler.frame.dependencies import FrameDependencies
from scaralang.core.service.decompiler.frame.factory import FrameFactory
from scaralang.core.service.decompiler.frame.provides import FrameProvides
from scaralang.core.service.decompiler.idecompiler import IScaraDecompiler
from scaralang.core.service.decompiler.provides import DecompilerProvides
from scaralang.core.service.kinematics.profile.default_scara_profile import DefaultScaraProfile
from scaralang.core.service.kinematics.transmission.factory import TransmissionFactory
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


class TestDecompilerFactory(TestCase):
    '''Test suite verifying DecompilerFactory instantiation and versioning.'''

    def test_create(self) -> None:
        '''Verifies factory creates configured DecompilerProvides instance with IScaraDecompiler.'''
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
        dependencies = DecompilerDependencies(
            parser=parser,
            frame_decompiler=frame_provides.decompiler,
        )
        provides: DecompilerProvides = DecompilerFactory.create(dependencies=dependencies)
        self.assertIsInstance(provides, DecompilerProvides)
        self.assertIsInstance(provides.decompiler, IScaraDecompiler)

    def test_get_version(self) -> None:
        '''Verifies factory version string retrieval.'''
        self.assertEqual(DecompilerFactory.get_version(), '1.1.0')


if __name__ == '__main__':
    main()
