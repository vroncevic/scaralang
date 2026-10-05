# -*- coding: UTF-8 -*-

'''
Module
    trajectory_plan_compiler_factory_test.py
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
    Unit tests for TrajectoryPlanCompilerFactory.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main
from unittest.mock import MagicMock

from scaralang.core.service.compiler.plan.itrajectory_plan_compiler import ITrajectoryPlanCompiler
from scaralang.core.service.compiler.plan.trajectory_plan_compiler_factory import TrajectoryPlanCompilerFactory
from scaralang.core.service.kinematics.default_scara_profile import DefaultScaraProfile
from scaralang.core.service.kinematics.kinematics_service_factory import KinematicsServiceFactory
from scaralang.core.service.trajectory.validation.trajectory_validator_factory import TrajectoryValidatorFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.5'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestTrajectoryPlanCompilerFactory(TestCase):
    '''
        Test cases verifying TrajectoryPlanCompilerFactory.

        It defines:

            :methods:
                | setUp - Prepares validator fixture.
                | test_create - Verifies factory returns ITrajectoryPlanCompiler.
                | test_create_with_collaborators - Verifies creation with collaborators.
                | test_get_version - Verifies factory version string.
    '''

    def setUp(self) -> None:
        '''
            Sets up validator fixture.
        '''
        bounds = DefaultScaraProfile.create_bounds()
        kinematics = KinematicsServiceFactory.create(bounds=bounds)
        self.validator = TrajectoryValidatorFactory.create(kinematics=kinematics)

    def test_create(self) -> None:
        '''
            Verifies factory produces ITrajectoryPlanCompiler instance.
        '''
        compiler: ITrajectoryPlanCompiler = TrajectoryPlanCompilerFactory.create(
            validator=self.validator
        )
        self.assertIsInstance(compiler, ITrajectoryPlanCompiler)

    def test_create_with_collaborators(self) -> None:
        '''
            Verifies factory produces ITrajectoryPlanCompiler with injected collaborators.
        '''
        mock_pipeline = MagicMock()
        mock_plan_factory = MagicMock()
        compiler: ITrajectoryPlanCompiler = (
            TrajectoryPlanCompilerFactory.create_with_collaborators(
                validator=self.validator,
                instruction_pipeline=mock_pipeline,
                plan_factory=mock_plan_factory,
            )
        )
        self.assertIsInstance(compiler, ITrajectoryPlanCompiler)

    def test_get_version(self) -> None:
        '''
            Verifies factory version string is non-empty.
        '''
        version: str = TrajectoryPlanCompilerFactory.get_version()
        self.assertTrue(bool(version))


if __name__ == '__main__':
    main()
