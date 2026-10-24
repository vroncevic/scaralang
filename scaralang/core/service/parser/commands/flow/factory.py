# -*- coding: UTF-8 -*-

'''
Module
    factory.py
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
    Factory instantiating and wiring flow command parser components.
'''

from __future__ import annotations

from scaralang.core.service.parser.commands.flow.disable import DisableParser
from scaralang.core.service.parser.commands.flow.enable import EnableParser
from scaralang.core.service.parser.commands.flow.estop import EstopParser
from scaralang.core.service.parser.commands.flow.hold import HoldParser
from scaralang.core.service.parser.commands.flow.provides import FlowProvides
from scaralang.core.service.parser.commands.flow.resume import ResumeParser
from scaralang.core.service.parser.commands.flow.sync import SyncParser
from scaralang.core.service.parser.commands.flow.wait import WaitParser

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class FlowFactory:
    '''
        Factory providing configured FlowProvides subsystem instances.

        It defines:

            :methods:
                | create - Constructs and wires FlowProvides container.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(cls) -> FlowProvides:
        '''
            Constructs and wires FlowProvides container with command parsers.

            :return: Fully configured FlowProvides container.
            :exceptions: None.
        '''
        return FlowProvides(
            parsers=(
                WaitParser(),
                SyncParser(),
                HoldParser(),
                ResumeParser(),
                EnableParser(),
                DisableParser(),
                EstopParser(),
            ),
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory version string.

            :return: Factory version string.
            :exceptions: None.
        '''
        return __version__
