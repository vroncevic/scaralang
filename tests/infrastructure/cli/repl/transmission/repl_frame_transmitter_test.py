# -*- coding: UTF-8 -*-

'''
Module
    repl_frame_transmitter_test.py
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
    Unit tests for ReplFrameTransmitter and ReplFrameTransmitterFactory.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.infrastructure.cli.repl.transmission.irepl_frame_transmitter import IReplFrameTransmitter
from scaralang.infrastructure.cli.repl.transmission.repl_frame_transmitter import ReplFrameTransmitter
from scaralang.infrastructure.cli.repl.transmission.repl_frame_transmitter_factory import ReplFrameTransmitterFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestReplFrameTransmitter(TestCase):
    '''
        Test cases verifying ReplFrameTransmitter.

        It defines:

            :methods:
                | test_transmit_frame - Verifies recording and transmitting frames.
                | test_dry_run_and_endpoint - Verifies endpoint and dry-run query.
                | test_configure - Verifies reconfiguring endpoint and mode.
                | test_factory_and_protocol_conformance - Verifies factory and protocol check.
    '''

    def test_transmit_frame(self) -> None:
        '''Verifies appending bytes to transmission buffer.'''
        transmitter = ReplFrameTransmitter()
        data = b'\xAA\x55\x10\x01\x00'
        success = transmitter.transmit_frame(raw_bytes=data)
        self.assertTrue(success)
        self.assertEqual(len(transmitter.transmitted_frames), 1)
        self.assertEqual(transmitter.transmitted_frames[0], data)

    def test_dry_run_and_endpoint(self) -> None:
        '''Verifies configuration properties.'''
        transmitter = ReplFrameTransmitter(endpoint='127.0.0.1:8080', dry_run=False)
        self.assertEqual(transmitter.get_endpoint(), '127.0.0.1:8080')
        self.assertFalse(transmitter.is_dry_run())

    def test_configure(self) -> None:
        '''Verifies reconfiguring endpoint and dry-run flag.'''
        transmitter = ReplFrameTransmitter()
        transmitter.configure(endpoint='/dev/ttyUSB0', dry_run=False)
        self.assertEqual(transmitter.get_endpoint(), '/dev/ttyUSB0')
        self.assertFalse(transmitter.is_dry_run())

    def test_factory_and_protocol_conformance(self) -> None:
        '''Verifies factory instantiation and protocol check.'''
        transmitter = ReplFrameTransmitterFactory.create()
        self.assertTrue(isinstance(transmitter, IReplFrameTransmitter))
        self.assertEqual(ReplFrameTransmitterFactory.get_version(), '1.0.3')


if __name__ == '__main__':
    main()
