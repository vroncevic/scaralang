# -*- coding: UTF-8 -*-

'''
Module
    iscara_lint_rule_test.py
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
    Unit tests for IScaraLintRule protocol compliance.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.service.linter.rules.iscara_lint_rule import IScaraLintRule
from scaralang.core.service.linter.rules.motion.motion_lint_rule_factory import MotionLintRuleFactory
from scaralang.core.service.linter.rules.pneumatic.pneumatic_lint_rule_factory import PneumaticLintRuleFactory
from scaralang.core.service.linter.rules.state.state_lint_rule_factory import StateLintRuleFactory
from scaralang.core.service.linter.rules.timing.timing_lint_rule_factory import TimingLintRuleFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestIScaraLintRule(TestCase):
    '''
        Test cases verifying IScaraLintRule structural subtyping across all rule implementations.

        It defines:

            :methods:
                | test_rules_satisfy_protocol - Verifies all 4 concrete rules implement IScaraLintRule.
                | test_rule_names - Verifies rule names for all concrete rules.
    '''

    def test_rules_satisfy_protocol(self) -> None:
        '''
            Verifies MotionLintRule, StateLintRule, PneumaticLintRule, and TimingLintRule satisfy protocol.
        '''
        self.assertIsInstance(MotionLintRuleFactory.create_default(), IScaraLintRule)
        self.assertIsInstance(StateLintRuleFactory.create_default(), IScaraLintRule)
        self.assertIsInstance(PneumaticLintRuleFactory.create_default(), IScaraLintRule)
        self.assertIsInstance(TimingLintRuleFactory.create_default(), IScaraLintRule)

    def test_rule_names(self) -> None:
        '''
            Verifies name properties for all concrete rules.
        '''
        self.assertEqual(MotionLintRuleFactory.create_default().name, 'motion')
        self.assertEqual(StateLintRuleFactory.create_default().name, 'state')
        self.assertEqual(PneumaticLintRuleFactory.create_default().name, 'pneumatic')
        self.assertEqual(TimingLintRuleFactory.create_default().name, 'timing')


if __name__ == '__main__':
    main()
