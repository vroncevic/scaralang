# -*- coding: UTF-8 -*-

'''
Module
    classifier_test.py
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
    Unit tests for FlowStatusClassifier ASCII response classifier.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.infrastructure.protocol.ascii.classifier.classifier import FlowStatusClassifier
from scaralang.infrastructure.protocol.ascii.classifier.iclassifier import IFlowStatusClassifier

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.9'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestFlowStatusClassifier(TestCase):
    '''
        Unit test cases verifying FlowStatusClassifier classification rules.

        It defines:

            :methods:
                | setUp - Initializes FlowStatusClassifier test fixture.
                | test_is_buffer_full - Verifies buffer saturation detection.
                | test_is_error - Verifies hardware error and fault detection.
                | test_is_ack - Verifies positive acknowledgment detection.
                | test_parse_queue_depth - Verifies queue depth extraction.
                | test_structural_typing - Verifies instance satisfies IFlowStatusClassifier.
                | test_get_version - Verifies version string retrieval.
    '''

    _classifier: FlowStatusClassifier

    def setUp(self) -> None:
        '''
            Sets up test fixture with FlowStatusClassifier instance.
        '''
        self._classifier = FlowStatusClassifier()

    def test_is_buffer_full(self) -> None:
        '''
            Verifies buffer full detection across different packet variations.
        '''
        self.assertTrue(self._classifier.is_buffer_full('<RESP:FULL#QUEUE=16>'))
        self.assertTrue(self._classifier.is_buffer_full('<FULL>'))
        self.assertTrue(self._classifier.is_buffer_full('<RESP:NACK#BUFFER_FULL>'))
        self.assertFalse(self._classifier.is_buffer_full('<RESP:ACK#QUEUE=5>'))
        self.assertFalse(self._classifier.is_buffer_full('<RESP:ERR#SYNTAX>'))

    def test_is_error(self) -> None:
        '''
            Verifies fault and rejection detection.
        '''
        self.assertTrue(self._classifier.is_error('<RESP:ERR#INVALID_PARAM>'))
        self.assertTrue(self._classifier.is_error('<ERR:INVALID_AXIS>'))
        self.assertTrue(self._classifier.is_error('<RESP:NACK#CHECKSUM>'))
        self.assertTrue(self._classifier.is_error('MOVE_FAILED: COLLISION'))
        self.assertTrue(self._classifier.is_error('HOMED_FAIL: LIMIT_SWITCH'))
        self.assertFalse(self._classifier.is_error('<RESP:ACK#OK>'))

    def test_is_ack(self) -> None:
        '''
            Verifies positive acknowledgment detection.
        '''
        self.assertTrue(self._classifier.is_ack('<RESP:ACK#OK>'))
        self.assertTrue(self._classifier.is_ack('<ACK#QUEUE=3>'))
        self.assertTrue(self._classifier.is_ack('OK'))
        self.assertFalse(self._classifier.is_ack('<RESP:ERR>'))

    def test_parse_queue_depth(self) -> None:
        '''
            Verifies extraction of integer queue depth from packets.
        '''
        self.assertEqual(self._classifier.parse_queue_depth('<RESP:ACK#QUEUE=12>'), 12)
        self.assertEqual(self._classifier.parse_queue_depth('<RESP:ACK#QUEUE=0>'), 0)
        self.assertEqual(self._classifier.parse_queue_depth('<RESP:ACK#OK>'), 0)

    def test_structural_typing(self) -> None:
        '''
            Verifies FlowStatusClassifier satisfies IFlowStatusClassifier protocol.
        '''
        self.assertIsInstance(self._classifier, IFlowStatusClassifier)

    def test_get_version(self) -> None:
        '''
            Verifies get_version returns a valid version string.
        '''
        version: str = self._classifier.get_version()
        self.assertIsInstance(version, str)
        self.assertGreater(len(version), 0)


if __name__ == '__main__':
    main()
