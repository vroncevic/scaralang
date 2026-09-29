# -*- coding: UTF-8 -*-

'''
Module
    info_command_executor_test.py
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
    Unit tests for InfoCommandExecutor class.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.service.dsl.scara_dsl_service_factory import ScaraDslServiceFactory
from scaralang.infrastructure.command.info.info_command_definition import InfoCommandDefinition
from scaralang.infrastructure.command.info.info_command_executor import InfoCommandExecutor
from scaralang.infrastructure.communication.protocol.binary.builder.binary_frame_builder_factory import BinaryFrameBuilderFactory
from scaralang.infrastructure.communication.protocol.binary.parser.binary_frame_parser_factory import BinaryFrameParserFactory
from scaralang.infrastructure.communication.protocol.binary.parser.binary_payload_unpacker_factory import BinaryPayloadUnpackerFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestInfoCommandExecutor(TestCase):
    '''
        Test cases verifying InfoCommandExecutor.

        It defines:

            :methods:
                | setUp - Initializes executor and service fixtures.
                | test_info_command_execution - Verifies info command returns valid payload.
                | test_get_definition - Verifies definition retrieval.
    '''

    def setUp(self) -> None:
        '''
            Sets up executor and service fixtures.
        '''
        self.cmd_def = InfoCommandDefinition()
        self.executor = InfoCommandExecutor(definition=self.cmd_def)
        self.service = ScaraDslServiceFactory.create_default(
            frame_builder=BinaryFrameBuilderFactory.create(),
            frame_parser=BinaryFrameParserFactory.create_default(),
            payload_unpacker=BinaryPayloadUnpackerFactory.create(),
        )

    def test_info_command_execution(self) -> None:
        '''
            Verifies info command execution output.
        '''
        result = self.executor.execute(params={}, service=self.service)
        self.assertEqual(result.get('returncode'), 0)
        stdout_text = str(result.get('stdout', ''))
        self.assertIn('scaralang: SCARA Robotics Domain-Specific Language', stdout_text)
        self.assertIn('CRC-16-CCITT', stdout_text)

    def test_get_definition(self) -> None:
        '''
            Verifies get_definition returns the injected definition.
        '''
        self.assertEqual(self.executor.get_definition(), self.cmd_def)


if __name__ == '__main__':
    main()
