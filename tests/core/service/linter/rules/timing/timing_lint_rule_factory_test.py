# -*- coding: UTF-8 -*-

'''
Module
    timing_lint_rule_factory_test.py
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
    Unit tests for TimingLintRuleFactory operations.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.service.linter.rules.iscara_lint_rule import IScaraLintRule
from scaralang.core.service.linter.rules.timing.timing_blend_zone_validator_factory import TimingBlendZoneValidatorFactory
from scaralang.core.service.linter.rules.timing.timing_dwell_validator_factory import TimingDwellValidatorFactory
from scaralang.core.service.linter.rules.timing.timing_lint_rule_factory import TimingLintRuleFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestTimingLintRuleFactory(TestCase):
    '''
        Test cases verifying TimingLintRuleFactory instantiation.

        It defines:

            :methods:
                | test_create_returns_instance - Verifies factory returns IScaraLintRule with injected validators.
                | test_create_default_returns_instance - Verifies factory returns IScaraLintRule with defaults.
                | test_get_version - Verifies factory version string.
    '''

    def test_create_returns_instance(self) -> None:
        '''
            Verifies create builds a valid IScaraLintRule instance with injected validators.
        '''
        rule = TimingLintRuleFactory.create(
            dwell_validator=TimingDwellValidatorFactory.create(),
            blend_zone_validator=TimingBlendZoneValidatorFactory.create(),
        )
        self.assertIsInstance(rule, IScaraLintRule)

    def test_create_default_returns_instance(self) -> None:
        '''
            Verifies create_default builds a valid IScaraLintRule instance with default validators.
        '''
        rule = TimingLintRuleFactory.create_default()
        self.assertIsInstance(rule, IScaraLintRule)

    def test_get_version(self) -> None:
        '''
            Verifies factory returns correct version string.
        '''
        self.assertEqual(TimingLintRuleFactory.get_version(), '1.0.3')


if __name__ == '__main__':
    main()
