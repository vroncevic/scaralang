# -*- coding: UTF-8 -*-

'''
Module
    home_factory_test.py
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
    Unit tests for HomePoseCalculatorFactory instantiation and version verification.
'''

from __future__ import annotations

from unittest import TestCase, main

from scaralang.core.model.kinematics.profile.bounds import ScaraBounds
from scaralang.core.service.kinematics.envelope.home import HomePoseCalculator
from scaralang.core.service.kinematics.envelope.home_factory import HomePoseCalculatorFactory
from scaralang.core.service.kinematics.envelope.ihome import IHomePoseCalculator
from scaralang.core.service.kinematics.profile.default_scara_profile import DefaultScaraProfile

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestHomePoseCalculatorFactory(TestCase):
    '''
        Validates HomePoseCalculatorFactory instantiation and version contract.

        It defines:

            :methods:
                | test_create_calculator - Verifies factory creates HomePoseCalculator.
                | test_get_version - Verifies factory component version.
    '''

    def test_create_calculator(self) -> None:
        '''
            Verifies factory instantiates HomePoseCalculator conforming to protocol.
        '''
        bounds: ScaraBounds = DefaultScaraProfile.create_bounds()
        calculator: HomePoseCalculator = HomePoseCalculatorFactory.create(bounds=bounds)

        self.assertIsInstance(calculator, HomePoseCalculator)
        self.assertIsInstance(calculator, IHomePoseCalculator)

    def test_get_version(self) -> None:
        '''
            Verifies factory component version string.
        '''
        self.assertEqual(HomePoseCalculatorFactory.get_version(), '1.1.1')


if __name__ == '__main__':
    main()
