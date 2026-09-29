# -*- coding: UTF-8 -*-

'''
Module
    iarc_interpolator_test.py
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
    Unit tests for IArcInterpolator protocol.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.model.dsl.compiler.arc_geometry import ArcGeometry
from scaralang.core.model.trajectory.arc_point import ArcPoint
from scaralang.core.service.compiler.motion.arc.interpolation.iarc_interpolator import IArcInterpolator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DummyArcInterpolator:
    '''
        Dummy class implementing IArcInterpolator for protocol verification.
    '''

    def interpolate(
        self,
        *,
        geometry: ArcGeometry,
    ) -> tuple[ArcPoint, ...]:
        '''
            Dummy implementation of interpolate.
        '''
        _ = geometry
        return ()


class IncompleteArcInterpolator:
    '''
        Incomplete dummy class missing interpolate method.
    '''


class TestIArcInterpolator(TestCase):
    '''
        Test cases verifying IArcInterpolator protocol.

        It defines:

            :methods:
                | test_runtime_checkable_satisfied - Verifies conforming class satisfies protocol.
                | test_runtime_checkable_not_satisfied - Verifies incomplete class fails check.
    '''

    def test_runtime_checkable_satisfied(self) -> None:
        '''
            Verifies conforming class passes isinstance check.
        '''
        interpolator = DummyArcInterpolator()
        self.assertIsInstance(interpolator, IArcInterpolator)

    def test_runtime_checkable_not_satisfied(self) -> None:
        '''
            Verifies non-conforming class fails isinstance check.
        '''
        interpolator = IncompleteArcInterpolator()
        self.assertNotIsInstance(interpolator, IArcInterpolator)


if __name__ == '__main__':
    main()
