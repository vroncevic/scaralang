# -*- coding: UTF-8 -*-

'''
Module
    scara_dsl_service.py
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
    High-level facade orchestrating SCARA DSL compilation, validation, and binary framing.
'''

from __future__ import annotations

from typing import Final

from scaralang.core.model.dsl.ast.program import ScaraProgram
from scaralang.core.model.dsl.binary.binary_program_telemetry import BinaryProgramTelemetry
from scaralang.core.model.dsl.binary.disassembled_frame import DisassembledFrame
from scaralang.core.model.dsl.binary.disassembly_summary import DisassemblySummary
from scaralang.core.model.dsl.binary.program import BinaryProgram
from scaralang.core.model.dsl.diagnostic.scara_diagnostic import ScaraDiagnostic
from scaralang.core.model.trajectory.waypoint import Waypoint
from scaralang.core.service.dsl.binary.ibinary_service import IBinaryService
from scaralang.core.service.dsl.compilation.iscara_dsl_compiler import IScaraDslCompiler
from scaralang.core.service.dsl.iscara_dsl_validator import IScaraDslValidator
from scaralang.core.service.dsl.scara_dsl_bundle import ScaraDslBundle
from scaralang.core.service.dsl.toolchain.itoolchain_info_provider import IToolchainInfoProvider
from scaralang.core.service.exporter.scara.iscara_plan_exporter import IScaraPlanExporter
from scaralang.core.service.trajectory.plan.itrajectory_plan import ITrajectoryPlan
from scaralang.core.service.trajectory.plan.itrajectory_read_only import ITrajectoryReadOnly

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ScaraDslService:
    '''
        High-level facade orchestrating SCARA DSL compilation, validation, and binary serialization.

        It defines:

            :attributes:
                | _compiler - DSL compiler orchestrating parsing, linting, and trajectory creation.
                | _validator - DSL script syntax, diagnostics, and kinematics validator.
                | _exporter - TrajectoryPlan to .scara code serializer protocol.
                | _binary_service - Binary compilation and disassembly service protocol.
                | _toolchain_info - Provider of toolchain catalog, metadata, and wire spec.
            :methods:
                | __init__ - Initializes DSL facade with injected collaborator bundle.
                | compile_script - Compiles DSL source code into executable ITrajectoryPlan.
                | compile_program - Compiles AST program into executable ITrajectoryPlan.
                | validate_script - Checks syntax, static analysis, and kinematics of DSL script.
                | lint_script - Performs static analysis checks on DSL script string.
                | export_plan - Serializes active TrajectoryPlan to DSL source text.
                | format_waypoint - Formats trajectory waypoint into SCARA move instruction.
                | compile_plan - Compiles ITrajectoryPlan into BinaryProgram package.
                | compile_to_bytes - Compiles DSL code directly to raw UART wire byte stream.
                | compile_to_binary - Compiles DSL source text into BinaryProgram package.
                | disassemble_bytes - Disassembles binary frame bytes into structured frame models.
                | get_toolchain_info - Returns toolchain metadata, catalog, and protocol spec.
                | is_initialized - Checks if all internal components are initialized.
    '''

    _compiler: IScaraDslCompiler
    _validator: IScaraDslValidator
    _exporter: IScaraPlanExporter
    _binary_service: IBinaryService
    _toolchain_info: IToolchainInfoProvider

    def __init__(self, *, bundle: ScaraDslBundle) -> None:
        '''
            Initializes ScaraDslService with injected collaborator bundle.

            :param bundle: Injected ScaraDslBundle collaborator container.
        '''
        self._compiler: Final[IScaraDslCompiler] = bundle.compiler
        self._validator: Final[IScaraDslValidator] = bundle.validator
        self._exporter: Final[IScaraPlanExporter] = bundle.exporter
        self._binary_service: Final[IBinaryService] = bundle.binary_service
        self._toolchain_info: Final[IToolchainInfoProvider] = bundle.toolchain_info

    def is_initialized(self) -> bool:
        '''
            Checks if all internal components are initialized.

            :return: True if service is operational, False otherwise.
            :exceptions: None.
        '''
        return all((
            self._compiler is not None,
            self._validator is not None,
            self._exporter is not None,
            self._binary_service is not None,
            self._toolchain_info is not None,
        ))

    def compile_script(self, *, source: str) -> ITrajectoryPlan:
        '''
            Compiles DSL source code into an executable and validated ITrajectoryPlan.

            :param source: Raw .scara script text.
            :return: Validated ITrajectoryPlan protocol instance.
            :exceptions: ValueError if syntax or static analysis errors occur.
        '''
        return self._compiler.compile_script(source=source)

    def compile_program(self, *, program: ScaraProgram) -> ITrajectoryPlan:
        '''
            Compiles parsed AST program into an executable and validated ITrajectoryPlan.

            :param program: ScaraProgram AST instance to compile.
            :return: Validated ITrajectoryPlan protocol instance.
            :exceptions: ValueError if static analysis errors occur.
        '''
        return self._compiler.compile_program(program=program)

    def validate_script(self, *, source: str) -> tuple[bool, list[str]]:
        '''
            Checks syntax, static analysis rules, and kinematics of a DSL script.

            :param source: Raw .scara script text.
            :return: Tuple of (is_valid boolean, list of error message strings).
            :exceptions: None.
        '''
        return self._validator.validate_script(source=source)

    def lint_script(self, *, source: str) -> tuple[ScaraDiagnostic, ...]:
        '''
            Performs static analysis checks on a DSL script string.

            :param source: Raw .scara script text.
            :return: Tuple of ScaraDiagnostic findings.
            :exceptions: None.
        '''
        return self._validator.lint_script(source=source)

    def export_plan(self, *, plan: ITrajectoryReadOnly) -> str:
        '''
            Serializes active TrajectoryPlan into formatted .scara DSL source text.

            :param plan: Read-only trajectory plan instance to serialize.
            :return: Formatted SCARA DSL script.
            :exceptions: None.
        '''
        return self._exporter.export_plan(plan=plan)

    def format_waypoint(
        self, *, waypoint: Waypoint, is_initial: bool = False
    ) -> str:
        '''
            Formats a single trajectory waypoint into a SCARA DSL move instruction.

            :param waypoint: Trajectory Waypoint instance.
            :param is_initial: True if generating the initial joint move, False for linear.
            :return: Formatted SCARA DSL instruction line.
            :exceptions: None.
        '''
        return self._exporter.format_waypoint(
            waypoint=waypoint, is_initial=is_initial
        )

    def compile_plan(self, *, plan: ITrajectoryPlan) -> BinaryProgram:
        '''
            Compiles ITrajectoryPlan into BinaryProgram package.

            :param plan: ITrajectoryPlan protocol instance.
            :return: BinaryProgram instance.
            :exceptions: None.
        '''
        return self._binary_service.compile_plan(plan=plan)

    def compile_to_bytes(self, *, source: str) -> bytes:
        '''
            Compiles DSL code directly to raw UART wire byte stream.

            :param source: Raw .scara DSL source text.
            :return: Serialized wire byte stream.
            :exceptions: None.
        '''
        program = self.compile_to_binary(source=source)

        return program.raw_bytes

    def compile_to_binary(self, *, source: str) -> BinaryProgram:
        '''
            Compiles DSL source text into BinaryProgram package.

            :param source: Raw .scara DSL source text.
            :return: BinaryProgram instance.
            :exceptions: None.
        '''
        plan = self.compile_script(source=source)

        return self._binary_service.compile_plan(plan=plan)

    def disassemble_bytes(
        self, *, data: bytes
    ) -> tuple[DisassembledFrame, ...]:
        '''
            Disassembles binary frame bytes into structured frame models.

            :param data: Contiguous binary bytes.
            :return: Tuple of decoded DisassembledFrame domain models.
            :exceptions: None.
        '''
        return self._binary_service.disassemble_bytes(data=data)

    def get_program_telemetry(
        self, *, program: BinaryProgram
    ) -> BinaryProgramTelemetry:
        '''
            Returns execution metrics and telemetry for a compiled binary program.

            :param program: BinaryProgram instance.
            :return: BinaryProgramTelemetry domain model.
            :exceptions: None.
        '''
        return self._binary_service.get_program_telemetry(program=program)

    def get_toolchain_info(self, *, verbose: bool = False) -> tuple[str, ...]:
        '''
            Returns toolchain metadata, instruction catalog and protocol specification.

            :param verbose: Whether to include kinematic bounds details.
            :return: Tuple of informative strings.
            :exceptions: None.
        '''
        return self._toolchain_info.get_toolchain_info(verbose=verbose)

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
        return self._binary_service.calculate_disassembly_summary(
            frames=frames, byte_count=byte_count
        )
