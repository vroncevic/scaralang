# -*- coding: UTF-8 -*-

'''
Module
    event.py
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
    Defines MoveEventType enumeration for binary wire motion event notifications.
'''

from __future__ import annotations

from enum import IntEnum, unique

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@unique
class MoveEventType(IntEnum):
    '''
        Motion execution event notification codes for RESP_MOVE_EVENT.

        It defines:

            :attributes:
                | START - Motion step execution started (1).
                | DONE - Motion step execution successfully completed (2).
                | FAILED - Motion step execution failed or aborted (3).
    '''

    START = 1
    DONE = 2
    FAILED = 3
