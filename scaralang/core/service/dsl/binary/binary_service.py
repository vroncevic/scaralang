# -*- coding: UTF-8 -*-

'''
Module
    binary_service.py
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
    Implementation of binary service orchestrating binary compilation and disassembly.
'''

from __future__ import annotations

from typing import Final

from scaralang.core.model.dsl.binary.binary_program_telemetry import BinaryProgramTelemetry
from scaralang.core.model.dsl.binary.disassembled_frame import DisassembledFrame
from scaralang.core.model.dsl.binary.disassembly_summary import DisassemblySummary
from scaralang.core.model.dsl.binary.program import BinaryProgram
from scaralang.core.service.compiler.binary.ibinary_compiler import IBinaryCompiler
from scaralang.core.service.disassembler.iscara_disassembler import IScaraDisassembler
from scaralang.core.service.trajectory.plan.itrajectory_plan import ITrajectoryPlan

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class BinaryService:
    '''
        Service orchestrating binary compilation and frame disassembly operations.

        It defines:

            :attributes:
                | _compiler - Binary frame compiler protocol instance.
                | _disassembler - Binary frame disassembler protocol instance.
            :methods:
                | __init__ - Initializes BinaryService with injected collaborators.
                | compile_plan - Compiles ITrajectoryPlan into BinaryProgram package.
                | disassemble_bytes - Disassembles binary frame bytes into structured frame models.
                | get_program_telemetry - Returns execution metrics and telemetry for binary program.
    '''

    _compiler: IBinaryCompiler
    _disassembler: IScaraDisassembler

    def __init__(
        self,
        *,
        compiler: IBinaryCompiler,
        disassembler: IScaraDisassembler,
    ) -> None:
        '''
            Initializes BinaryService with injected compiler and disassembler.

            :param compiler: Injected IBinaryCompiler protocol instance.
            :param disassembler: Injected IScaraDisassembler protocol instance.
            :exceptions: None.
        '''
        self._compiler: Final[IBinaryCompiler] = compiler
        self._disassembler: Final[IScaraDisassembler] = disassembler

    def compile_plan(self, *, plan: ITrajectoryPlan) -> BinaryProgram:
        '''
            Compiles a validated ITrajectoryPlan into a binary program package.

            :param plan: ITrajectoryPlan protocol instance.
            :return: BinaryProgram instance.
            :exceptions: None.
        '''
        return self._compiler.compile_plan(plan=plan)

    def disassemble_bytes(
        self, *, data: bytes
    ) -> tuple[DisassembledFrame, ...]:
        '''
            Disassembles binary frame bytes into structured frame models.

            :param data: Contiguous binary bytes.
            :return: Tuple of decoded DisassembledFrame domain models.
            :exceptions: None.
        '''
        return self._disassembler.disassemble(data=data)

    def get_program_telemetry(
        self, *, program: BinaryProgram
    ) -> BinaryProgramTelemetry:
        '''
            Returns execution metrics and telemetry for a compiled binary program.

            :param program: BinaryProgram instance.
            :return: BinaryProgramTelemetry domain model.
            :exceptions: None.
        '''
        return program.telemetry

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
            :exceptions: None.
        '''
        return self._disassembler.calculate_summary(
            frames=frames, byte_count=byte_count
        )
