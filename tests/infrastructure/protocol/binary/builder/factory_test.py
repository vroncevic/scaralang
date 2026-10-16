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
    Unit tests for BuilderFactory.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.service.protocol.ibinary_actuator_frame_builder import IBinaryActuatorFrameBuilder
from scaralang.core.service.protocol.ibinary_frame_packer import IBinaryFramePacker
from scaralang.core.service.protocol.ibinary_motion_frame_builder import IBinaryMotionFrameBuilder
from scaralang.core.service.protocol.ibinary_system_frame_builder import IBinarySystemFrameBuilder
from scaralang.infrastructure.protocol.binary.builder.actuator import BinaryActuatorFrameBuilder
from scaralang.infrastructure.protocol.binary.builder.factory import BuilderFactory
from scaralang.infrastructure.protocol.binary.builder.motion import BinaryMotionFrameBuilder
from scaralang.infrastructure.protocol.binary.builder.packer import BinaryFramePacker
from scaralang.infrastructure.protocol.binary.builder.provides import BuilderProvides
from scaralang.infrastructure.protocol.binary.builder.system import BinarySystemFrameBuilder

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.9'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestBuilderFactory(TestCase):
    '''
        Test suite verifying BuilderFactory instantiation and versioning.

        It defines:

            :methods:
                | test_create - Verifies BuilderProvides creation.
                | test_structural_typing - Verifies instances satisfy protocols.
                | test_get_version - Verifies version string retrieval.
    '''

    def test_create(self) -> None:
        '''
            Verifies factory creates a valid BuilderProvides instance.

            :exceptions: None.
        '''
        provides: BuilderProvides = BuilderFactory.create()
        self.assertIsInstance(provides, BuilderProvides)
        self.assertIsInstance(provides.packer, BinaryFramePacker)
        self.assertIsInstance(provides.motion, BinaryMotionFrameBuilder)
        self.assertIsInstance(provides.actuator, BinaryActuatorFrameBuilder)
        self.assertIsInstance(provides.system, BinarySystemFrameBuilder)

    def test_structural_typing(self) -> None:
        '''
            Verifies created builders satisfy respective protocols.

            :exceptions: None.
        '''
        provides: BuilderProvides = BuilderFactory.create()
        self.assertIsInstance(provides.packer, IBinaryFramePacker)
        self.assertIsInstance(provides.motion, IBinaryMotionFrameBuilder)
        self.assertIsInstance(provides.actuator, IBinaryActuatorFrameBuilder)
        self.assertIsInstance(provides.system, IBinarySystemFrameBuilder)

    def test_get_version(self) -> None:
        '''
            Verifies factory returns a valid semantic version string.

            :exceptions: None.
        '''
        version: str = BuilderFactory.get_version()
        self.assertIsInstance(version, str)
        self.assertGreater(len(version), 0)


if __name__ == '__main__':
    main()
