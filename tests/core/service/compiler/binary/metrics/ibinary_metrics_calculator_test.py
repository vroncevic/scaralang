# -*- coding: UTF-8 -*-

'''
Module
    ibinary_metrics_calculator_test.py
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
    Unit tests for IBinaryMetricsCalculator protocol contract.
'''

from __future__ import annotations

from collections.abc import Sequence
from unittest import TestCase, main

from scaralang.core.model.dsl.binary.binary_program_telemetry import BinaryProgramTelemetry
from scaralang.core.model.dsl.binary.step import Step
from scaralang.core.service.compiler.binary.metrics.ibinary_metrics_calculator import IBinaryMetricsCalculator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.5'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DummyMetricsCalculator:
    '''Dummy metrics calculator for protocol runtime check verification.'''

    def calculate_metrics(
        self, *, steps: Sequence[Step]
    ) -> tuple[int, tuple[int, int, int, int]]:
        '''Dummy calculate_metrics implementation.'''
        _ = steps
        return 0, (0, 0, 0, 0)

    def calculate_telemetry(
        self, *, steps: Sequence[Step], raw_bytes: bytes
    ) -> BinaryProgramTelemetry:
        '''Dummy calculate_telemetry implementation.'''
        return BinaryProgramTelemetry(
            source_instructions=len(steps),
            compiled_steps=len(steps),
            total_wire_bytes=len(raw_bytes),
        )


class TestIBinaryMetricsCalculator(TestCase):
    '''
        Test cases verifying IBinaryMetricsCalculator protocol contract.

        It defines:

            :methods:
                | test_protocol_conformance - Verifies dummy class satisfies protocol.
    '''

    def test_protocol_conformance(self) -> None:
        '''Verifies structural typing conformance without inheritance.'''
        calculator = DummyMetricsCalculator()
        self.assertIsInstance(calculator, IBinaryMetricsCalculator)


if __name__ == '__main__':
    main()
