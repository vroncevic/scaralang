# -*- coding: UTF-8 -*-

'''
Module
    scara_info_provider.py
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
    Provides comprehensive toolchain metadata, instruction catalog, and specifications.
'''

from __future__ import annotations

from math import degrees
from typing import ClassVar

from scaralang.core.model.dsl.exporter.export_format import ExportFormat
from scaralang.core.model.kinematics.scara_bounds import ScaraBounds
from scaralang.core.model.kinematics.transmission_parameters import TransmissionParameters
from scaralang.core.model.protocol.binary_delimiter import BinaryDelimiter
from scaralang.core.service.kinematics.default_scara_profile import DefaultScaraProfile

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ScaraInfoProvider:
    '''
        Provides comprehensive toolchain metadata, instruction catalog, and specifications.

        It defines:

            :methods:
                | get_info - Returns formatted toolchain specification lines.
                | get_toolchain_info - Returns formatted toolchain specification lines.
                | get_supported_instructions - Returns list of supported DSL instruction summaries.
                | build_verbose_lines - Returns detailed kinematic bounds and transmission lines.
                | get_version - Returns the info provider version string representation.
    '''

    _INSTRUCTIONS: ClassVar[tuple[str, ...]] = (
        '  --- Motion Commands ---',
        '  MOVE_L X Y Z [F] [MODE]  - Linear Cartesian motion interpolation',
        '  MOVE_J J1 J2 Z J4 [F]    - Joint space point-to-point motion',
        '  JUMP X Y Z [H] [F]       - Gate motion (retract, traverse, plunge)',
        '  ARC X Y CX CY CW/CCW [F] - Circular arc interpolation (CW/CCW)',
        '  APPROACH Z [F]           - Relative downward vertical approach along Z',
        '  RETRACT Z [F]            - Relative upward vertical retract along Z',
        '  HOME [AXIS]              - Multi-axis homing sequence calibration',
        '  JOG_AXIS AXIS DIST [F]   - Relative manual Cartesian axis jog',
        '  JOG_JOINT JOINT DEG [F]  - Relative manual joint rotation jog',
        '  --- Configuration Commands ---',
        '  CONFIG ELBOW LEFT/RIGHT  - Kinematic elbow arm configuration mode',
        '  CONFIG MOTOR OPEN/CLOSED - Stepper motor actuation drive mode',
        '  SPEED [RAPID/WORK] F     - Path feedrate speed setting (mm/s)',
        '  ACCEL A                  - Path acceleration setting (mm/s^2)',
        '  OVERRIDE P               - Global speed override percentage (1-200%)',
        '  ZONE FINE/BLEND [R]      - Corner trajectory blending mode',
        '  TOOL_ORIENT FIXED/TANGENT- End-effector 4th axis orientation mode',
        '  --- Work Frames & Palletization ---',
        '  FRAME SET X Y THETA      - Define local work coordinate frame',
        '  FRAME RESET              - Reset coordinate frame to base world frame',
        '  PALLET DEF ID R C DX DY  - Matrix pallet layout definition',
        '  PALLET MOVE ID INDEX     - Move to pallet slot index',
        '  --- Tools & Actuation ---',
        '  PUMP ON/OFF              - Vacuum gripper pump control',
        '  VALVE ON/OFF             - Blow-off vent valve control',
        '  TOOL UP/DOWN             - Pneumatic tool cylinder actuation',
        '  PROBE Z [F]              - Tactile search probe until contact',
        '  --- Flow Control & Safety ---',
        '  WAIT MS                  - Dwell delay in milliseconds',
        '  SYNC                     - Synchronize motion queue buffer',
        '  HOLD / RESUME            - Pause / resume motion execution',
        '  ENABLE / DISABLE         - Energize / de-energize stepper driver stages',
        '  ESTOP                    - Immediate emergency stop',
    )

    _SUBCOMMANDS: ClassVar[tuple[str, ...]] = (
        'Available Subcommands:',
        '  compile     - Compiles .scara DSL scripts into binary frame streams',
        '  decompile   - Reconstructs .scara DSL code from binary frame files',
        '  disassemble - Disassembles and inspects binary wire frames and opcodes',
        '  export      - Exports trajectories into external formats (GCODE, CSV, JSON, SVG, SCARA)',
        '  lint        - Static syntax, semantic, and kinematic validation',
        '  info        - Toolchain metadata, instruction catalog, and specifications',
        '  repl        - Interactive Read-Eval-Print Loop terminal',
    )

    _EXPORT_FORMATS: ClassVar[tuple[str, ...]] = (
        'Supported Export Formats:',
        f'  {ExportFormat.GCODE:<11} - RS-274 / ISO G-code format for CNC/3D controllers',
        f'  {ExportFormat.CSV:<11} - Comma-separated tabular time-series trajectory waypoints',
        f'  {ExportFormat.JSON:<11} - Structured JSON AST and trajectory telemetry format',
        f'  {ExportFormat.SVG:<11} - 2D vector graphic path visualization diagram',
        f'  {ExportFormat.SCARA:<11} - Canonical SCARA DSL script format',
    )

    _PROTOCOL_SPECS: ClassVar[tuple[str, ...]] = (
        'Binary Protocol Specification:',
        f'  Frame Delimiters: SOF1=0x{BinaryDelimiter.SOF1:02X}, SOF2=0x{BinaryDelimiter.SOF2:02X}, EOF=0x{BinaryDelimiter.EOF:02X}',
        '  Integrity Check:  CRC-16-CCITT (poly 0x1021, init 0xFFFF)',
        '  Header Format:    <BBB (msg_id, seq_num, payload_len)',
        '  Trailer Format:   <HB  (crc16, eof)',
        f'  Max Payload:      {BinaryDelimiter.MAX_PAYLOAD_LEN} bytes',
    )

    def get_supported_instructions(self) -> tuple[str, ...]:
        '''
            Returns list of supported DSL instruction syntax summaries.

            :return: Tuple of supported instruction names and signatures.
            :exceptions: None.
        '''
        return self._INSTRUCTIONS

    def get_info(self, *, verbose: bool = False) -> tuple[str, ...]:
        '''
            Returns toolchain metadata, instruction catalog and protocol specification.

            :param verbose: Whether to include kinematic bounds details.
            :return: Tuple of informative strings.
            :exceptions: None.
        '''
        return self.get_toolchain_info(verbose=verbose)

    def get_toolchain_info(self, *, verbose: bool = False) -> tuple[str, ...]:
        '''
            Returns toolchain metadata, instruction catalog and protocol specification.

            :param verbose: Whether to include kinematic bounds details.
            :return: Tuple of informative strings.
            :exceptions: None.
        '''
        lines: list[str] = [
            'scaralang: SCARA Robotics Domain-Specific Language (DSL) Toolchain',
            f'Version: {__version__}',
            'Architecture: Clean Architecture / Hexagonal (Ports & Adapters)',
            '',
        ]
        lines.extend(self._SUBCOMMANDS)
        lines.append('')
        lines.extend(self._EXPORT_FORMATS)
        lines.append('')
        lines.append('Supported Instructions:')
        lines.extend(self._INSTRUCTIONS)
        lines.append('')
        lines.extend(self._PROTOCOL_SPECS)

        if verbose:
            lines.extend(self.build_verbose_lines())

        return tuple(lines)

    def build_verbose_lines(self) -> tuple[str, ...]:
        '''
            Builds detailed kinematic bounds and transmission lines.

            :return: Tuple of formatted verbose specification lines.
            :exceptions: None.
        '''
        bounds: ScaraBounds = DefaultScaraProfile.create_bounds()
        tx: TransmissionParameters = DefaultScaraProfile.create_transmission()

        j1_deg = degrees(bounds.joints.j1_max_rad)
        j2_deg = degrees(bounds.joints.j2_max_rad)

        return (
            '',
            'Default Kinematic Bounds:',
            f'  L1 = {bounds.links.l1:.1f} mm, L2 = {bounds.links.l2:.1f} mm',
            f'  Z range = [{bounds.vertical.z_min:.1f}, {bounds.vertical.z_max:.1f}] mm',
            (
                f'  Speed range = [{bounds.speeds.min_speed:.1f}, {bounds.speeds.max_speed:.1f}] '
                f'mm/s (default: {bounds.speeds.default_speed:.1f} mm/s)'
            ),
            (
                f'  Accel range = [1.0, {bounds.speeds.max_accel:.1f}] mm/s^2 '
                f'(default: {bounds.speeds.default_accel:.1f} mm/s^2)'
            ),
            f'  Shoulder (J1) = [-{j1_deg:.1f}, +{j1_deg:.1f}] deg',
            f'  Elbow (J2)    = [-{j2_deg:.1f}, +{j2_deg:.1f}] deg',
            (
                f'  Deadzone radius = {bounds.singularity.deadzone_r_min:.1f} mm, '
                f'Singularity margin = {bounds.singularity.singularity_outer_margin_mm:.1f} mm'
            ),
            '',
            'Default Transmission Parameters:',
            f'  Motor resolution = {tx.steps_per_rev:.1f} steps/rev, Microstepping = {tx.microstepping:.0f}x',
            f'  Shoulder gear ratio (J1) = {tx.gear_ratio_j1:.1f}:1',
            f'  Elbow gear ratio (J2)    = {tx.gear_ratio_j2:.1f}:1',
            f'  Wrist gear ratio (J4)    = {tx.gear_ratio_j4:.1f}:1',
            f'  Z-axis leadscrew pitch   = {tx.leadscrew_pitch_z:.1f} mm/rev',
        )

    def get_version(self) -> str:
        '''
            Returns the info provider version string representation.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return __version__
