# -*- coding: UTF-8 -*-

'''
Module
    disassemble_summary_formatter_factory.py
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
    Defines DisassembleSummaryFormatterFactory for instantiating DisassembleSummaryFormatter.
'''

from __future__ import annotations

from scaralang.infrastructure.command.disassemble.format.disassemble_summary_formatter import DisassembleSummaryFormatter

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DisassembleSummaryFormatterFactory:
    '''
        Factory instantiating DisassembleSummaryFormatter instances.

        It defines:

            :methods:
                | create - Instantiates a new DisassembleSummaryFormatter instance.
                | create_default - Instantiates default DisassembleSummaryFormatter.
    '''

    @classmethod
    def create(cls) -> DisassembleSummaryFormatter:
        '''
            Creates a new DisassembleSummaryFormatter instance.

            :return: Configured DisassembleSummaryFormatter instance.
        '''
        return DisassembleSummaryFormatter()

    @classmethod
    def create_default(cls) -> DisassembleSummaryFormatter:
        '''
            Creates a default DisassembleSummaryFormatter instance.

            :return: Default DisassembleSummaryFormatter instance.
        '''
        return cls.create()
