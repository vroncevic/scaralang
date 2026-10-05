# -*- coding: UTF-8 -*-

'''
Module
    iprogram_inspection_presenter.py
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
    Defines structural interface protocol for binary program frame inspection reports.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from scaralang.core.model.dsl.binary.program import BinaryProgram

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.5'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IProgramInspectionPresenter(Protocol):
    '''
        Structural interface protocol for presenting full binary program frame inspection.

        It defines:

            :methods:
                | present_program - Formats compiled BinaryProgram into inspection report.
                | get_version - Returns the interface protocol version identifier.
    '''

    def present_program(self, *, program: BinaryProgram) -> str:
        '''
            Renders complete frame inspection report for a compiled binary program.

            :param program: Compiled BinaryProgram containing steps and raw bytes.
            :return: Formatted multi-line inspection report.
        '''

    def get_version(self) -> str:
        '''
            Returns the interface protocol version identifier.

            :return: The protocol version string.
        '''
