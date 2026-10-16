# -*- coding: UTF-8 -*-

'''
Module
    factory_test.py
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
    Unit tests for StepDiscretizerFactory class.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main
from unittest.mock import MagicMock

from scaralang.core.service.compiler.binary.step.discretizer.dependencies import DiscretizerDependencies
from scaralang.core.service.compiler.binary.step.discretizer.factory import StepDiscretizerFactory
from scaralang.core.service.compiler.binary.step.discretizer.idiscretizer import IStepDiscretizer
from scaralang.core.service.compiler.binary.step.duration.icalculator import ISegmentDurationCalculator
from scaralang.core.service.kinematics.solver.spatial.isolver import ISpatialKinematicsSolver
from scaralang.core.service.kinematics.transmission.iconverter import IJointStepTransmissionConverter

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.9'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestStepDiscretizerFactory(TestCase):
    '''
        Test cases verifying StepDiscretizerFactory.

        It defines:

            :methods:
                | test_create_with_dependencies - Verifies factory returns IStepDiscretizer.
                | test_get_version - Verifies factory version string.
    '''

    def test_create_with_dependencies(self) -> None:
        '''
            Verifies factory returns IStepDiscretizer instance.

            :exceptions: None.
        '''
        mock_spatial = MagicMock(spec=ISpatialKinematicsSolver)
        mock_transmission = MagicMock(spec=IJointStepTransmissionConverter)
        mock_duration = MagicMock(spec=ISegmentDurationCalculator)
        deps = DiscretizerDependencies(
            spatial=mock_spatial,
            transmission=mock_transmission,
            duration_calculator=mock_duration,
        )
        discretizer = StepDiscretizerFactory.create(dependencies=deps)
        self.assertIsInstance(discretizer, IStepDiscretizer)

    def test_get_version(self) -> None:
        '''
            Verifies factory version returns valid string.

            :exceptions: None.
        '''
        self.assertEqual(StepDiscretizerFactory.get_version(), '1.0.9')


if __name__ == '__main__':
    main()
