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
    Unit tests for ShapeFactory class.
'''

from __future__ import annotations

from unittest import TestCase, main

from scaralang.core.service.trajectory.avoidance.bypass.arc.factory import ArcFactory
from scaralang.core.service.trajectory.avoidance.bypass.dependencies import BypassDependencies
from scaralang.core.service.trajectory.avoidance.bypass.factory import BypassFactory
from scaralang.core.service.trajectory.avoidance.shape.dependencies import ShapeDependencies
from scaralang.core.service.trajectory.avoidance.shape.factory import ShapeFactory
from scaralang.core.service.trajectory.avoidance.shape.iplanner import IAvoidanceShapePlanner
from scaralang.core.service.trajectory.avoidance.shape.provides import ShapeProvides
from scaralang.core.service.trajectory.avoidance.validation.factory import ValidationFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.9'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestShapeFactory(TestCase):
    '''
        Test cases for ShapeFactory creation logic.

        It defines:

            :methods:
                | test_create - Verifies factory builds ShapeProvides instance.
                | test_get_version - Verifies factory version string representation.
    '''

    def test_create(self) -> None:
        '''Verifies factory builds ShapeProvides with injected dependencies.'''
        validator = ValidationFactory.create(dead_zone_radius=86.0).validator
        calculator = ArcFactory.create().calculator
        deps = BypassDependencies(
            validator=validator,
            calculator=calculator,
            safety_margin_mm=5.0,
        )
        bypass_planner = BypassFactory.create(dependencies=deps).planner
        shape_deps = ShapeDependencies(
            validator=validator,
            bypass_planner=bypass_planner,
        )
        provides: ShapeProvides = ShapeFactory.create(dependencies=shape_deps)
        self.assertIsInstance(provides, ShapeProvides)
        self.assertIsInstance(provides.planner, IAvoidanceShapePlanner)

    def test_get_version(self) -> None:
        '''Verifies factory version getter.'''
        self.assertIsInstance(ShapeFactory.get_version(), str)
        self.assertTrue(len(ShapeFactory.get_version()) > 0)


if __name__ == '__main__':
    main()
