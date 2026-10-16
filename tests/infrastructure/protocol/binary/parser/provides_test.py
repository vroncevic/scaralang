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
    Unit tests for ParserProvides dataclass container.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.service.protocol.ibinary_actuator_payload_unpacker import IBinaryActuatorPayloadUnpacker
from scaralang.core.service.protocol.ibinary_frame_parser import IBinaryFrameParser
from scaralang.core.service.protocol.ibinary_motion_payload_unpacker import IBinaryMotionPayloadUnpacker
from scaralang.core.service.protocol.ibinary_response_payload_unpacker import IBinaryResponsePayloadUnpacker
from scaralang.core.service.protocol.ibinary_system_payload_unpacker import IBinarySystemPayloadUnpacker
from scaralang.infrastructure.protocol.binary.parser.assembler.assembler import BinaryFrameAssembler
from scaralang.infrastructure.protocol.binary.parser.assembler.iassembler import IBinaryFrameAssembler
from scaralang.infrastructure.protocol.binary.parser.parser import BinaryFrameParser
from scaralang.infrastructure.protocol.binary.parser.provides import ParserProvides
from scaralang.infrastructure.protocol.binary.parser.unpacker.actuator import BinaryActuatorPayloadUnpacker
from scaralang.infrastructure.protocol.binary.parser.unpacker.motion import BinaryMotionPayloadUnpacker
from scaralang.infrastructure.protocol.binary.parser.unpacker.response import BinaryResponsePayloadUnpacker
from scaralang.infrastructure.protocol.binary.parser.unpacker.system import BinarySystemPayloadUnpacker

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.9'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestParserProvides(TestCase):
    '''
        Test cases verifying ParserProvides dataclass.

        It defines:

            :methods:
                | test_parser_provides_attributes - Verifies attributes and protocol typing.
                | test_parser_provides_immutability - Verifies frozen behavior.
    '''

    def test_parser_provides_attributes(self) -> None:
        '''
            Tests ParserProvides holds valid protocol instances.

            :exceptions: None.
        '''
        assembler = BinaryFrameAssembler()
        parser = BinaryFrameParser(assembler=assembler)
        motion = BinaryMotionPayloadUnpacker()
        actuator = BinaryActuatorPayloadUnpacker()
        system = BinarySystemPayloadUnpacker()
        response = BinaryResponsePayloadUnpacker()

        provides = ParserProvides(
            parser=parser,
            assembler=assembler,
            motion_unpacker=motion,
            actuator_unpacker=actuator,
            system_unpacker=system,
            response_unpacker=response,
        )

        self.assertIs(provides.parser, parser)
        self.assertIs(provides.assembler, assembler)
        self.assertIs(provides.motion_unpacker, motion)
        self.assertIs(provides.actuator_unpacker, actuator)
        self.assertIs(provides.system_unpacker, system)
        self.assertIs(provides.response_unpacker, response)

        self.assertIsInstance(provides.parser, IBinaryFrameParser)
        self.assertIsInstance(provides.assembler, IBinaryFrameAssembler)
        self.assertIsInstance(provides.motion_unpacker, IBinaryMotionPayloadUnpacker)
        self.assertIsInstance(provides.actuator_unpacker, IBinaryActuatorPayloadUnpacker)
        self.assertIsInstance(provides.system_unpacker, IBinarySystemPayloadUnpacker)
        self.assertIsInstance(provides.response_unpacker, IBinaryResponsePayloadUnpacker)

    def test_parser_provides_immutability(self) -> None:
        '''
            Tests ParserProvides is frozen and immutable.

            :exceptions: None.
        '''
        assembler = BinaryFrameAssembler()
        parser = BinaryFrameParser(assembler=assembler)
        motion = BinaryMotionPayloadUnpacker()
        actuator = BinaryActuatorPayloadUnpacker()
        system = BinarySystemPayloadUnpacker()
        response = BinaryResponsePayloadUnpacker()

        provides = ParserProvides(
            parser=parser,
            assembler=assembler,
            motion_unpacker=motion,
            actuator_unpacker=actuator,
            system_unpacker=system,
            response_unpacker=response,
        )
        with self.assertRaises(AttributeError):
            provides.parser = parser  # type: ignore[misc]


if __name__ == '__main__':
    main()
