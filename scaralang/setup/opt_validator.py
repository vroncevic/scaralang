# -*- coding: UTF-8 -*-

'''
Module
    opt_validator.py
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
    Validator for the scaralang bundle options.
'''

from __future__ import annotations

from collections.abc import Mapping

from ats_utilities.exceptions import ATSValueError, ATSTypeError
from ats_utilities.validation.check_type import istype
from ats_utilities.validation.check_value import not_none

from scaralang.setup.options import ScaralangBundleOptions
from scaralang.setup.keys import ScaralangBundleKeys

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ScaralangBundleOptionsValidator:
    '''
        Validator for the scaralang bundle options.

        It defines:

            :methods:
                | validate - Validates the scaralang bundle options.
                | is_valid - Checks if the scaralang bundle options are valid.
    '''

    @classmethod
    def validate(cls, options: ScaralangBundleOptions) -> None:
        '''
            Validates the scaralang bundle options.

            :param options: The scaralang bundle options to be validated.
            :exceptions:
                | ATSValueError: The scaralang bundle options must be provided.
                | ATSTypeError: The options must be a Mapping and match expected types.
        '''
        ctx: str = 'scaralang_bundle_options_validator::validate(...)'
        msg_opts_none: str = 'the scaralang bundle options must be provided'
        msg_opts_istype: str = 'the scaralang bundle options must be a Mapping'

        not_none(options, ctx, msg_opts_none)
        istype(options, Mapping, ctx, msg_opts_istype)

        for attr_name, expected_type in ScaralangBundleKeys.get_option_to_type().items():
            if attr_name in options:
                msg_attr_istype: str = f'the {attr_name.replace("_", " ")} must be an instance of {expected_type.__name__}'
                istype(options[attr_name], expected_type, ctx, msg_attr_istype)

    @classmethod
    def is_valid(cls, options: ScaralangBundleOptions) -> bool:
        '''
            Checks if the scaralang bundle options are valid.

            :param options: The scaralang bundle options to check.
            :return: True if valid, False otherwise.
            :exceptions: None.
        '''
        try:
            cls.validate(options)
            return True

        except (ATSValueError, ATSTypeError):
            return False
