# -*- coding: UTF-8 -*-

'''
Module
    definition.py
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
    Defines ExportCommandDefinition class for CLI export subcommand.
'''

from __future__ import annotations

from collections.abc import Sequence

from ats_utilities.option.command.data import OptionData
from ats_utilities.utils.reflection import to_str

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.5'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ExportCommandDefinition:
    '''
        CLI subcommand metadata definition for exporting trajectories to multiple targets.

        It defines:

            :methods:
                | name - Returns the command name.
                | help_text - Returns the command help text.
                | options - Returns the sequence of command options.
                | __str__ - Returns the command definition as string representation.
    '''

    @property
    def name(self) -> str:
        '''
            Returns the command name.

            :return: The command name.
            :exceptions: None.
        '''
        return 'export'

    @property
    def help_text(self) -> str:
        '''
            Returns the command help text.

            :return: The command help text.
            :exceptions: None.
        '''
        return 'Export a .scara DSL script to G-code, CSV, JSON, or SVG format'

    @property
    def options(self) -> Sequence[OptionData]:
        '''
            Returns the command options.

            :return: Sequence of command options.
            :exceptions: None.
        '''
        return [
            OptionData(
                name='--script',
                help_text='Path to input .scara DSL source file',
                action=None,
                default=None,
                required=True,
                choices=None,
                nargs=None,
            ),
            OptionData(
                name='--format',
                help_text='Target format: gcode, csv, json, svg, or scara',
                action=None,
                default='gcode',
                required=False,
                choices=['gcode', 'csv', 'json', 'svg', 'scara'],
                nargs=None,
            ),
            OptionData(
                name='--output',
                help_text='Path to destination output file',
                action=None,
                default=None,
                required=False,
                choices=None,
                nargs=None,
            ),
        ]

    def __str__(self) -> str:
        '''
            Returns the command definition as string.

            :return: String representation of command definition.
            :exceptions: None.
        '''
        return to_str(self)
