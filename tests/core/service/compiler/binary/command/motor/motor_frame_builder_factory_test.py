# -*- coding: UTF-8 -*-

'''
Module
    motor_frame_builder_factory_test.py
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
    Unit tests for MotorFrameBuilderFactory.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.service.compiler.binary.command.motor.imotor_frame_builder import IMotorFrameBuilder
from scaralang.core.service.compiler.binary.command.motor.motor_frame_builder_factory import MotorFrameBuilderFactory
from scaralang.core.service.protocol.ibinary_frame_builder import IBinaryFrameBuilder
from scaralang.infrastructure.communication.protocol.binary.builder.binary_frame_builder_factory import BinaryFrameBuilderFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestMotorFrameBuilderFactory(TestCase):
    '''
        Test cases verifying MotorFrameBuilderFactory.

        It defines:

            :methods:
                | test_create - Verifies factory returns IMotorFrameBuilder.
                | test_get_version - Verifies factory version string.
    '''

    def test_create(self) -> None:
        '''Verifies create returns conforming IMotorFrameBuilder instance.'''
        frame_builder: IBinaryFrameBuilder = BinaryFrameBuilderFactory.create()
        motor_builder = MotorFrameBuilderFactory.create(frame_builder=frame_builder)
        self.assertIsInstance(motor_builder, IMotorFrameBuilder)

    def test_get_version(self) -> None:
        '''Verifies factory version returns valid string.'''
        version = MotorFrameBuilderFactory.get_version()
        self.assertIsInstance(version, str)
        self.assertTrue(len(version) > 0)


if __name__ == '__main__':
    main()
