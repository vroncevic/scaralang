# -*- coding: UTF-8 -*-

'''
Module
    scara_kinematics_error_test.py
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
    Unit tests for ScaraKinematicsError exception model.
'''

from __future__ import annotations

from unittest import TestCase, main

from scaralang.core.model.exceptions.scara_error import ScaraError
from scaralang.core.model.exceptions.scara_kinematics_error import ScaraKinematicsError

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.5'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestScaraKinematicsError(TestCase):
    '''Unit tests validating ScaraKinematicsError inheritance and message propagation.'''

    def test_instantiation(self) -> None:
        '''Verify exception instantiation and string representation.'''
        err = ScaraKinematicsError('Target point outside robot reachable workspace')
        self.assertEqual(str(err), 'Target point outside robot reachable workspace')
        self.assertIsInstance(err, ScaraError)
        self.assertIsInstance(err, Exception)

    def test_raising_and_catching(self) -> None:
        '''Verify raising and catching as ScaraKinematicsError and ScaraError.'''
        with self.assertRaises(ScaraError) as ctx:
            raise ScaraKinematicsError('Singularity encountered')
        self.assertIsInstance(ctx.exception, ScaraKinematicsError)
        self.assertEqual(str(ctx.exception), 'Singularity encountered')


if __name__ == '__main__':
    main()
