# -*- coding: UTF-8 -*-

'''
Module
    elbow_test.py
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
    Unit testing for ElbowConfig enumeration.
'''

from __future__ import annotations

from unittest import TestCase, main

from scaralang.core.model.kinematics.solver.elbow import ElbowConfig

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ElbowTest(TestCase):
    '''
        Validates member values and string equality of ElbowConfig enumeration.

        It defines:

            :methods:
                | test_members - Verifies all enumeration members.
                | test_value_instantiation - Verifies instantiation from string literals.
    '''

    def test_members(self) -> None:
        '''
            Verifies all enumeration members and their exact string representations.

            :exceptions: None.
        '''
        self.assertEqual(ElbowConfig.RIGHT, 'RIGHT')
        self.assertEqual(ElbowConfig.LEFT, 'LEFT')
        self.assertEqual(len(ElbowConfig), 2)

    def test_value_instantiation(self) -> None:
        '''
            Verifies instantiation from string literals.

            :exceptions: None.
        '''
        self.assertIs(ElbowConfig('RIGHT'), ElbowConfig.RIGHT)
        self.assertIs(ElbowConfig('LEFT'), ElbowConfig.LEFT)


if __name__ == '__main__':
    main()
