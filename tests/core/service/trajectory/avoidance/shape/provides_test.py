# -*- coding: UTF-8 -*-

'''
Module
    provides_test.py
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
    Unit tests for ShapeProvides dataclass.
'''

from __future__ import annotations

from dataclasses import FrozenInstanceError
from unittest import TestCase, main

from scaralang.core.service.trajectory.avoidance.bypass.arc.factory import ArcFactory
from scaralang.core.service.trajectory.avoidance.bypass.dependencies import BypassDependencies
from scaralang.core.service.trajectory.avoidance.bypass.factory import BypassFactory
from scaralang.core.service.trajectory.avoidance.shape.dependencies import ShapeDependencies
from scaralang.core.service.trajectory.avoidance.shape.planner import AvoidanceShapePlanner
from scaralang.core.service.trajectory.avoidance.shape.provides import ShapeProvides
from scaralang.core.service.trajectory.avoidance.validation.factory import ValidationFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestShapeProvides(TestCase):
    '''
        Test cases for ShapeProvides container dataclass.

        It defines:

            :attributes:
                | planner - Instance of AvoidanceShapePlanner.
            :methods:
                | setUp - Prepares AvoidanceShapePlanner fixture.
                | test_provides_attributes - Verifies planner instance exposed properly.
                | test_provides_immutability - Verifies frozen immutability of bundle.
    '''

    planner: AvoidanceShapePlanner

    def setUp(self) -> None:
        '''
            Prepares AvoidanceShapePlanner fixture.

            :exceptions: None.
        '''
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
        self.planner = AvoidanceShapePlanner(dependencies=shape_deps)

    def test_provides_attributes(self) -> None:
        '''
            Verifies planner attribute is properly exposed.

            :exceptions: None.
        '''
        provides = ShapeProvides(planner=self.planner)
        self.assertIs(provides.planner, self.planner)

    def test_provides_immutability(self) -> None:
        '''
            Verifies frozen dataclass immutability.

            :exceptions: None.
        '''
        provides = ShapeProvides(planner=self.planner)
        with self.assertRaises(FrozenInstanceError):
            provides.planner = None  # type: ignore[misc]


if __name__ == '__main__':
    main()
