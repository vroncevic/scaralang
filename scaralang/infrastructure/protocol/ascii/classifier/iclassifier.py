# -*- coding: UTF-8 -*-

'''
Module
    iclassifier.py
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
    Defines IFlowStatusClassifier structural protocol for ASCII response evaluation.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.9'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IFlowStatusClassifier(Protocol):
    '''
        Structural protocol defining ASCII line status and flow control evaluation.

        It defines:

            :methods:
                | is_buffer_full - Checks if packet indicates microcontroller buffer saturation.
                | is_error - Checks if packet signals an error or fault condition.
                | is_ack - Checks if packet signals positive acknowledgment.
                | parse_queue_depth - Extracts remote queue depth integer from line.
                | get_version - Returns classifier version string.
    '''

    def is_buffer_full(self, line: str) -> bool:
        '''
            Checks if packet indicates microcontroller buffer saturation.

            :param line: Received line string.
            :return: True if buffer full packet, False otherwise.
            :exceptions: None.
        '''

    def is_error(self, line: str) -> bool:
        '''
            Checks if packet signals an error or fault condition.

            :param line: Received line string.
            :return: True if error condition, False otherwise.
            :exceptions: None.
        '''

    def is_ack(self, line: str) -> bool:
        '''
            Checks if packet signals positive acknowledgment.

            :param line: Received line string.
            :return: True if positive acknowledgment, False otherwise.
            :exceptions: None.
        '''

    def parse_queue_depth(self, line: str) -> int:
        '''
            Extracts remote queue depth integer from ACK packet.

            :param line: Received line string.
            :return: Integer queue depth count (0 if not present).
            :exceptions: None.
        '''

    def get_version(self) -> str:
        '''
            Returns the classifier version string.

            :return: Semantic version string.
            :exceptions: None.
        '''
