# -*- coding: UTF-8 -*-

'''
Module
    ianalyzer_test.py
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

from unittest import TestCase, main

from scaralang.core.service.trajectory.metrics.profile.analyzer import AxisSpeedProfileAnalyzer
from scaralang.core.service.trajectory.metrics.profile.factory import ProfileFactory
from scaralang.core.service.trajectory.metrics.profile.ianalyzer import IAxisSpeedProfileAnalyzer

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.9'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class NonConformingSpeedAnalyzer:  # pylint: disable=too-few-public-methods
    '''Dummy class not implementing IAxisSpeedProfileAnalyzer.'''


class TestIAxisSpeedProfileAnalyzer(TestCase):
    '''
        Test cases for IAxisSpeedProfileAnalyzer structural protocol conformance.

        It defines:

            :methods:
                | test_structural_conformance - Verifies AxisSpeedProfileAnalyzer satisfies protocol.
                | test_factory_conformance - Verifies factory returns protocol instance.
                | test_non_conforming_instance - Verifies non-conforming object rejected.
                | test_analyzer_name - Verifies analyzer name property.
    '''

    def test_structural_conformance(self) -> None:
        '''Verifies concrete AxisSpeedProfileAnalyzer satisfies protocol.'''
        analyzer = AxisSpeedProfileAnalyzer()
        self.assertIsInstance(analyzer, IAxisSpeedProfileAnalyzer)

    def test_factory_conformance(self) -> None:
        '''Verifies factory returns instance satisfying protocol.'''
        provides = ProfileFactory.create()
        self.assertIsInstance(provides.analyzer, IAxisSpeedProfileAnalyzer)

    def test_non_conforming_instance(self) -> None:
        '''Verifies non-conforming object is rejected by runtime_checkable protocol.'''
        dummy = NonConformingSpeedAnalyzer()
        self.assertNotIsInstance(dummy, IAxisSpeedProfileAnalyzer)

    def test_analyzer_name(self) -> None:
        '''Verifies analyzer name property returns expected identifier string.'''
        analyzer = AxisSpeedProfileAnalyzer()
        self.assertEqual(analyzer.name, 'axis_speed_profile_analyzer')


if __name__ == '__main__':
    main()
