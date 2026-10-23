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
    Unit tests for UnpackerFactory.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.service.protocol.iactuator_unpacker import IBinaryActuatorPayloadUnpacker
from scaralang.core.service.protocol.imotion_unpacker import IBinaryMotionPayloadUnpacker
from scaralang.core.service.protocol.iresponse_unpacker import IBinaryResponsePayloadUnpacker
from scaralang.core.service.protocol.isystem_unpacker import IBinarySystemPayloadUnpacker
from scaralang.infrastructure.protocol.parser.unpacker.actuator import BinaryActuatorPayloadUnpacker
from scaralang.infrastructure.protocol.parser.unpacker.factory import UnpackerFactory
from scaralang.infrastructure.protocol.parser.unpacker.motion import BinaryMotionPayloadUnpacker
from scaralang.infrastructure.protocol.parser.unpacker.provides import UnpackerProvides
from scaralang.infrastructure.protocol.parser.unpacker.response import BinaryResponsePayloadUnpacker
from scaralang.infrastructure.protocol.parser.unpacker.system import BinarySystemPayloadUnpacker

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestUnpackerFactory(TestCase):
    '''
        Test suite verifying UnpackerFactory instantiation and versioning.

        It defines:

            :methods:
                | test_create - Verifies UnpackerProvides creation.
                | test_structural_typing - Verifies instances satisfy protocols.
                | test_get_version - Verifies version string retrieval.
    '''

    def test_create(self) -> None:
        '''
            Verifies factory creates a valid UnpackerProvides instance.

            :exceptions: None.
        '''
        provides: UnpackerProvides = UnpackerFactory.create()
        self.assertIsInstance(provides, UnpackerProvides)
        self.assertIsInstance(provides.motion, BinaryMotionPayloadUnpacker)
        self.assertIsInstance(provides.actuator, BinaryActuatorPayloadUnpacker)
        self.assertIsInstance(provides.system, BinarySystemPayloadUnpacker)
        self.assertIsInstance(provides.response, BinaryResponsePayloadUnpacker)

    def test_structural_typing(self) -> None:
        '''
            Verifies created unpackers satisfy respective protocols.

            :exceptions: None.
        '''
        provides: UnpackerProvides = UnpackerFactory.create()
        self.assertIsInstance(provides.motion, IBinaryMotionPayloadUnpacker)
        self.assertIsInstance(provides.actuator, IBinaryActuatorPayloadUnpacker)
        self.assertIsInstance(provides.system, IBinarySystemPayloadUnpacker)
        self.assertIsInstance(provides.response, IBinaryResponsePayloadUnpacker)

    def test_get_version(self) -> None:
        '''
            Verifies factory returns a valid semantic version string.

            :exceptions: None.
        '''
        version: str = UnpackerFactory.get_version()
        self.assertIsInstance(version, str)
        self.assertGreater(len(version), 0)


if __name__ == '__main__':
    main()
