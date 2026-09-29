# -*- coding: UTF-8 -*-

'''
Module
    ibinary_service.py
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
    Defines structural protocol IBinaryService for binary compilation and frame disassembly.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from scaralang.core.model.dsl.binary.binary_program_telemetry import BinaryProgramTelemetry
from scaralang.core.model.dsl.binary.disassembled_frame import DisassembledFrame
from scaralang.core.model.dsl.binary.disassembly_summary import DisassemblySummary
from scaralang.core.model.dsl.binary.program import BinaryProgram
from scaralang.core.service.trajectory.plan.itrajectory_plan import ITrajectoryPlan

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IBinaryService(Protocol):
    '''
        Structural protocol defining contracts for binary compilation and disassembly operations.

        It defines:

            :methods:
                | compile_plan - Compiles ITrajectoryPlan into BinaryProgram package.
                | disassemble_bytes - Disassembles wire byte stream into structured frames.
                | get_program_telemetry - Returns execution metrics and telemetry for binary program.
                | calculate_disassembly_summary - Computes DisassemblySummary domain model.
    '''

    def compile_plan(self, *, plan: ITrajectoryPlan) -> BinaryProgram:
        '''
            Compiles a validated ITrajectoryPlan into a binary program package.

            :param plan: Validated ITrajectoryPlan protocol instance.
            :return: Compiled BinaryProgram containing binary frames and byte stream.
        '''

    def disassemble_bytes(
        self, *, data: bytes
    ) -> tuple[DisassembledFrame, ...]:
        '''
            Disassembles binary frame bytes into structured frame models.

            :param data: Contiguous binary bytes.
            :return: Tuple of decoded DisassembledFrame domain models.
        '''

    def get_program_telemetry(
        self, *, program: BinaryProgram
    ) -> BinaryProgramTelemetry:
        '''
            Returns execution metrics and telemetry for a compiled binary program.

            :param program: BinaryProgram instance.
            :return: BinaryProgramTelemetry domain model.
        '''

    def calculate_disassembly_summary(
        self,
        *,
        frames: tuple[DisassembledFrame, ...],
        byte_count: int,
    ) -> DisassemblySummary:
        '''
            Computes DisassemblySummary domain model from decoded frames and total bytes.

            :param frames: Decoded DisassembledFrame domain models.
            :param byte_count: Total raw bytes parsed from binary source.
            :return: Computed DisassemblySummary domain model.
        '''
