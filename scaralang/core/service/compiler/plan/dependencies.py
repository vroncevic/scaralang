# -*- coding: UTF-8 -*-

'''
Module
    dependencies.py
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
    Defines PlanDependencies dataclass bundle for plan compilation subsystem.
'''

from __future__ import annotations

from dataclasses import dataclass

from scaralang.core.service.linter.ilinter import ILinter
from scaralang.core.service.parser.iparser import IScaraParser
from scaralang.core.service.trajectory.validation.plan.ivalidator import ITrajectoryPlanValidator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(frozen=True, slots=True)
class PlanDependencies:
    '''
        Immutable dependency bundle required by PlanFactory.

        It defines:

            :attributes:
                | validator - Injected kinematic trajectory plan validator protocol.
                | parser - Injected AST parser protocol.
                | linter - Injected static analysis linter protocol.
    '''

    validator: ITrajectoryPlanValidator
    parser: IScaraParser
    linter: ILinter
