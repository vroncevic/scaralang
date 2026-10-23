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
    Factory providing default full-stack ScriptValidator composition.
'''

from __future__ import annotations

from scaralang.core.service.compiler.plan.ast.factory import AstPlanCompilerFactory
from scaralang.core.service.linter.factory import LinterFactory
from scaralang.core.service.linter.validator.dependencies import ValidatorDependencies
from scaralang.core.service.linter.validator.factory import ValidatorFactory
from scaralang.core.service.linter.validator.provides import ValidatorProvides
from scaralang.infrastructure.parser.factory import DefaultParserFactory
from scaralang.infrastructure.trajectory.validation.factory import DefaultValidationFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DefaultScriptValidatorFactory:
    '''
        Factory providing default ScriptValidator composition.

        It defines:

            :methods:
                | create - Builds and returns default ValidatorProvides instance.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(cls) -> ValidatorProvides:
        '''
            Builds and returns default ValidatorProvides instance.

            :return: Fully configured ValidatorProvides instance.
            :exceptions: None.
        '''
        validation = DefaultValidationFactory.create()
        parser = DefaultParserFactory.create().parser
        compiler = AstPlanCompilerFactory.create(validator=validation.plan)
        linter = LinterFactory.create().linter
        return ValidatorFactory.create(
            dependencies=ValidatorDependencies(
                parser=parser,
                linter=linter,
                compiler=compiler,
            )
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory version string.

            :return: Factory version string.
            :exceptions: None.
        '''
        return __version__
