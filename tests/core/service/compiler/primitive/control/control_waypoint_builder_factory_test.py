# -*- coding: UTF-8 -*-

'''
Module
    control_waypoint_builder_factory_test.py
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
    Unit tests for ControlWaypointBuilderFactory.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.service.compiler.primitive.control.control_waypoint_builder_factory import ControlWaypointBuilderFactory
from scaralang.core.service.compiler.primitive.control.icontrol_waypoint_builder import IControlWaypointBuilder

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestControlWaypointBuilderFactory(TestCase):
    '''
        Test cases verifying ControlWaypointBuilderFactory functionality.

        It defines:

            :methods:
                | test_create - Verifies factory creates IControlWaypointBuilder instance.
                | test_get_version - Verifies factory returns non-empty version string.
    '''

    def test_create(self) -> None:
        '''
            Verifies create instantiates IControlWaypointBuilder instance.
        '''
        builder = ControlWaypointBuilderFactory.create()
        self.assertIsInstance(builder, IControlWaypointBuilder)

    def test_get_version(self) -> None:
        '''
            Verifies factory version string is non-empty.
        '''
        version = ControlWaypointBuilderFactory.get_version()
        self.assertTrue(bool(version))


if __name__ == '__main__':
    main()
