# -*- coding: UTF-8 -*-

'''
Module
    factory.py
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
    Factory instantiating and wiring AstPlanCompiler with validators and instruction pipeline.
'''

from __future__ import annotations

from scaralang.core.service.compiler.instruction.dependencies import InstructionDependencies
from scaralang.core.service.compiler.instruction.factory import InstructionFactory
from scaralang.core.service.compiler.instruction.provides import InstructionProvides
from scaralang.core.service.compiler.macro.dependencies import MacroDependencies
from scaralang.core.service.compiler.macro.factory import MacroFactory
from scaralang.core.service.compiler.macro.provides import MacroProvides
from scaralang.core.service.compiler.plan.ast.compiler import AstPlanCompiler
from scaralang.core.service.compiler.plan.ast.icompiler import IAstPlanCompiler
from scaralang.core.service.compiler.primitive.factory import PrimitiveFactory
from scaralang.core.service.compiler.primitive.provides import PrimitiveProvides
from scaralang.core.service.trajectory.validation.plan.ivalidator import ITrajectoryPlanValidator
from scaralang.core.service.transformation.factory import TransformationFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.9'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class AstPlanCompilerFactory:
    '''
        Factory providing wired IAstPlanCompiler instances.

        It defines:

            :methods:
                | create - Builds and wires AstPlanCompiler with collaborators.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(
        cls,
        *,
        validator: ITrajectoryPlanValidator,
    ) -> IAstPlanCompiler:
        '''
            Builds and wires AstPlanCompiler with internal collaborators.

            :param validator: Injected ITrajectoryPlanValidator instance.
            :return: IAstPlanCompiler structural protocol instance.
            :exceptions: None.
        '''
        macro_provides: MacroProvides = MacroFactory.create(
            dependencies=MacroDependencies(
                frame_transformer=TransformationFactory.create().transformer
            )
        )
        primitive_provides: PrimitiveProvides = PrimitiveFactory.create()

        instruction_provides: InstructionProvides = InstructionFactory.create(
            dependencies=InstructionDependencies(
                macro_expanders=macro_provides.expanders,
                primitive_compilers=primitive_provides.compilers,
            )
        )

        return AstPlanCompiler(
            validator=validator,
            instruction_pipeline=instruction_provides.pipeline,
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory version string.

            :return: Factory version string.
            :exceptions: None.
        '''
        return __version__
