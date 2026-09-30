# -*- coding: UTF-8 -*-

'''
Module
    itrajectory_cycle_summary_builder_test.py
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
    Unit tests for ITrajectoryCycleSummaryBuilder protocol.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.service.trajectory.metrics.summary.itrajectory_cycle_summary_builder import ITrajectoryCycleSummaryBuilder
from scaralang.core.service.trajectory.metrics.summary.trajectory_cycle_summary_builder_factory import TrajectoryCycleSummaryBuilderFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestITrajectoryCycleSummaryBuilder(TestCase):
    '''
        Test cases for ITrajectoryCycleSummaryBuilder protocol structural typing.

        It defines:

            :methods:
                | test_factory_conformance - Verifies factory returns protocol instance.
                | test_builder_name - Verifies builder name property.
    '''

    def test_factory_conformance(self) -> None:
        '''Verifies factory returns instance satisfying protocol.'''
        builder = TrajectoryCycleSummaryBuilderFactory.create()
        self.assertIsInstance(builder, ITrajectoryCycleSummaryBuilder)

    def test_builder_name(self) -> None:
        '''Verifies builder name property.'''
        builder = TrajectoryCycleSummaryBuilderFactory.create()
        self.assertEqual(builder.name, 'trajectory_cycle_summary_builder')


if __name__ == '__main__':
    main()
