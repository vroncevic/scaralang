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
    Unit tests for DiscretizerDependencies parameter bundle.
'''

from __future__ import annotations

from dataclasses import FrozenInstanceError
from unittest import TestCase
from unittest import main
from unittest.mock import MagicMock

from scaralang.core.service.compiler.binary.step.discretizer.dependencies import DiscretizerDependencies
from scaralang.core.service.compiler.binary.step.duration.icalculator import ISegmentDurationCalculator
from scaralang.core.service.kinematics.solver.analytical.spatial.isolver import ISpatialKinematicsSolver
from scaralang.core.service.kinematics.solver.numerical.spatial.isolver import INumericalSpatialKinematicsSolver
from scaralang.core.service.kinematics.transmission.iconverter import IJointStepTransmissionConverter

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestDiscretizerDependencies(TestCase):
    '''
        Test cases verifying DiscretizerDependencies dataclass behavior.

        It defines:

            :methods:
                | test_initialization - Verifies attributes are set correctly.
                | test_immutability - Verifies frozen behavior on attribute modification.
    '''

    def test_initialization(self) -> None:
        '''
            Verifies attributes are set correctly.

            :exceptions: None.
        '''
        mock_spatial = MagicMock(spec=ISpatialKinematicsSolver)
        mock_numerical = MagicMock(spec=INumericalSpatialKinematicsSolver)
        mock_transmission = MagicMock(spec=IJointStepTransmissionConverter)
        mock_duration = MagicMock(spec=ISegmentDurationCalculator)
        deps = DiscretizerDependencies(
            spatial=mock_spatial,
            numerical_spatial=mock_numerical,
            transmission=mock_transmission,
            duration_calculator=mock_duration,
        )
        self.assertIs(deps.spatial, mock_spatial)
        self.assertIs(deps.numerical_spatial, mock_numerical)
        self.assertIs(deps.transmission, mock_transmission)
        self.assertIs(deps.duration_calculator, mock_duration)

    def test_immutability(self) -> None:
        '''
            Verifies frozen behavior on attribute modification.

            :exceptions: None.
        '''
        mock_spatial = MagicMock(spec=ISpatialKinematicsSolver)
        mock_numerical = MagicMock(spec=INumericalSpatialKinematicsSolver)
        mock_transmission = MagicMock(spec=IJointStepTransmissionConverter)
        mock_duration = MagicMock(spec=ISegmentDurationCalculator)
        deps = DiscretizerDependencies(
            spatial=mock_spatial,
            numerical_spatial=mock_numerical,
            transmission=mock_transmission,
            duration_calculator=mock_duration,
        )
        with self.assertRaises(FrozenInstanceError):
            deps.spatial = mock_spatial


if __name__ == '__main__':
    main()
