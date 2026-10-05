# -*- coding: UTF-8 -*-

'''
Module
    binary_program_telemetry.py
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
    Defines immutable BinaryProgramTelemetry model holding execution metrics and axis step counts.
'''

from __future__ import annotations

from dataclasses import dataclass, field

from scaralang.core.model.dsl.binary.axis_peak_steps import AxisPeakSteps

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(frozen=True, slots=True, kw_only=True)
class BinaryProgramTelemetry:
    '''
        Execution metrics and telemetry metadata for a compiled binary program.

        It defines:

            :attributes:
                | source_instructions - Total number of compiled instructions.
                | compiled_steps - Total number of compiled motion steps.
                | duration_us - Total estimated execution duration in microseconds.
                | duration_s - Total estimated execution duration in seconds.
                | peak_steps - Peak axis step counts observed across motion steps.
                | total_wire_bytes - Total raw byte size of the wire frame stream.
    '''

    source_instructions: int = 0
    compiled_steps: int = 0
    duration_us: int = 0
    duration_s: float = 0.0
    peak_steps: AxisPeakSteps = field(default_factory=AxisPeakSteps)
    total_wire_bytes: int = 0
