# -*- coding: UTF-8 -*-

'''
Module
    ienvelope_test.py
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
    Unit tests for IWorkspaceEnvelope protocol contract.
'''

from __future__ import annotations

from typing import Protocol
from unittest import TestCase
from unittest import main

from scaralang.core.service.kinematics.envelope.ienvelope import IWorkspaceEnvelope

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestIWorkspaceEnvelope(TestCase):
    '''
        Validates IWorkspaceEnvelope protocol contract.

        It defines:

            :methods:
                | test_is_protocol - Verifies IWorkspaceEnvelope is a Protocol.
                | test_required_attributes - Verifies protocol property definitions.
    '''

    def test_is_protocol(self) -> None:
        '''Verifies that IWorkspaceEnvelope is a runtime checkable Protocol.'''
        self.assertTrue(issubclass(IWorkspaceEnvelope, Protocol))

    def test_required_attributes(self) -> None:
        '''Verifies that protocol defines expected methods and properties.'''
        expected_members: tuple[str, ...] = (
            'bounds',
            'r_min',
            'r_max',
            'safe_r_max',
            'get_version',
        )

        for member in expected_members:
            self.assertTrue(
                hasattr(IWorkspaceEnvelope, member),
                f'IWorkspaceEnvelope missing contract member: {member}',
            )


if __name__ == '__main__':
    main()
