# -*- coding: UTF-8 -*-

'''
Module
    timing_lint_rule_factory.py
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
    Factory instantiating TimingLintRule components.
'''

from __future__ import annotations

from scaralang.core.service.linter.rules.iscara_lint_rule import IScaraLintRule
from scaralang.core.service.linter.rules.timing.itiming_blend_zone_validator import ITimingBlendZoneValidator
from scaralang.core.service.linter.rules.timing.itiming_dwell_validator import ITimingDwellValidator
from scaralang.core.service.linter.rules.timing.timing_blend_zone_validator_factory import TimingBlendZoneValidatorFactory
from scaralang.core.service.linter.rules.timing.timing_dwell_validator_factory import TimingDwellValidatorFactory
from scaralang.core.service.linter.rules.timing.timing_lint_rule import TimingLintRule

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TimingLintRuleFactory:
    '''
        Factory providing configured TimingLintRule instances.

        It defines:

            :methods:
                | create - Creates an instance of TimingLintRule with injected validators.
                | create_default - Creates an instance of TimingLintRule with default validators.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(
        cls,
        *,
        dwell_validator: ITimingDwellValidator,
        blend_zone_validator: ITimingBlendZoneValidator,
    ) -> IScaraLintRule:
        '''
            Builds and returns an IScaraLintRule instance for timing validation.

            :param dwell_validator: Required ITimingDwellValidator instance.
            :param blend_zone_validator: Required ITimingBlendZoneValidator instance.
            :return: Configured IScaraLintRule instance.
            :exceptions: None.
        '''
        return TimingLintRule(
            dwell_validator=dwell_validator,
            blend_zone_validator=blend_zone_validator,
        )

    @classmethod
    def create_default(cls) -> IScaraLintRule:
        '''
            Builds and returns an IScaraLintRule instance with default collaborating validators.

            :return: Configured IScaraLintRule instance.
            :exceptions: None.
        '''
        return cls.create(
            dwell_validator=TimingDwellValidatorFactory.create(),
            blend_zone_validator=TimingBlendZoneValidatorFactory.create(),
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory version string.

            :return: Factory version string.
            :exceptions: None.
        '''
        return __version__
