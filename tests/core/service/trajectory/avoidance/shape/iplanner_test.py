# -*- coding: UTF-8 -*-

'''
Module
    iplanner_test.py
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
    Unit tests for IAvoidanceShapePlanner protocol.
'''

from __future__ import annotations

from unittest import TestCase, main

from scaralang.core.service.trajectory.avoidance.bypass.arc.factory import ArcFactory
from scaralang.core.service.trajectory.avoidance.bypass.planner.dependencies import PlannerDependencies
from scaralang.core.service.trajectory.avoidance.bypass.planner.factory import PlannerFactory
from scaralang.core.service.trajectory.avoidance.shape.dependencies import ShapeDependencies
from scaralang.core.service.trajectory.avoidance.shape.factory import ShapeFactory
from scaralang.core.service.trajectory.avoidance.shape.iplanner import IAvoidanceShapePlanner
from scaralang.core.service.trajectory.avoidance.shape.planner import AvoidanceShapePlanner
from scaralang.core.service.trajectory.avoidance.validation.factory import ValidationFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.8'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestIAvoidanceShapePlanner(TestCase):
    '''
        Test cases for IAvoidanceShapePlanner structural protocol conformance.

        It defines:

            :methods:
                | test_structural_conformance - Verifies AvoidanceShapePlanner satisfies protocol.
                | test_factory_return_conformance - Verifies factory returns protocol instance.
    '''

    def test_structural_conformance(self) -> None:
        '''Verifies concrete AvoidanceShapePlanner satisfies IAvoidanceShapePlanner protocol.'''
        validator = ValidationFactory.create(dead_zone_radius=86.0).validator
        calculator = ArcFactory.create().calculator
        planner_deps = PlannerDependencies(
            validator=validator,
            calculator=calculator,
            safety_margin_mm=5.0,
            angular_step_rad=0.1,
        )
        bypass_planner = PlannerFactory.create(dependencies=planner_deps).planner
        shape_deps = ShapeDependencies(
            validator=validator,
            bypass_planner=bypass_planner,
        )
        planner = AvoidanceShapePlanner(dependencies=shape_deps)
        self.assertIsInstance(planner, IAvoidanceShapePlanner)

    def test_factory_return_conformance(self) -> None:
        '''Verifies factory returns instance satisfying IAvoidanceShapePlanner.'''
        validator = ValidationFactory.create(dead_zone_radius=86.0).validator
        calculator = ArcFactory.create().calculator
        planner_deps = PlannerDependencies(
            validator=validator,
            calculator=calculator,
            safety_margin_mm=5.0,
            angular_step_rad=0.1,
        )
        bypass_planner = PlannerFactory.create(dependencies=planner_deps).planner
        shape_deps = ShapeDependencies(
            validator=validator,
            bypass_planner=bypass_planner,
        )
        provides = ShapeFactory.create(dependencies=shape_deps)
        self.assertIsInstance(provides.planner, IAvoidanceShapePlanner)


if __name__ == '__main__':
    main()
