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
    Factory for creating the CLI bundle with commands.
'''

from __future__ import annotations

from scaralang.infrastructure.cli.setup.bundle import CLIBundle
from scaralang.infrastructure.cli.setup.dependencies import CLIBundleDependencies
from scaralang.infrastructure.cli.setup.keys import CLIBundleKeys
from scaralang.infrastructure.cli.setup.opt_validator import CLIBundleOptionsValidator
from scaralang.infrastructure.cli.setup.options import CLIBundleOptions
from scaralang.infrastructure.cli.setup.registry import CLIBundleRegistry
from scaralang.infrastructure.command.command_bundle_factory import CommandBundleFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class CLIBundleFactory:
    '''
        Factory for creating the CLI bundle.

        It defines:

            :methods:
                | create_bundle - Creates the CLI bundle with registered commands.
                | get_version - Returns the factory version.
    '''

    @classmethod
    def create_bundle(cls, options: CLIBundleOptions) -> CLIBundle:
        '''
            Creates the CLI bundle with registered commands.

            :param options: The CLI bundle options.
            :return: The CLI bundle.
            :exceptions:
                | ATSValueError: If options fail validation.
                | ATSTypeError:  If options have incorrect types.
        '''
        CLIBundleOptionsValidator.validate(options)
        service = options[CLIBundleKeys.OPTION_SERVICE]
        commands = CommandBundleFactory.create_commands(service=service)

        return CLIBundleRegistry.create_bundle(
            dependencies=CLIBundleDependencies(
                service=service,
                parser=options[CLIBundleKeys.OPTION_PARSER],
                commands=commands
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
