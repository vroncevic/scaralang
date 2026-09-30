# -*- coding: UTF-8 -*-

'''
Module
    joint_steps_payload_formatter.py
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
    Defines JointStepsPayloadFormatter formatting joint step motion payloads for inspection.
'''

from __future__ import annotations

from typing import Final

from scaralang.core.model.protocol.joint_steps import JointSteps
from scaralang.infrastructure.command.compile.inspection.framing.ihex_stream_formatter import IHexStreamFormatter

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class JointStepsPayloadFormatter:
    '''
        Formats joint step displacement payloads into human-readable multi-line presentation.

        It defines:

            :attributes:
                | _hex_formatter - Injected hex stream formatter strategy.
            :methods:
                | __init__ - Initializes formatter with injected hex stream formatter.
                | format_joint_steps - Formats unpacked JointSteps and hex bytes.
    '''

    _hex_formatter: IHexStreamFormatter

    def __init__(self, *, hex_formatter: IHexStreamFormatter) -> None:
        '''
            Initializes JointStepsPayloadFormatter with injected hex formatter.

            :param hex_formatter: Injected hex stream formatter.
        '''
        self._hex_formatter: Final[IHexStreamFormatter] = hex_formatter

    def format_joint_steps(
        self,
        *,
        steps: JointSteps,
        raw_payload: bytes
    ) -> str:
        '''
            Formats unpacked joint step coordinates, duration, feedrate, and raw hex bytes.

            :param steps: Deserialized JointSteps model.
            :param raw_payload: Raw payload byte sequence.
            :return: Formatted presentation string.
        '''
        dur_ms: float = steps.duration_us / 1000.0
        hex_str: str = self._hex_formatter.format_bytes(data=raw_payload)
        struct_line_1: str = (
            f'  - Packed Struct: J1={steps.target_j1_steps:+d} steps | '
            f'J2={steps.target_j2_steps:+d} steps | '
            f'Z={steps.target_z_steps:+d} steps | '
            f'J4={steps.target_j4_steps:+d} steps'
        )
        struct_line_2: str = (
            f'                   Duration={steps.duration_us:,} µs ({dur_ms:.1f} ms) | '
            f'Feedrate={steps.feedrate_scale}%'
        )
        hex_line: str = f'  - Payload Hex:   {hex_str}'

        return f'{struct_line_1}\n{struct_line_2}\n{hex_line}'
