# -*- coding: UTF-8 -*-

'''
Module
    provides.py
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
    Provides container encapsulating flow command parser components.
'''

from __future__ import annotations

from dataclasses import dataclass

from scaralang.core.service.parser.commands.icommand_parser import ICommandParser

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.8'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(frozen=True, slots=True)
class FlowProvides:
    '''
        Immutable container providing outbound flow command parser interfaces.

        It defines:

            :attributes:
                | disable_parser - Bound ICommandParser for DISABLE.
                | enable_parser - Bound ICommandParser for ENABLE.
                | estop_parser - Bound ICommandParser for ESTOP.
                | hold_parser - Bound ICommandParser for HOLD.
                | resume_parser - Bound ICommandParser for RESUME.
                | sync_parser - Bound ICommandParser for SYNC.
                | wait_parser - Bound ICommandParser for WAIT and WAIT_MS.
                | parsers - Tuple of all registered flow command parsers.
    '''

    disable_parser: ICommandParser
    enable_parser: ICommandParser
    estop_parser: ICommandParser
    hold_parser: ICommandParser
    resume_parser: ICommandParser
    sync_parser: ICommandParser
    wait_parser: ICommandParser
    parsers: tuple[ICommandParser, ...]
