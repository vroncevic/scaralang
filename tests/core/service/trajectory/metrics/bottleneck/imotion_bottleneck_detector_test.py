# -*- coding: UTF-8 -*-

'''
Module
    imotion_bottleneck_detector_test.py
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

from unittest import TestCase
from unittest import main

from scaralang.core.service.trajectory.metrics.bottleneck.imotion_bottleneck_detector import IMotionBottleneckDetector
from scaralang.core.service.trajectory.metrics.bottleneck.motion_bottleneck_detector import MotionBottleneckDetector
from scaralang.core.service.trajectory.metrics.bottleneck.motion_bottleneck_detector_factory import MotionBottleneckDetectorFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.7'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestIMotionBottleneckDetector(TestCase):
    '''
        Test cases for IMotionBottleneckDetector protocol structural typing.

        It defines:

            :methods:
                | test_structural_conformance - Verifies detector satisfies protocol.
                | test_factory_conformance - Verifies factory returns protocol instance.
                | test_detector_name - Verifies detector name property.
    '''

    def test_structural_conformance(self) -> None:
        '''Verifies MotionBottleneckDetector satisfies protocol.'''
        detector = MotionBottleneckDetector()
        self.assertIsInstance(detector, IMotionBottleneckDetector)

    def test_factory_conformance(self) -> None:
        '''Verifies factory returns instance satisfying protocol.'''
        detector = MotionBottleneckDetectorFactory.create()
        self.assertIsInstance(detector, IMotionBottleneckDetector)

    def test_detector_name(self) -> None:
        '''Verifies detector name property.'''
        detector = MotionBottleneckDetector()
        self.assertEqual(detector.name, 'motion_bottleneck_detector')


if __name__ == '__main__':
    main()
