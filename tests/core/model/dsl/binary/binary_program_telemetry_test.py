# -*- coding: UTF-8 -*-

'''
Module
    binary_program_telemetry_test.py
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
    Unit tests for BinaryProgramTelemetry model.
'''

from __future__ import annotations

from dataclasses import FrozenInstanceError
from unittest import TestCase, main

from scaralang.core.model.dsl.binary.binary_program_telemetry import (
    BinaryProgramTelemetry
)

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class BinaryProgramTelemetryTest(TestCase):
    '''Unit tests validating BinaryProgramTelemetry purity and immutability.'''

    def test_instantiation_and_attributes(self) -> None:
        '''Verify BinaryProgramTelemetry fields.'''
        telemetry = BinaryProgramTelemetry(
            source_instructions=5,
            compiled_steps=10,
            duration_us=250000,
            duration_s=0.25,
            peak_j1_steps=1200,
            peak_j2_steps=800,
            peak_z_steps=100,
            peak_j4_steps=50,
            total_wire_bytes=240,
        )
        self.assertEqual(telemetry.source_instructions, 5)
        self.assertEqual(telemetry.compiled_steps, 10)
        self.assertEqual(telemetry.duration_us, 250000)
        self.assertAlmostEqual(telemetry.duration_s, 0.25)
        self.assertEqual(telemetry.peak_j1_steps, 1200)
        self.assertEqual(telemetry.peak_j2_steps, 800)
        self.assertEqual(telemetry.peak_z_steps, 100)
        self.assertEqual(telemetry.peak_j4_steps, 50)
        self.assertEqual(telemetry.total_wire_bytes, 240)

    def test_frozen_immutability(self) -> None:
        '''Verify that modifying attributes raises FrozenInstanceError.'''
        telemetry = BinaryProgramTelemetry(
            source_instructions=1,
            compiled_steps=1,
            duration_us=1000,
            duration_s=0.001,
            peak_j1_steps=0,
            peak_j2_steps=0,
            peak_z_steps=0,
            peak_j4_steps=0,
            total_wire_bytes=20,
        )
        with self.assertRaises(FrozenInstanceError):
            setattr(telemetry, 'duration_us', 2000)


if __name__ == '__main__':
    main()
