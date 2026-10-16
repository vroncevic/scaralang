# -*- coding: UTF-8 -*-

'''
Module
    idetector_test.py
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
    Unit tests for IMotionBottleneckDetector protocol.
'''

from __future__ import annotations

from unittest import TestCase, main

from scaralang.core.service.trajectory.metrics.bottleneck.detector import MotionBottleneckDetector
from scaralang.core.service.trajectory.metrics.bottleneck.factory import BottleneckFactory
from scaralang.core.service.trajectory.metrics.bottleneck.idetector import IMotionBottleneckDetector

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.9'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class NonConformingBottleneckDetector:  # pylint: disable=too-few-public-methods
    '''Dummy class not implementing IMotionBottleneckDetector.'''


class TestIMotionBottleneckDetector(TestCase):
    '''
        Test cases for IMotionBottleneckDetector structural protocol conformance.

        It defines:

            :methods:
                | test_structural_conformance - Verifies detector satisfies protocol.
                | test_factory_conformance - Verifies factory returns protocol instance.
                | test_non_conforming_instance - Verifies non-conforming object rejected.
                | test_detector_name - Verifies detector name property.
    '''

    def test_structural_conformance(self) -> None:
        '''Verifies MotionBottleneckDetector satisfies protocol.'''
        detector = MotionBottleneckDetector()
        self.assertIsInstance(detector, IMotionBottleneckDetector)

    def test_factory_conformance(self) -> None:
        '''Verifies factory returns instance satisfying protocol.'''
        provides = BottleneckFactory.create()
        self.assertIsInstance(provides.detector, IMotionBottleneckDetector)

    def test_non_conforming_instance(self) -> None:
        '''Verifies non-conforming object is rejected by runtime_checkable protocol.'''
        dummy = NonConformingBottleneckDetector()
        self.assertNotIsInstance(dummy, IMotionBottleneckDetector)

    def test_detector_name(self) -> None:
        '''Verifies detector name property returns expected identifier string.'''
        detector = MotionBottleneckDetector()
        self.assertEqual(detector.name, 'motion_bottleneck_detector')


if __name__ == '__main__':
    main()
