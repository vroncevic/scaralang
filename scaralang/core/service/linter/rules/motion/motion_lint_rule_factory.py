# -*- coding: UTF-8 -*-

'''
Module
    motion_lint_rule_factory.py
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
    Factory instantiating MotionLintRule components.
'''

from __future__ import annotations

from scaralang.core.service.linter.rules.iscara_lint_rule import IScaraLintRule
from scaralang.core.service.linter.rules.motion.imotion_calibration_validator import IMotionCalibrationValidator
from scaralang.core.service.linter.rules.motion.imotion_duplicate_validator import IMotionDuplicateValidator
from scaralang.core.service.linter.rules.motion.motion_calibration_validator_factory import MotionCalibrationValidatorFactory
from scaralang.core.service.linter.rules.motion.motion_duplicate_validator_factory import MotionDuplicateValidatorFactory
from scaralang.core.service.linter.rules.motion.motion_lint_rule import MotionLintRule

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class MotionLintRuleFactory:
    '''
        Factory providing configured MotionLintRule instances.

        It defines:

            :methods:
                | create - Creates an instance of MotionLintRule with injected validators.
                | create_default - Creates an instance of MotionLintRule with default validators.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(
        cls,
        *,
        calibration_validator: IMotionCalibrationValidator,
        duplicate_validator: IMotionDuplicateValidator,
    ) -> IScaraLintRule:
        '''
            Builds and returns an IScaraLintRule instance for motion validation.

            :param calibration_validator: Required IMotionCalibrationValidator instance.
            :param duplicate_validator: Required IMotionDuplicateValidator instance.
            :return: Configured IScaraLintRule instance.
            :exceptions: None.
        '''
        return MotionLintRule(
            calibration_validator=calibration_validator,
            duplicate_validator=duplicate_validator,
        )

    @classmethod
    def create_default(cls) -> IScaraLintRule:
        '''
            Builds and returns an IScaraLintRule instance with default collaborating validators.

            :return: Configured IScaraLintRule instance.
            :exceptions: None.
        '''
        return cls.create(
            calibration_validator=MotionCalibrationValidatorFactory.create(),
            duplicate_validator=MotionDuplicateValidatorFactory.create(),
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory version string.

            :return: Factory version string.
            :exceptions: None.
        '''
        return __version__
