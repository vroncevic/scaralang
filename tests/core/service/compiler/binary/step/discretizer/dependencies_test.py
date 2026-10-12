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
from scaralang.core.service.kinematics.iservice import IKinematicsService
from scaralang.core.service.kinematics.transmission.iconverter import IJointStepTransmissionConverter

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.8'
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
        '''Verifies attributes are set correctly.'''
        mock_kinematics = MagicMock(spec=IKinematicsService)
        mock_transmission = MagicMock(spec=IJointStepTransmissionConverter)
        deps = DiscretizerDependencies(
            kinematics=mock_kinematics,
            transmission=mock_transmission,
        )
        self.assertIs(deps.kinematics, mock_kinematics)
        self.assertIs(deps.transmission, mock_transmission)

    def test_immutability(self) -> None:
        '''Verifies frozen behavior on attribute modification.'''
        mock_kinematics = MagicMock(spec=IKinematicsService)
        mock_transmission = MagicMock(spec=IJointStepTransmissionConverter)
        deps = DiscretizerDependencies(
            kinematics=mock_kinematics,
            transmission=mock_transmission,
        )
        with self.assertRaises(FrozenInstanceError):
            deps.kinematics = mock_kinematics  # type: ignore[misc]


if __name__ == '__main__':
    main()
