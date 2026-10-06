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
    Defines ReplCommandDefinition class for CLI repl subcommand.
'''

from __future__ import annotations

from collections.abc import Sequence

from ats_utilities.option.command.data import OptionData
from ats_utilities.utils.reflection import to_str

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.6'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ReplCommandDefinition:
    '''
        CLI subcommand metadata definition for launching the interactive REPL console.

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
        return 'repl'

    @property
    def help_text(self) -> str:
        '''
            Returns the command help text.

            :return: The command help text.
            :exceptions: None.
        '''
        return 'Launch interactive SCARA DSL motion console (REPL)'

    @property
    def options(self) -> Sequence[OptionData]:
        '''
            Returns the command options.

            :return: Sequence of command options.
            :exceptions: None.
        '''
        return [
            OptionData(
                name='--endpoint',
                help_text='Target connection endpoint (e.g. host:port, serial port, or dry-run)',
                action=None,
                default='dry-run',
                required=False,
                choices=None,
                nargs=None,
            ),
            OptionData(
                name='--dry-run',
                help_text='Run in offline simulation mode without hardware transmission',
                action='store_true',
                default=False,
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
