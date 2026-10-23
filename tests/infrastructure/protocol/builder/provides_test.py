# -*- coding: UTF-8 -*-

'''
Module
    provides_test.py
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
    Unit tests for BuilderProvides dataclass container.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.service.protocol.iactuator_builder import IBinaryActuatorFrameBuilder
from scaralang.core.service.protocol.ipacker import IBinaryFramePacker
from scaralang.core.service.protocol.imotion_builder import IBinaryMotionFrameBuilder
from scaralang.core.service.protocol.isystem_builder import IBinarySystemFrameBuilder
from scaralang.infrastructure.protocol.builder.actuator import BinaryActuatorFrameBuilder
from scaralang.infrastructure.protocol.builder.motion import BinaryMotionFrameBuilder
from scaralang.infrastructure.protocol.builder.packer import BinaryFramePacker
from scaralang.infrastructure.protocol.builder.provides import BuilderProvides
from scaralang.infrastructure.protocol.builder.system import BinarySystemFrameBuilder

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestBuilderProvides(TestCase):
    '''
        Test cases verifying BuilderProvides dataclass.

        It defines:

            :methods:
                | test_builder_provides_attributes - Verifies attributes and typing.
                | test_builder_provides_immutability - Verifies frozen behavior.
    '''

    def test_builder_provides_attributes(self) -> None:
        '''
            Tests BuilderProvides holds valid protocol instances.

            :exceptions: None.
        '''
        packer = BinaryFramePacker()
        motion = BinaryMotionFrameBuilder(packer=packer)
        actuator = BinaryActuatorFrameBuilder(packer=packer)
        system = BinarySystemFrameBuilder(packer=packer)

        provides = BuilderProvides(
            packer=packer,
            motion=motion,
            actuator=actuator,
            system=system,
        )

        self.assertIs(provides.packer, packer)
        self.assertIs(provides.motion, motion)
        self.assertIs(provides.actuator, actuator)
        self.assertIs(provides.system, system)

        self.assertIsInstance(provides.packer, IBinaryFramePacker)
        self.assertIsInstance(provides.motion, IBinaryMotionFrameBuilder)
        self.assertIsInstance(provides.actuator, IBinaryActuatorFrameBuilder)
        self.assertIsInstance(provides.system, IBinarySystemFrameBuilder)

    def test_builder_provides_immutability(self) -> None:
        '''
            Tests BuilderProvides is frozen and immutable.

            :exceptions: None.
        '''
        packer = BinaryFramePacker()
        motion = BinaryMotionFrameBuilder(packer=packer)
        actuator = BinaryActuatorFrameBuilder(packer=packer)
        system = BinarySystemFrameBuilder(packer=packer)

        provides = BuilderProvides(
            packer=packer,
            motion=motion,
            actuator=actuator,
            system=system,
        )
        with self.assertRaises(AttributeError):
            provides.packer = packer  # type: ignore[misc]


if __name__ == '__main__':
    main()
