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
    Unit tests for TimingFactory operations.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.service.linter.rules.irule import ILintRule
from scaralang.core.service.linter.rules.timing.blend_zone.ivalidator import IBlendZoneValidator
from scaralang.core.service.linter.rules.timing.dwell.ivalidator import IDwellValidator
from scaralang.core.service.linter.rules.timing.factory import TimingFactory
from scaralang.core.service.linter.rules.timing.provides import TimingProvides

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestTimingFactory(TestCase):
    '''
        Test cases verifying TimingFactory instantiation.

        It defines:

            :methods:
                | test_create_returns_provides - Verifies factory returns TimingProvides.
                | test_get_version - Verifies factory version string.
    '''

    def test_create_returns_provides(self) -> None:
        '''
            Verifies create builds a valid TimingProvides instance with wired components.
        '''
        provides = TimingFactory.create()
        self.assertIsInstance(provides, TimingProvides)
        self.assertIsInstance(provides.rule, ILintRule)
        self.assertIsInstance(provides.dwell_validator, IDwellValidator)
        self.assertIsInstance(provides.blend_zone_validator, IBlendZoneValidator)

    def test_get_version(self) -> None:
        '''
            Verifies factory returns correct version string.
        '''
        self.assertEqual(TimingFactory.get_version(), '1.1.0')


if __name__ == '__main__':
    main()
