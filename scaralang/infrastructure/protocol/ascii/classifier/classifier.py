# -*- coding: UTF-8 -*-

'''
Module
    classifier.py
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
    Concrete implementation of ASCII flow status and response classifier.
'''

from __future__ import annotations

from re import IGNORECASE, Match, Pattern, compile as re_compile
from typing import ClassVar

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.9'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class FlowStatusClassifier:
    '''
        Evaluates ASCII protocol lines against buffer saturation and fault criteria.

        It defines:

            :attributes:
                | _QUEUE_REGEX - Regular expression extracting QUEUE depth counter.
            :methods:
                | is_buffer_full - Checks if line indicates microcontroller buffer saturation.
                | is_error - Checks if line signals an error or fault condition.
                | is_ack - Checks if line signals positive acknowledgment.
                | parse_queue_depth - Extracts remote queue depth integer from line.
                | get_version - Returns classifier component version string.
    '''

    _QUEUE_REGEX: ClassVar[Pattern[str]] = re_compile(r'QUEUE=(\d+)', IGNORECASE)

    def is_buffer_full(self, line: str) -> bool:
        '''
            Checks if packet indicates microcontroller buffer saturation.

            :param line: Received line string.
            :return: True if buffer full packet, False otherwise.
            :exceptions: None.
        '''
        clean: str = line.strip().upper()

        return (
            'BUFFER_FULL' in clean
            or clean.startswith('<FULL')
            or clean.startswith('<RESP:FULL')
            or ('<RESP:NACK' in clean and 'BUFFER' in clean)
        )

    def is_error(self, line: str) -> bool:
        '''
            Checks if packet signals an error or fault condition.

            :param line: Received line string.
            :return: True if error condition, False otherwise.
            :exceptions: None.
        '''
        clean: str = line.strip().upper()

        return (
            clean.startswith('<RESP:ERR')
            or clean.startswith('<ERR')
            or clean.startswith('<RESP:NACK')
            or 'MOVE_FAILED' in clean
            or 'HOMED_FAIL' in clean
            or 'ERROR' in clean
        )

    def is_ack(self, line: str) -> bool:
        '''
            Checks if packet signals positive acknowledgment.

            :param line: Received line string.
            :return: True if positive acknowledgment, False otherwise.
            :exceptions: None.
        '''
        clean: str = line.strip().upper()

        return (
            clean.startswith('<RESP:ACK')
            or clean.startswith('<ACK')
            or clean == 'OK'
        )

    def parse_queue_depth(self, line: str) -> int:
        '''
            Extracts remote queue depth integer from ACK packet.

            :param line: Received line string.
            :return: Integer queue depth count (0 if not present).
            :exceptions: None.
        '''
        clean: str = line.strip()
        match: Match[str] | None = self._QUEUE_REGEX.search(clean)

        return int(match.group(1)) if match is not None else 0

    def get_version(self) -> str:
        '''
            Returns the classifier version string.

            :return: Version string.
            :exceptions: None.
        '''
        return __version__
