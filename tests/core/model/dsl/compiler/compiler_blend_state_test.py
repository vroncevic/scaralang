# -*- coding: UTF-8 -*-

'''
Module
    compiler_blend_state_test.py
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
    Unit tests for CompilerBlendState model.
'''

from __future__ import annotations

from unittest import TestCase, main

from scaralang.core.model.dsl.ast.zone_mode import ZoneMode
from scaralang.core.model.dsl.compiler.compiler_blend_state import CompilerBlendState

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.7'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class CompilerBlendStateTest(TestCase):
    '''
        Validates CompilerBlendState default initialization, custom values, and mutation.
    '''

    def test_default_values(self) -> None:
        '''
            Verifies default initialization of blend parameters.
        '''
        blend = CompilerBlendState()
        self.assertEqual(blend.zone_mode, ZoneMode.FINE)
        self.assertEqual(blend.zone_radius, 0.0)

    def test_custom_values(self) -> None:
        '''
            Verifies custom values assignment on instantiation.
        '''
        blend = CompilerBlendState(
            zone_mode=ZoneMode.BLEND,
            zone_radius=10.0,
        )
        self.assertEqual(blend.zone_mode, ZoneMode.BLEND)
        self.assertEqual(blend.zone_radius, 10.0)

    def test_state_mutation(self) -> None:
        '''
            Verifies in-place mutation of blend parameters.
        '''
        blend = CompilerBlendState()
        blend.zone_mode = ZoneMode.BLEND
        blend.zone_radius = 5.0

        self.assertEqual(blend.zone_mode, ZoneMode.BLEND)
        self.assertEqual(blend.zone_radius, 5.0)


if __name__ == '__main__':
    main()
