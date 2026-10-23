# -*- coding: UTF-8 -*-

'''
Module
    tool_state_test.py
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
    Unit tests for LintToolState model.
'''

from __future__ import annotations

from unittest import TestCase, main

from scaralang.core.model.dsl.linter.tool_state import LintToolState

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class LintToolStateTest(TestCase):
    '''
        Unit tests validating LintToolState initialization and mutability.

        It defines:

            :methods:
                | test_initialization - Verifies default initialization values.
                | test_custom_values - Verifies custom initialization values.
                | test_mutation - Verifies in-place attribute mutation.
    '''

    def test_initialization(self) -> None:
        '''
            Verify LintToolState initialization values.

            :exceptions: None.
        '''
        state = LintToolState(pump_on=False, valve_on=False)
        self.assertFalse(state.pump_on)
        self.assertFalse(state.valve_on)

    def test_custom_values(self) -> None:
        '''
            Verify LintToolState custom values.

            :exceptions: None.
        '''
        state = LintToolState(pump_on=True, valve_on=False)
        self.assertTrue(state.pump_on)
        self.assertFalse(state.valve_on)

    def test_mutation(self) -> None:
        '''
            Verify that LintToolState attributes can be updated in-place.

            :exceptions: None.
        '''
        state = LintToolState(pump_on=False, valve_on=False)
        state.pump_on = True
        state.valve_on = True
        self.assertTrue(state.pump_on)
        self.assertTrue(state.valve_on)


if __name__ == '__main__':
    main()
