# -*- coding: UTF-8 -*-

'''
Module
    buffer_test.py
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
    Unit tests for TransmissionBuffer implementation.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.infrastructure.cli.repl.transmission.buffer.buffer import TransmissionBuffer
from scaralang.infrastructure.cli.repl.transmission.buffer.ibuffer import ITransmissionBuffer

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestTransmissionBuffer(TestCase):
    '''
        Test cases verifying TransmissionBuffer operations.

        It defines:

            :methods:
                | test_init - Verifies buffer is initially empty.
                | test_append_and_get_frames - Verifies appending and retrieving frames.
                | test_clear - Verifies clearing buffer contents.
                | test_structural_typing - Verifies protocol satisfaction.
    '''

    def test_init(self) -> None:
        '''
            Verifies buffer is empty upon initialization.

            :exceptions: None.
        '''
        buf = TransmissionBuffer()
        self.assertEqual(len(buf.get_frames()), 0)

    def test_append_and_get_frames(self) -> None:
        '''
            Verifies appending frames and shallow copying in get_frames.

            :exceptions: None.
        '''
        buf = TransmissionBuffer()
        frame1 = b'\x01\x02\x03'
        frame2 = b'\x04\x05\x06'
        buf.append(frame_bytes=frame1)
        buf.append(frame_bytes=frame2)

        frames = buf.get_frames()
        self.assertEqual(len(frames), 2)
        self.assertEqual(frames[0], frame1)
        self.assertEqual(frames[1], frame2)

        frames.append(b'\x99')
        self.assertEqual(len(buf.get_frames()), 2)

    def test_clear(self) -> None:
        '''
            Verifies clearing buffered frames.

            :exceptions: None.
        '''
        buf = TransmissionBuffer()
        buf.append(frame_bytes=b'\x01')
        self.assertEqual(len(buf.get_frames()), 1)
        buf.clear()
        self.assertEqual(len(buf.get_frames()), 0)

    def test_structural_typing(self) -> None:
        '''
            Verifies TransmissionBuffer satisfies ITransmissionBuffer protocol.

            :exceptions: None.
        '''
        buf = TransmissionBuffer()
        self.assertTrue(isinstance(buf, ITransmissionBuffer))


if __name__ == '__main__':
    main()
