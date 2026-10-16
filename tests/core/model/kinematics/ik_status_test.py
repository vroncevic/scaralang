# -*- coding: UTF-8 -*-

'''
Module
    ik_status_test.py
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
    Unit tests for IkStatus enumeration.
'''

from __future__ import annotations

from unittest import TestCase, main
from scaralang.core.model.kinematics.ik_status import IkStatus

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.9'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestIkStatus(TestCase):
    '''Unit tests validating IkStatus enumeration members and string values.'''

    def test_members(self) -> None:
        '''Verify enum member values match expected strings.'''
        self.assertEqual(IkStatus.SUCCESS, 'SUCCESS')
        self.assertEqual(IkStatus.OUT_OF_REACH, 'OUT_OF_REACH')
        self.assertEqual(IkStatus.INNER_DEADZONE, 'INNER_DEADZONE')
        self.assertEqual(IkStatus.Z_LIMIT_EXCEEDED, 'Z_LIMIT_EXCEEDED')
        self.assertEqual(IkStatus.JOINT_LIMIT_EXCEEDED, 'JOINT_LIMIT_EXCEEDED')
        self.assertEqual(IkStatus.SINGULARITY, 'SINGULARITY')

    def test_iteration(self) -> None:
        '''Verify all expected members exist in enumeration.'''
        members = list(IkStatus)
        self.assertEqual(len(members), 6)


if __name__ == '__main__':
    main()
