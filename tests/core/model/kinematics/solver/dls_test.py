# -*- coding: UTF-8 -*-

'''
Module
    dls_test.py
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
    Unit tests for DlsConfig model.
'''

from __future__ import annotations

from unittest import TestCase, main

from scaralang.core.model.kinematics.solver.dls import DlsConfig

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DlsTest(TestCase):
    '''
        Test cases verifying DlsConfig defaults and custom attributes.

        It defines:

            :methods:
                | test_default_values - Verifies default parameter values.
                | test_custom_values - Verifies customized parameter instantiation.
    '''

    def test_default_values(self) -> None:
        '''
            Verifies default parameters meet expected baseline values.

            :exceptions: None.
        '''
        config = DlsConfig()
        self.assertEqual(config.damping, 0.05)
        self.assertEqual(config.max_iterations, 50)
        self.assertEqual(config.tolerance_mm, 0.01)
        self.assertEqual(config.step_limit_rad, 0.2)

    def test_custom_values(self) -> None:
        '''
            Verifies custom values are stored accurately.

            :exceptions: None.
        '''
        config = DlsConfig(
            damping=0.1,
            max_iterations=100,
            tolerance_mm=0.005,
            step_limit_rad=0.15,
        )
        self.assertEqual(config.damping, 0.1)
        self.assertEqual(config.max_iterations, 100)
        self.assertEqual(config.tolerance_mm, 0.005)
        self.assertEqual(config.step_limit_rad, 0.15)


if __name__ == '__main__':
    main()
