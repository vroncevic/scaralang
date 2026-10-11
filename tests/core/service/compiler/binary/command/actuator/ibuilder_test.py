# -*- coding: UTF-8 -*-

'''
Module
    ibuilder_test.py
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
    Unit tests for IActuatorFrameBuilder protocol.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.model.protocol.binary_frame import BinaryFrame
from scaralang.core.model.protocol.message_id import MessageId
from scaralang.core.service.compiler.binary.command.actuator.ibuilder import IActuatorFrameBuilder

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.8'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DummyActuatorFrameBuilder:
    '''
        Dummy class implementing IActuatorFrameBuilder for protocol verification.
    '''

    def build_actuator_frame(
        self,
        *,
        arg: str,
        seq_num: int,
    ) -> BinaryFrame:
        '''
            Dummy implementation of build_actuator_frame.
        '''
        _ = arg
        return BinaryFrame(
            seq_num=seq_num,
            msg_id=MessageId.CMD_CONFIG_MOTOR,
            payload=b'',
            crc16=0,
        )

    def build_motor_frame(
        self,
        *,
        arg: str,
        seq_num: int,
    ) -> BinaryFrame:
        '''
            Dummy compatibility implementation of build_motor_frame.
        '''
        return self.build_actuator_frame(arg=arg, seq_num=seq_num)

    def get_version(self) -> str:
        '''
            Dummy implementation of get_version.
        '''
        return '1.0.0'


class TestIActuatorFrameBuilder(TestCase):
    '''
        Test cases verifying IActuatorFrameBuilder structural protocol.

        It defines:

            :methods:
                | test_structural_conformance - Verifies protocol check.
                | test_structural_rejection - Verifies incomplete dummy is rejected.
    '''

    def test_structural_conformance(self) -> None:
        '''
            Verifies that dummy conforming class satisfies protocol check.
        '''
        builder = DummyActuatorFrameBuilder()
        self.assertIsInstance(builder, IActuatorFrameBuilder)

    def test_structural_rejection(self) -> None:
        '''
            Verifies that class missing required methods fails protocol check.
        '''
        self.assertFalse(isinstance(object(), IActuatorFrameBuilder))


if __name__ == '__main__':
    main()
