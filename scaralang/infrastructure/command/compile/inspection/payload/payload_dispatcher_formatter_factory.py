# -*- coding: UTF-8 -*-

'''
Module
    payload_dispatcher_formatter_factory.py
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
    Defines PayloadDispatcherFormatterFactory creating formatters.
'''

from __future__ import annotations

from scaralang.core.service.protocol.ibinary_payload_unpacker import IBinaryPayloadUnpacker
from scaralang.infrastructure.command.compile.inspection.framing.hex_stream_formatter_factory import HexStreamFormatterFactory
from scaralang.infrastructure.command.compile.inspection.payload.joint_steps_payload_formatter_factory import JointStepsPayloadFormatterFactory
from scaralang.infrastructure.command.compile.inspection.payload.payload_dispatcher_formatter import PayloadDispatcherFormatter
from scaralang.infrastructure.command.compile.inspection.payload.tool_command_payload_formatter_factory import ToolCommandPayloadFormatterFactory
from scaralang.infrastructure.communication.protocol.binary.parser.binary_payload_unpacker_factory import BinaryPayloadUnpackerFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class PayloadDispatcherFormatterFactory:
    '''
        Factory instantiating PayloadDispatcherFormatter instances.

        It defines:

            :methods:
                | create - Instantiates a new PayloadDispatcherFormatter with injected unpacker.
                | create_default - Instantiates a new PayloadDispatcherFormatter with default unpacker.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(
        cls,
        *,
        unpacker: IBinaryPayloadUnpacker,
    ) -> PayloadDispatcherFormatter:
        '''
            Creates a new PayloadDispatcherFormatter instance with
            wired collaborator formatters.

            :param unpacker: Injected payload unpacker protocol instance.
            :return: New PayloadDispatcherFormatter instance.
        '''
        return PayloadDispatcherFormatter(
            joint_formatter=JointStepsPayloadFormatterFactory.create(),
            tool_formatter=ToolCommandPayloadFormatterFactory.create(),
            hex_formatter=HexStreamFormatterFactory.create(),
            unpacker=unpacker,
        )

    @classmethod
    def create_default(cls) -> PayloadDispatcherFormatter:
        '''
            Creates a new PayloadDispatcherFormatter instance with default unpacker.

            :return: New PayloadDispatcherFormatter instance.
        '''
        return cls.create(unpacker=BinaryPayloadUnpackerFactory.create())

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory version string.

            :return: Factory version string.
        '''
        return __version__
