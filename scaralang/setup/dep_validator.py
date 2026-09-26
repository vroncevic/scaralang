# -*- coding: UTF-8 -*-

'''
Module
    dep_validator.py
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
    Validator for the scaralang bundle dependencies.
'''

from __future__ import annotations

from collections.abc import Mapping

from ats_utilities.exceptions import ATSValueError, ATSTypeError
from ats_utilities.validation.check_type import istype
from ats_utilities.validation.check_value import not_none

from scaralang.setup.dependencies import ScaralangBundleDependencies
from scaralang.setup.keys import ScaralangBundleKeys

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ScaralangBundleDependenciesValidator:
    '''
        Validator for the scaralang bundle dependencies.

        It defines:

            :methods:
                | validate - Validates the scaralang bundle dependencies.
                | is_valid - Checks if the scaralang bundle dependencies are valid.
    '''

    @classmethod
    def validate(cls, dependencies: ScaralangBundleDependencies) -> None:
        '''
            Validates the scaralang bundle dependencies.

            :param dependencies: The scaralang bundle dependencies to be validated.
            :exceptions:
                | ATSValueError: The dependencies must be provided.
                | ATSTypeError: The dependencies must be a Mapping and match expected types.
        '''
        ctx: str = 'scaralang_bundle_dependencies_validator::validate(...)'
        msg_deps_none: str = 'the scaralang bundle dependencies must be provided'
        msg_deps_istype: str = 'the scaralang bundle dependencies must be a Mapping'

        not_none(dependencies, ctx, msg_deps_none)
        istype(dependencies, Mapping, ctx, msg_deps_istype)

        for attr_name, expected_type in ScaralangBundleKeys.get_dependency_to_type().items():
            msg_attr_none: str = f'the {attr_name.replace("_", " ")} must be provided'
            msg_attr_istype: str = f'the {attr_name.replace("_", " ")} must be an instance of {expected_type.__name__}'

            attribute = dependencies.get(attr_name)

            not_none(attribute, ctx, msg_attr_none)
            istype(attribute, expected_type, ctx, msg_attr_istype)

    @classmethod
    def is_valid(cls, dependencies: ScaralangBundleDependencies) -> bool:
        '''
            Checks if the scaralang bundle dependencies are valid.

            :param dependencies: The scaralang bundle dependencies to check.
            :return: True if valid, False otherwise.
            :exceptions: None.
        '''
        try:
            cls.validate(dependencies)
            return True

        except (ATSValueError, ATSTypeError):
            return False
