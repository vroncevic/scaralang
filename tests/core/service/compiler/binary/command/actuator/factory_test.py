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
    Unit tests for ActuatorFrameBuilderFactory.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.service.compiler.binary.command.actuator.dependencies import ActuatorDependencies
from scaralang.core.service.compiler.binary.command.actuator.factory import ActuatorFrameBuilderFactory
from scaralang.core.service.compiler.binary.command.actuator.ibuilder import IActuatorFrameBuilder
from scaralang.core.service.protocol.iactuator_builder import IBinaryActuatorFrameBuilder
from scaralang.infrastructure.protocol.builder.factory import BuilderFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestActuatorFrameBuilderFactory(TestCase):
    '''
        Test cases verifying ActuatorFrameBuilderFactory.

        It defines:

            :methods:
                | test_create - Verifies factory returns IActuatorFrameBuilder.
                | test_get_version - Verifies factory version string.
    '''

    def test_create(self) -> None:
        '''Verifies create returns conforming IActuatorFrameBuilder instance.'''
        frame_builder: IBinaryActuatorFrameBuilder = (
            BuilderFactory.create().actuator
        )
        deps = ActuatorDependencies(frame_builder=frame_builder)
        actuator_builder = ActuatorFrameBuilderFactory.create(dependencies=deps)
        self.assertIsInstance(actuator_builder, IActuatorFrameBuilder)

    def test_get_version(self) -> None:
        '''Verifies factory version returns valid string.'''
        version = ActuatorFrameBuilderFactory.get_version()
        self.assertIsInstance(version, str)
        self.assertEqual(version, '1.1.0')


if __name__ == '__main__':
    main()
