# -*- coding: UTF-8 -*-

'''
Module
    motor.py
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
    Implementation of command parser parsing CONFIG MOTOR actuation mode commands.
'''

from __future__ import annotations

from typing import ClassVar

from scaralang.core.model.dsl.ast.command_type import ScaraCommandType
from scaralang.core.model.dsl.ast.instruction import ScaraInstruction
from scaralang.core.model.dsl.ast.instruction_param import ScaraInstructionParam
from scaralang.core.model.dsl.token.token import ScaraToken
from scaralang.core.model.exceptions.semantic import ScaraSemanticError
from scaralang.core.model.exceptions.syntax import ScaraSyntaxError
from scaralang.core.model.motor.mask import AxisMask
from scaralang.core.model.motor.config import MotorConfig
from scaralang.core.model.motor.mode import MotorDriveMode
from scaralang.core.model.motor.interface import MotorInterfaceType
from scaralang.core.service.motor.factory import MotorFactory
from scaralang.core.service.motor.interface import InterfaceResolver
from scaralang.core.service.motor.mode import DriveModeResolver
from scaralang.core.service.parser.commands.config.syntax import MotorSyntaxExtractor

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class MotorParser:
    '''
        Command parser handler for CONFIG MOTOR actuation mode instructions.

        It defines:

            :attributes:
                | NAME - Component identification name.
                | PARSED_COMMANDS - Handled command keywords tuple.
                | name - Property returning component name.
            :methods:
                | can_parse - Checks whether command matches CONFIG_MOTOR or MOTOR_MODE.
                | parse - Parses CONFIG MOTOR statement tokens into ScaraInstruction.
    '''

    NAME: ClassVar[str] = 'motor_parser'
    PARSED_COMMANDS: ClassVar[tuple[ScaraCommandType, str, str]] = (
        ScaraCommandType.CONFIG_MOTOR,
        'CONFIG_MOTOR',
        'MOTOR_MODE',
    )

    @property
    def name(self) -> str:
        '''
            Gets component identification name.

            :return: Component name string.
        '''
        return self.NAME

    def can_parse(self, *, command_name: str) -> bool:
        '''
            Checks if command is CONFIG_MOTOR or MOTOR_MODE.

            :param command_name: Command keyword string.
            :return: True if match, False otherwise.
        '''
        return command_name in self.PARSED_COMMANDS

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
            :exceptions: ScaraSyntaxError on invalid motor configuration syntax.
        '''
        raw_val, raw_iface = MotorSyntaxExtractor.extract(
            tokens=tokens, line_num=line_num
        )
        norm_val: str = raw_val.strip().upper()

        if not DriveModeResolver.is_valid_drive_mode(norm_val):
            raise ScaraSyntaxError(
                f'Invalid motor drive mode {raw_val!r} at line {line_num}. '
                'Must be OPEN_LOOP or CLOSED_LOOP'
            )

        drive_mode: MotorDriveMode = DriveModeResolver.parse_drive_mode(norm_val)

        try:
            interface_type: MotorInterfaceType = (
                InterfaceResolver.resolve_interface_type(
                    mode=drive_mode, raw_interface=raw_iface
                )
            )

        except (ScaraSemanticError, ValueError, KeyError) as exc:
            raise ScaraSyntaxError(
                f'Invalid motor interface {raw_iface!r} at line {line_num}. '
                'Must be STEP_DIR, CAN_BUS, or SERIAL'
            ) from exc

        motor_config: MotorConfig = MotorFactory.create(
            mode=drive_mode,
            interface_type=interface_type,
            axis_mask=AxisMask.ALL,
        )

        return ScaraInstruction(
            command_type=ScaraCommandType.CONFIG_MOTOR,
            line_number=line_num,
            raw_text=raw_text,
            parameters={
                ScaraInstructionParam.MODE: motor_config.mode.value,
                ScaraInstructionParam.INTERFACE: motor_config.interface_type.value,
                ScaraInstructionParam.AXIS_MASK: motor_config.axis_mask.value,
            },
        )
