# -*- coding: UTF-8 -*-

'''
Module
    disassembly_summary_test.py
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
    Unit tests for DisassemblySummary domain model.
'''

from __future__ import annotations

from dataclasses import FrozenInstanceError
from unittest import TestCase
from unittest import main

from scaralang.core.model.dsl.binary.disassembly_summary import DisassemblySummary

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestDisassemblySummary(TestCase):
    '''Unit tests verifying DisassemblySummary attributes and immutability.'''

    def test_instantiation_and_attributes(self) -> None:
        '''Verifies DisassemblySummary fields are assigned correctly.'''
        summary = DisassemblySummary(
            total_bytes=128,
            decoded_frames=4,
            motion_frames=2,
            tool_commands=1,
            wait_delays=1,
            system_frames=0,
        )
        self.assertEqual(summary.total_bytes, 128)
        self.assertEqual(summary.decoded_frames, 4)
        self.assertEqual(summary.motion_frames, 2)
        self.assertEqual(summary.tool_commands, 1)
        self.assertEqual(summary.wait_delays, 1)
        self.assertEqual(summary.system_frames, 0)

    def test_immutability(self) -> None:
        '''Verifies DisassemblySummary is frozen and cannot be mutated.'''
        summary = DisassemblySummary(
            total_bytes=64,
            decoded_frames=2,
            motion_frames=1,
            tool_commands=1,
            wait_delays=0,
            system_frames=0,
        )
        with self.assertRaises(FrozenInstanceError):
            summary.total_bytes = 256  # type: ignore[misc]


if __name__ == '__main__':
    main()
