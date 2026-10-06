# -*- coding: UTF-8 -*-

'''
Module
    icommand_compiler.py
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
    Defines ICommandCompiler Protocol for compiling hardware commands into binary steps.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from scaralang.core.model.dsl.binary.step import Step

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.6'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class ICommandCompiler(Protocol):
    '''
        Structural protocol defining contracts for compiling hardware commands into binary steps.

        It defines:

            :methods:
                | compile_command_step - Compiles a command string into a binary command step.
                | get_version - Gets implementation version string.
    '''

    def compile_command_step(self, *, command: str, seq_num: int, line_num: int) -> Step:
        '''
            Compiles a semantic command string into a binary command step.

            :param command: Command text (e.g. PUMP, VALVE, WAIT, HOME).
            :param seq_num: Frame sequence counter.
            :param line_num: Source line index.
            :return: Compiled Step.
        '''

    def get_version(self) -> str:
        '''
            Gets implementation version string.

            :return: Version string.
        '''
