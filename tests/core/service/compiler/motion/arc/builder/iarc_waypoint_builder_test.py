# -*- coding: UTF-8 -*-

'''
Module
    iarc_waypoint_builder_test.py
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
    Unit tests for IArcWaypointBuilder protocol contract.
'''

from __future__ import annotations

from typing import Protocol
from unittest import TestCase
from unittest import main

from scaralang.core.service.compiler.motion.arc.builder.iarc_waypoint_builder import IArcWaypointBuilder

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.7'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestIArcWaypointBuilder(TestCase):
    '''
        Test cases verifying IArcWaypointBuilder protocol contract.

        It defines:

            :methods:
                | test_protocol_definition - Verifies protocol methods.
                | test_protocol_runtime_check - Verifies protocol runtime check with non-conforming object.
    '''

    def test_protocol_definition(self) -> None:
        '''
            Verifies that IArcWaypointBuilder defines required methods.
        '''
        self.assertTrue(issubclass(IArcWaypointBuilder, Protocol))
        self.assertTrue(hasattr(IArcWaypointBuilder, 'build_waypoints'))
        self.assertTrue(hasattr(IArcWaypointBuilder, 'get_version'))

    def test_protocol_runtime_check(self) -> None:
        '''
            Verifies non-conforming object fails runtime protocol check.
        '''
        self.assertFalse(isinstance(object(), IArcWaypointBuilder))



if __name__ == '__main__':
    main()
