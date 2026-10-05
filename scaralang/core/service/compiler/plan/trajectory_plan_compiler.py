# -*- coding: UTF-8 -*-

'''
Module
    trajectory_plan_compiler.py
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
    Implementation of ITrajectoryPlanCompiler transforming SCARA DSL programs
    into validated trajectory plans.
'''

from __future__ import annotations

from typing import Final

from scaralang.core.model.dsl.ast.program import ScaraProgram
from scaralang.core.model.exceptions.scara_kinematics_error import ScaraKinematicsError
from scaralang.core.service.compiler.iinstruction_pipeline import IInstructionPipeline
from scaralang.core.service.trajectory.plan.itrajectory_plan import ITrajectoryPlan
from scaralang.core.service.trajectory.plan.itrajectory_plan_factory import ITrajectoryPlanFactory
from scaralang.core.service.trajectory.validation.itrajectory_validator import ITrajectoryValidator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TrajectoryPlanCompiler:
    '''
        Compiler orchestrator coordinating instruction pipeline and kinematic validation.

        It defines:

            :attributes:
                | _validator - Kinematic reachability validator.
                | _plan_factory - Factory producing ITrajectoryPlan instances.
                | _instruction_pipeline - Pipeline compiling AST instructions into Waypoints.
            :methods:
                | __init__ - Initializes compiler with injected collaborators.
                | compile - Compiles Program into validated TrajectoryPlan.
                | get_version - Returns the compiler version string.
    '''

    _validator: ITrajectoryValidator
    _plan_factory: ITrajectoryPlanFactory
    _instruction_pipeline: IInstructionPipeline

    def __init__(
        self,
        *,
        validator: ITrajectoryValidator,
        instruction_pipeline: IInstructionPipeline,
        plan_factory: ITrajectoryPlanFactory,
    ) -> None:
        '''
            Initializes TrajectoryPlanCompiler with injected components.

            :param validator: Injected ITrajectoryValidator instance.
            :param instruction_pipeline: Injected IInstructionPipeline component.
            :param plan_factory: Injected ITrajectoryPlanFactory component.
            :exceptions: None.
        '''
        self._validator: Final[ITrajectoryValidator] = validator
        self._instruction_pipeline: Final[IInstructionPipeline] = instruction_pipeline
        self._plan_factory: Final[ITrajectoryPlanFactory] = plan_factory

    def compile(self, *, program: ScaraProgram) -> ITrajectoryPlan:
        '''
            Compiles a SCARA DSL program into an executable and validated ITrajectoryPlan.

            :param program: Parsed ScaraProgram AST root.
            :return: Validated ITrajectoryPlan instance.
            :exceptions: ScaraKinematicsError if kinematic validation fails.
        '''
        waypoints = self._instruction_pipeline.compile_instructions(
            instructions=program.instructions
        )

        plan = self._plan_factory.create()
        plan.set_waypoints(waypoints)

        is_valid, messages = self._validator.validate_plan(plan=plan)

        if not is_valid:
            err_msg = '; '.join(messages)
            raise ScaraKinematicsError(
                f'Compilation failed kinematic validation: {err_msg}'
            )

        return plan

    def get_version(self) -> str:
        '''
            Returns the compiler version string representation.

            :return: Version string representation.
            :exceptions: None.
        '''
        return __version__
