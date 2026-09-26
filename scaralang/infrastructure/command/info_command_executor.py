# -*- coding: UTF-8 -*-

'''
Module
    info_command_executor.py
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
    Command executor for displaying SCARA DSL toolchain information.
'''

from __future__ import annotations

from collections.abc import Mapping

from scaralang.core.service.dsl.iscara_dsl_service import IScaraDslService
from scaralang.infrastructure.command.icommand_definition import ICommandDefinition

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class InfoCommandExecutor:
    '''
        Command executor strategy for displaying toolchain and grammar info.

        It defines:

            :attributes:
                | definition - The command CLI metadata definition.
            :methods:
                | execute - Executes the info command.
                | get_definition - Returns the command definition metadata.
    '''

    definition: ICommandDefinition

    def __init__(self, definition: ICommandDefinition) -> None:
        '''
            Initializes the info command executor.

            :param definition: The command definition metadata.
            :exceptions: None.
        '''
        self.definition = definition

    def execute(
        self,
        *,
        params: Mapping[str, object],
        service: IScaraDslService
    ) -> Mapping[str, object]:
        '''
            Executes the info subcommand.

            :param params: Subcommand parameters from CLI parser.
            :param service: SCARA DSL service instance.
            :return: The result of the subcommand execution.
            :exceptions: None.
        '''
        verbose = bool(params.get('verbose'))
        lines = [
            'scaralang: SCARA Robotics Domain-Specific Language (DSL) Toolchain',
            'Version: 1.0.0',
            'Supported Instructions:',
            '  MOVE X Y Z [F] [MODE]  - Linear motion in Cartesian space',
            '  JUMP X Y Z [H] [F]     - Gate motion (retract, traverse, plunge)',
            '  ARC X Y CX CY CW/CCW   - Circular arc interpolation',
            '  WAIT MS                - Dwell delay in milliseconds',
            '  PUMP ON/OFF            - Vacuum pump control',
            '  VALVE ON/OFF           - Blow-off vent valve control',
            '  HOME                   - Homing sequence calibration',
            'Binary Protocol Specification:',
            '  Frame Delimiters: SOF1=0xAA, SOF2=0x55, EOF=0x0D',
            '  Integrity Check:  CRC-16-CCITT (poly 0x1021, init 0xFFFF)',
            '  Header Format:    <BBB (msg_id, seq_num, payload_len)',
            '  Trailer Format:   <HB  (crc16, eof)'
        ]
        if verbose:
            lines.extend([
                '',
                'Default Kinematic Bounds:',
                '  L1 = 150.0 mm, L2 = 150.0 mm',
                '  Z range = [-50.0, 50.0] mm',
                '  Speed range = [1.0, 200.0] mm/s',
                '  Shoulder (J1) = [-150.0, +150.0] deg',
                '  Elbow (J2)    = [-150.0, +150.0] deg'
            ])

        return {'returncode': 0, 'stdout': '\n'.join(lines), 'stderr': ''}

    def get_definition(self) -> ICommandDefinition:
        '''
            Returns the command definition metadata.

            :return: The command definition metadata.
            :exceptions: None.
        '''
        return self.definition
