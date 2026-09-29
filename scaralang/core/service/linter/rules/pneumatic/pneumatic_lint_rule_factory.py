# -*- coding: UTF-8 -*-

'''
Module
    pneumatic_lint_rule_factory.py
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
    Factory instantiating PneumaticLintRule components.
'''

from __future__ import annotations

from scaralang.core.service.linter.rules.iscara_lint_rule import IScaraLintRule
from scaralang.core.service.linter.rules.pneumatic.ipneumatic_conflict_validator import IPneumaticConflictValidator
from scaralang.core.service.linter.rules.pneumatic.ipneumatic_flyby_validator import IPneumaticFlybyValidator
from scaralang.core.service.linter.rules.pneumatic.ipneumatic_redundancy_validator import IPneumaticRedundancyValidator
from scaralang.core.service.linter.rules.pneumatic.pneumatic_conflict_validator_factory import PneumaticConflictValidatorFactory
from scaralang.core.service.linter.rules.pneumatic.pneumatic_flyby_validator_factory import PneumaticFlybyValidatorFactory
from scaralang.core.service.linter.rules.pneumatic.pneumatic_redundancy_validator_factory import PneumaticRedundancyValidatorFactory
from scaralang.core.service.linter.rules.pneumatic.pneumatic_lint_rule import PneumaticLintRule

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class PneumaticLintRuleFactory:
    '''
        Factory providing configured PneumaticLintRule instances.

        It defines:

            :methods:
                | create - Creates an instance of PneumaticLintRule with injected validators.
                | create_default - Creates an instance of PneumaticLintRule with default validators.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(
        cls,
        *,
        flyby_validator: IPneumaticFlybyValidator,
        redundancy_validator: IPneumaticRedundancyValidator,
        conflict_validator: IPneumaticConflictValidator,
    ) -> IScaraLintRule:
        '''
            Builds and returns an IScaraLintRule instance for pneumatic validation.

            :param flyby_validator: Required IPneumaticFlybyValidator instance.
            :param redundancy_validator: Required IPneumaticRedundancyValidator instance.
            :param conflict_validator: Required IPneumaticConflictValidator instance.
            :return: Configured IScaraLintRule instance.
            :exceptions: None.
        '''
        return PneumaticLintRule(
            flyby_validator=flyby_validator,
            redundancy_validator=redundancy_validator,
            conflict_validator=conflict_validator,
        )

    @classmethod
    def create_default(cls) -> IScaraLintRule:
        '''
            Builds and returns an IScaraLintRule instance with default collaborating validators.

            :return: Configured IScaraLintRule instance.
            :exceptions: None.
        '''
        return cls.create(
            flyby_validator=PneumaticFlybyValidatorFactory.create(),
            redundancy_validator=PneumaticRedundancyValidatorFactory.create(),
            conflict_validator=PneumaticConflictValidatorFactory.create(),
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory version string.

            :return: Factory version string.
            :exceptions: None.
        '''
        return __version__
