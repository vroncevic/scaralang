# -*- coding: UTF-8 -*-

'''
Module
    scara_linter_factory.py
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
    Factory instantiating and wiring ScaraLinter with static analysis rules.
'''

from __future__ import annotations

from collections.abc import Sequence

from scaralang.core.service.linter.iscara_linter import IScaraLinter
from scaralang.core.service.linter.rules.iscara_lint_rule import IScaraLintRule
from scaralang.core.service.linter.rules.motion.motion_lint_rule_factory import MotionLintRuleFactory
from scaralang.core.service.linter.rules.pneumatic.pneumatic_lint_rule_factory import PneumaticLintRuleFactory
from scaralang.core.service.linter.rules.state.state_lint_rule_factory import StateLintRuleFactory
from scaralang.core.service.linter.rules.timing.timing_lint_rule_factory import TimingLintRuleFactory
from scaralang.core.service.linter.scara_linter import ScaraLinter

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.6'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ScaraLinterFactory:
    '''
        Factory providing wired IScaraLinter instances.

        It defines:

            :methods:
                | create - Builds and wires ScaraLinter with static analysis rules.
                | create_with_rules - Builds ScaraLinter with explicit custom rules.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(cls) -> IScaraLinter:
        '''
            Builds and wires ScaraLinter with default static analysis rules.

            :return: IScaraLinter structural protocol instance.
            :exceptions: None.
        '''
        return ScaraLinter(
            rules=(
                StateLintRuleFactory.create_default(),
                MotionLintRuleFactory.create_default(),
                PneumaticLintRuleFactory.create_default(),
                TimingLintRuleFactory.create_default(),
            )
        )

    @classmethod
    def create_with_rules(cls, *, rules: Sequence[IScaraLintRule]) -> IScaraLinter:
        '''
            Builds ScaraLinter with explicit custom rules.

            :param rules: Explicit sequence of IScaraLintRule components.
            :return: IScaraLinter structural protocol instance.
            :exceptions: None.
        '''
        return ScaraLinter(rules=rules)

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory version string.

            :return: Factory version string.
            :exceptions: None.
        '''
        return __version__
