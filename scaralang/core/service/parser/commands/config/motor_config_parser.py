# -*- coding: UTF-8 -*-

'''
Module
    motor_config_parser.py
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
    Implementation of ICommandParser parsing CONFIG MOTOR actuation mode commands.
'''

from __future__ import annotations

from scaralang.core.model.dsl.ast.command_type import ScaraCommandType
from scaralang.core.model.dsl.ast.instruction import ScaraInstruction
from scaralang.core.model.dsl.ast.instruction_param import InstructionParam
from scaralang.core.model.dsl.token.scara_token import ScaraToken
from scaralang.core.model.motor.axis_mask import AxisMask
from scaralang.core.model.motor.motor_config import MotorConfig
from scaralang.core.model.motor.motor_drive_mode import MotorDriveMode
from scaralang.core.model.motor.motor_interface_type import MotorInterfaceType
from scaralang.core.service.motor.motor_config_factory import MotorConfigFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class MotorConfigParser:
    '''
        Command parser handler for CONFIG MOTOR actuation mode instructions.

        It defines:

            :attributes:
                | _name - Component identification name.
            :methods:
                | name - Property returning component name.
                | can_parse - Checks whether command matches CONFIG_MOTOR or MOTOR_MODE.
                | parse - Parses CONFIG MOTOR statement tokens into ScaraInstruction.
    '''

    def __init__(self) -> None:
        '''Initializes MotorConfigParser.'''
        self._name: str = 'motor_config_parser'

    @property
    def name(self) -> str:
        '''
            Gets component identification name.

            :return: Component name string.
        '''
        return self._name

    def can_parse(self, *, command_name: str) -> bool:
        '''
            Checks if command is CONFIG_MOTOR or MOTOR_MODE.

            :param command_name: Command keyword string.
            :return: True if match, False otherwise.
        '''
        return command_name in (
            ScaraCommandType.CONFIG_MOTOR,
            'CONFIG_MOTOR',
            'MOTOR_MODE',
        )

    def parse(
        self,
        *,
        tokens: tuple[ScaraToken, ...],
        line_num: int,
        raw_text: str,
    ) -> ScaraInstruction:
        '''
            Parses CONFIG MOTOR statement into ScaraInstruction.

            :param tokens: Statement token tuple.
            :param line_num: Line number in source code.
            :param raw_text: Original statement text.
            :return: ScaraInstruction node.
            :exceptions: ValueError on invalid motor configuration syntax.
        '''
        first_kw: str = tokens[0].value.upper()
        raw_val: str = ''
        raw_iface: str = ''

        if first_kw == ScaraCommandType.CONFIG:
            if len(tokens) < 3:
                raise ValueError(
                    f'Invalid CONFIG syntax at line {line_num}. '
                    f'Expected: CONFIG MOTOR <OPEN_LOOP|CLOSED_LOOP> [INTERFACE]'
                )

            sub: str = tokens[1].value.upper()

            if sub != 'MOTOR':
                raise ValueError(
                    f'Unknown CONFIG property {sub!r} at line {line_num}'
                )

            raw_val = tokens[2].value.upper()

            if len(tokens) >= 4:
                raw_iface = tokens[3].value.upper()

        elif first_kw in (ScaraCommandType.CONFIG_MOTOR, 'MOTOR_MODE'):
            if len(tokens) < 2:
                raise ValueError(
                    f'Invalid {first_kw} syntax at line {line_num}. '
                    f'Expected: {first_kw} <OPEN_LOOP|CLOSED_LOOP> [INTERFACE]'
                )

            raw_val = tokens[1].value.upper()

            if len(tokens) >= 3:
                raw_iface = tokens[2].value.upper()

        else:
            raise ValueError(
                f'Unexpected command {first_kw!r} for motor config at line {line_num}'
            )

        norm_val: str = raw_val.strip().upper()

        if not MotorConfigFactory.is_valid_drive_mode(norm_val):
            raise ValueError(
                f'Invalid motor drive mode {raw_val!r} at line {line_num}. '
                f'Must be OPEN_LOOP or CLOSED_LOOP'
            )

        drive_mode: MotorDriveMode = MotorConfigFactory.parse_drive_mode(norm_val)

        try:
            interface_type: MotorInterfaceType = MotorConfigFactory.resolve_interface_type(
                mode=drive_mode,
                raw_interface=raw_iface,
            )
        except ValueError as exc:
            raise ValueError(
                f'Invalid motor interface {raw_iface!r} at line {line_num}. '
                f'Must be STEP_DIR, CAN_BUS, or SERIAL'
            ) from exc

        motor_config: MotorConfig = MotorConfigFactory.create(
            mode=drive_mode,
            interface_type=interface_type,
            axis_mask=AxisMask.ALL,
        )

        return ScaraInstruction(
            command_type=ScaraCommandType.CONFIG_MOTOR,
            line_number=line_num,
            raw_text=raw_text,
            parameters={
                InstructionParam.MODE: motor_config.mode.value,
                InstructionParam.MOTOR_MODE: motor_config.mode.value,
                InstructionParam.INTERFACE: motor_config.interface_type.value,
                InstructionParam.AXIS_MASK: motor_config.axis_mask.value,
            },
        )
