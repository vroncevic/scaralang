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
    Unit tests for PayloadDecoderFactory.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.service.disassembler.frame.decoder.factory import PayloadDecoderFactory
from scaralang.core.service.disassembler.frame.decoder.idecoder import IFramePayloadDecoder
from scaralang.infrastructure.protocol.binary.parser.unpacker.actuator import BinaryActuatorPayloadUnpacker
from scaralang.infrastructure.protocol.binary.parser.unpacker.motion import BinaryMotionPayloadUnpacker

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.9'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestPayloadDecoderFactory(TestCase):
    '''
    Test cases verifying PayloadDecoderFactory operations.

    It defines:

        :methods:
            | test_create - Verifies factory produces tuple of IFramePayloadDecoder instances.
            | test_get_version - Verifies version string retrieval.
    '''

    def test_create(self) -> None:
        '''
        Verifies factory instantiates tuple of valid payload decoders.
        '''
        motion_unpacker = BinaryMotionPayloadUnpacker()
        actuator_unpacker = BinaryActuatorPayloadUnpacker()
        decoders = PayloadDecoderFactory.create(
            motion_unpacker=motion_unpacker,
            actuator_unpacker=actuator_unpacker,
        )
        self.assertIsInstance(decoders, tuple)
        self.assertEqual(len(decoders), 3)
        for decoder in decoders:
            self.assertIsInstance(decoder, IFramePayloadDecoder)

    def test_get_version(self) -> None:
        '''
        Verifies version string retrieval.
        '''
        self.assertEqual(PayloadDecoderFactory.get_version(), '1.0.9')


if __name__ == '__main__':
    main()
