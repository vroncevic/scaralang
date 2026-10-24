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
    Unit tests for DefaultShapeFactory infrastructure factory.
'''

from __future__ import annotations

from unittest import TestCase, main

from scaralang.core.model.kinematics.profile.bounds import ScaraBounds
from scaralang.core.service.kinematics.profile.default_scara_profile import DefaultScaraProfile
from scaralang.core.service.trajectory.avoidance.shape.iplanner import IAvoidanceShapePlanner
from scaralang.core.service.trajectory.avoidance.shape.provides import ShapeProvides
from scaralang.infrastructure.trajectory.avoidance.shape.dependencies import DefaultShapeDependencies
from scaralang.infrastructure.trajectory.avoidance.shape.factory import DefaultShapeFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestDefaultShapeFactory(TestCase):
    '''
        Test cases for DefaultShapeFactory composition logic.

        It defines:

            :methods:
                | test_create - Verifies factory builds ShapeProvides with configured planner.
                | test_get_version - Verifies factory version string representation.
    '''

    def test_create(self) -> None:
        '''Verifies factory builds ShapeProvides from default dependencies.'''
        bounds: ScaraBounds = DefaultScaraProfile.create_bounds()
        dependencies = DefaultShapeDependencies(bounds=bounds)
        provides: ShapeProvides = DefaultShapeFactory.create(dependencies=dependencies)
        self.assertIsInstance(provides, ShapeProvides)
        self.assertIsInstance(provides.planner, IAvoidanceShapePlanner)

    def test_get_version(self) -> None:
        '''Verifies factory version getter.'''
        self.assertIsInstance(DefaultShapeFactory.get_version(), str)
        self.assertTrue(len(DefaultShapeFactory.get_version()) > 0)


if __name__ == '__main__':
    main()
