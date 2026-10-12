# -*- coding: UTF-8 -*-

'''
Module
    imetrics_test.py
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
    Unit tests for ITrajectoryMetrics protocol.
'''

from __future__ import annotations

from unittest import TestCase, main

from scaralang.core.service.trajectory.metrics.factory import MetricsFactory
from scaralang.core.service.trajectory.metrics.imetrics import ITrajectoryMetrics
from scaralang.core.service.trajectory.metrics.metrics import TrajectoryMetrics

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.8'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class NonConformingTrajectoryMetrics:  # pylint: disable=too-few-public-methods
    '''Dummy class not implementing ITrajectoryMetrics.'''


class TestITrajectoryMetrics(TestCase):
    '''
        Test cases for ITrajectoryMetrics structural protocol conformance.

        It defines:

            :methods:
                | test_structural_conformance - Verifies metrics satisfies protocol.
                | test_factory_conformance - Verifies factory returns protocol instance.
                | test_non_conforming_instance - Verifies non-conforming object rejected.
    '''

    def test_structural_conformance(self) -> None:
        '''Verifies TrajectoryMetrics satisfies ITrajectoryMetrics protocol.'''
        metrics = TrajectoryMetrics()
        self.assertIsInstance(metrics, ITrajectoryMetrics)

    def test_factory_conformance(self) -> None:
        '''Verifies factory returns instance satisfying ITrajectoryMetrics.'''
        provides = MetricsFactory.create()
        self.assertIsInstance(provides.metrics, ITrajectoryMetrics)

    def test_non_conforming_instance(self) -> None:
        '''Verifies non-conforming object is rejected by runtime_checkable protocol.'''
        dummy = NonConformingTrajectoryMetrics()
        self.assertNotIsInstance(dummy, ITrajectoryMetrics)


if __name__ == '__main__':
    main()
