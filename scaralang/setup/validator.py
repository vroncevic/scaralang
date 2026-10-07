# -*- coding: UTF-8 -*-

'''
Module
    validator.py
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
    Validator for the scaralang bundle instance.
'''

from __future__ import annotations

from ats_utilities.base.setup.bundle import BaseBundle
from ats_utilities.exceptions import ATSValueError, ATSTypeError
from ats_utilities.validation.check_value import not_none
from ats_utilities.validation.check_type import istype

from scaralang.setup.bundle import ScaralangBundle
from scaralang.infrastructure.cli.icli import ICLI

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.7'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ScaralangBundleValidator:
    '''
        Validator for the scaralang bundle instance.

        It defines:

            :methods:
                | validate - Validates the scaralang bundle instance.
                | is_valid - Checks if the scaralang bundle instance is valid.
    '''

    @classmethod
    def validate(cls, bundle: ScaralangBundle) -> None:
        '''
            Validates the scaralang bundle instance.

            :param bundle: The scaralang bundle to be validated.
            :exceptions:
                | ATSValueError: The scaralang bundle must be provided and have non-None attributes.
                | ATSTypeError: The scaralang bundle attributes must match required interfaces.
        '''
        ctx: str = 'scaralang_bundle_validator::validate(...)'
        msg_bundle_none: str = 'the scaralang bundle must be provided'
        msg_bundle_istype: str = 'the scaralang bundle must be an instance of ScaralangBundle'
        msg_base_none: str = 'the base bundle must be provided'
        msg_cli_none: str = 'the cli must be provided'
        msg_base_istype: str = 'the base bundle must be an instance of BaseBundle'
        msg_cli_istype: str = 'the cli must be an instance of ICLI'

        not_none(bundle, ctx, msg_bundle_none)
        istype(bundle, ScaralangBundle, ctx, msg_bundle_istype)

        not_none(bundle.base, ctx, msg_base_none)
        not_none(bundle.cli, ctx, msg_cli_none)

        istype(bundle.base, BaseBundle, ctx, msg_base_istype)
        istype(bundle.cli, ICLI, ctx, msg_cli_istype)

    @classmethod
    def is_valid(cls, bundle: ScaralangBundle) -> bool:
        '''
            Checks if the scaralang bundle is valid.

            :param bundle: The scaralang bundle to check.
            :return: True if valid, False otherwise.
            :exceptions: None.
        '''
        try:
            cls.validate(bundle)
            return True

        except (ATSValueError, ATSTypeError):
            return False
