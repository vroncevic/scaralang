# -*- coding: UTF-8 -*-

'''
Module
    dependencies_test.py
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
    Unit tests for BinaryDependencies parameter bundle.
'''

from __future__ import annotations

from dataclasses import FrozenInstanceError
from unittest import TestCase, main
from unittest.mock import MagicMock

from scaralang.core.service.compiler.binary.dependencies import BinaryDependencies
from scaralang.core.service.compiler.binary.metrics.icalculator import IMetricsCalculator
from scaralang.core.service.compiler.binary.step.dispatcher.idispatcher import IWaypointStepDispatcher

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestBinaryDependencies(TestCase):
    '''
        Test cases verifying BinaryDependencies dataclass behavior.

        It defines:

            :methods:
                | test_initialization - Verifies attributes are set correctly.
                | test_immutability - Verifies frozen behavior on attribute modification.
    '''

    def test_initialization(self) -> None:
        '''Verifies attributes are set correctly.'''
        mock_dispatcher = MagicMock(spec=IWaypointStepDispatcher)
        mock_calculator = MagicMock(spec=IMetricsCalculator)
        deps = BinaryDependencies(
            step_dispatcher=mock_dispatcher,
            metrics_calculator=mock_calculator,
        )
        self.assertIs(deps.step_dispatcher, mock_dispatcher)
        self.assertIs(deps.metrics_calculator, mock_calculator)

    def test_immutability(self) -> None:
        '''Verifies frozen behavior on attribute modification.'''
        mock_dispatcher = MagicMock(spec=IWaypointStepDispatcher)
        mock_calculator = MagicMock(spec=IMetricsCalculator)
        deps = BinaryDependencies(
            step_dispatcher=mock_dispatcher,
            metrics_calculator=mock_calculator,
        )
        with self.assertRaises(FrozenInstanceError):
            deps.step_dispatcher = mock_dispatcher  # type: ignore[misc]


if __name__ == '__main__':
    main()
