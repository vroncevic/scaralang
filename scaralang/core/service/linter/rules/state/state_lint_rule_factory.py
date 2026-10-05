# -*- coding: UTF-8 -*-

'''
Module
    state_lint_rule_factory.py
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
    Factory instantiating StateLintRule components.
'''

from __future__ import annotations

from scaralang.core.service.linter.rules.iscara_lint_rule import IScaraLintRule
from scaralang.core.service.linter.rules.state.imotor_mode_validator import IMotorModeValidator
from scaralang.core.service.linter.rules.state.istate_homing_validator import IStateHomingValidator
from scaralang.core.service.linter.rules.state.istate_zone_validator import IStateZoneValidator
from scaralang.core.service.linter.rules.state.motor_mode_validator_factory import MotorModeValidatorFactory
from scaralang.core.service.linter.rules.state.state_homing_validator_factory import StateHomingValidatorFactory
from scaralang.core.service.linter.rules.state.state_zone_validator_factory import StateZoneValidatorFactory
from scaralang.core.service.linter.rules.state.state_lint_rule import StateLintRule

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class StateLintRuleFactory:
    '''
        Factory providing configured StateLintRule instances.

        It defines:

            :methods:
                | create - Creates an instance of StateLintRule with injected validators.
                | create_default - Creates an instance of StateLintRule with default validators.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(
        cls,
        *,
        homing_validator: IStateHomingValidator,
        zone_validator: IStateZoneValidator,
        motor_mode_validator: IMotorModeValidator,
    ) -> IScaraLintRule:
        '''
            Builds and returns an IScaraLintRule instance for state validation.

            :param homing_validator: Required IStateHomingValidator instance.
            :param zone_validator: Required IStateZoneValidator instance.
            :param motor_mode_validator: Required IMotorModeValidator instance.
            :return: Configured IScaraLintRule instance.
            :exceptions: None.
        '''
        return StateLintRule(
            homing_validator=homing_validator,
            zone_validator=zone_validator,
            motor_mode_validator=motor_mode_validator,
        )

    @classmethod
    def create_default(cls) -> IScaraLintRule:
        '''
            Builds and returns an IScaraLintRule instance with default collaborating validators.

            :return: Configured IScaraLintRule instance.
            :exceptions: None.
        '''
        return cls.create(
            homing_validator=StateHomingValidatorFactory.create(),
            zone_validator=StateZoneValidatorFactory.create(),
            motor_mode_validator=MotorModeValidatorFactory.create(),
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory version string.

            :return: Factory version string.
            :exceptions: None.
        '''
        return __version__
