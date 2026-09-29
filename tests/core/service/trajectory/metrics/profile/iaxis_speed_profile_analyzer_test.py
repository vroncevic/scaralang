# -*- coding: UTF-8 -*-

'''
Module
    iaxis_speed_profile_analyzer_test.py
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
    Unit tests for IAxisSpeedProfileAnalyzer protocol.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.service.trajectory.metrics.profile.axis_speed_profile_analyzer import AxisSpeedProfileAnalyzer
from scaralang.core.service.trajectory.metrics.profile.axis_speed_profile_analyzer_factory import AxisSpeedProfileAnalyzerFactory
from scaralang.core.service.trajectory.metrics.profile.iaxis_speed_profile_analyzer import IAxisSpeedProfileAnalyzer

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestIAxisSpeedProfileAnalyzer(TestCase):
    '''
        Test cases for IAxisSpeedProfileAnalyzer protocol structural typing.

        It defines:

            :methods:
                | test_structural_conformance - Verifies analyzer satisfies protocol.
                | test_factory_conformance - Verifies factory returns protocol instance.
                | test_analyzer_name - Verifies analyzer name property.
    '''

    def test_structural_conformance(self) -> None:
        '''Verifies AxisSpeedProfileAnalyzer satisfies protocol.'''
        analyzer = AxisSpeedProfileAnalyzer()
        self.assertIsInstance(analyzer, IAxisSpeedProfileAnalyzer)

    def test_factory_conformance(self) -> None:
        '''Verifies factory returns instance satisfying protocol.'''
        analyzer = AxisSpeedProfileAnalyzerFactory.create()
        self.assertIsInstance(analyzer, IAxisSpeedProfileAnalyzer)

    def test_analyzer_name(self) -> None:
        '''Verifies analyzer name property.'''
        analyzer = AxisSpeedProfileAnalyzer()
        self.assertEqual(analyzer.name, 'axis_speed_profile_analyzer')


if __name__ == '__main__':
    main()
