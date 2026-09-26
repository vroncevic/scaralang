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
    Factory for creating the scaralang bundle.
'''

from __future__ import annotations

from os.path import abspath, dirname, join

from ats_utilities.base.setup.bundle import BaseBundle
from ats_utilities.base.setup.factory import BaseBundleFactory
from ats_utilities.base.setup.options import BaseBundleOptions
from ats_utilities.context.factory import ContextBundleFactory

from scaralang.core.service.dsl.iscara_dsl_service import IScaraDslService
from scaralang.core.service.dsl.scara_dsl_service_factory import ScaraDslServiceFactory
from scaralang.infrastructure.cli.engine import CLI
from scaralang.infrastructure.cli.setup.bundle import CLIBundle
from scaralang.infrastructure.cli.setup.options import CLIBundleOptions
from scaralang.infrastructure.cli.setup.factory import CLIBundleFactory
from scaralang.setup.bundle import ScaralangBundle
from scaralang.setup.options import ScaralangBundleOptions
from scaralang.setup.registry import ScaralangBundleRegistry
from scaralang.setup.dependencies import ScaralangBundleDependencies
from scaralang.setup.opt_validator import ScaralangBundleOptionsValidator
from scaralang.setup.keys import ScaralangBundleKeys

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ScaralangBundleFactory:
    '''
        Factory for creating the scaralang bundle.

        It defines:

            :attributes:
                | _info_file - Path to the scaralang info file.
            :methods:
                | create_bundle - Creates the scaralang bundle with optional configuration options.
                | get_version - Returns the factory version.
    '''

    _info_file: str = join(
        dirname(dirname(abspath(__file__))), 'infrastructure', 'config', 'scaralang.cfg'
    )

    @classmethod
    def create_bundle(cls, options: ScaralangBundleOptions | None = None) -> ScaralangBundle:
        '''
            Creates the scaralang bundle.

            :param options: Optional bundle configuration options.
            :return: The initialized ScaralangBundle.
            :exceptions:
                | ATSValueError: If options fail validation.
                | ATSTypeError:  If options have incorrect types.
        '''
        if options is None:
            options = ScaralangBundleOptions(
                info_file=cls._info_file,
                verbose=False
            )
        else:
            ScaralangBundleOptionsValidator.validate(options)

        info_file: str = (
            options[ScaralangBundleKeys.OPTION_INFO_FILE]
            if ScaralangBundleKeys.OPTION_INFO_FILE in options
            else cls._info_file
        )

        base_bundle: BaseBundle = BaseBundleFactory.create_bundle(
            options=BaseBundleOptions(
                info_file=info_file, use_generator=False, context_bundle=ContextBundleFactory.create_bundle()
            )
        )

        dsl_service: IScaraDslService = ScaraDslServiceFactory.create_default()

        cli_bundle: CLIBundle = CLIBundleFactory.create_bundle(
            options=CLIBundleOptions(service=dsl_service, parser=base_bundle.option_manager)
        )

        cli: CLI = CLI(bundle=cli_bundle)

        return ScaralangBundleRegistry.create_bundle(
            dependencies=ScaralangBundleDependencies(
                base=base_bundle,
                service=dsl_service,
                cli=cli
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
