# -*- coding: UTF-8 -*-
#
# The MIT License (MIT)
#
# Copyright (c) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

'''
Module
    iscara_info_provider.py
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
    Defines structural protocol IScaraInfoProvider for querying SCARA toolchain metadata.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.7'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IScaraInfoProvider(Protocol):
    '''
        Protocol defining toolchain metadata and instruction catalog provider contract.

        It defines:

            :methods:
                | get_info - Returns formatted toolchain specification lines.
                | get_toolchain_info - Returns formatted toolchain specification lines.
                | get_supported_instructions - Returns list of supported DSL instruction names.
                | build_verbose_lines - Returns detailed kinematic bounds and transmission lines.
                | get_version - Returns the info provider version string representation.
    '''

    def get_info(self, *, verbose: bool = False) -> tuple[str, ...]:
        '''
            Returns toolchain metadata, instruction catalog and protocol specification.

            :param verbose: Whether to include kinematic bounds details.
            :return: Tuple of informative strings.
            :exceptions: None.
        '''

    def get_toolchain_info(self, *, verbose: bool = False) -> tuple[str, ...]:
        '''
            Returns toolchain metadata, instruction catalog and protocol specification.

            :param verbose: Whether to include kinematic bounds details.
            :return: Tuple of informative strings.
            :exceptions: None.
        '''

    def get_supported_instructions(self) -> tuple[str, ...]:
        '''
            Returns list of supported DSL instruction syntax summaries.

            :return: Tuple of supported instruction names and signatures.
            :exceptions: None.
        '''

    def build_verbose_lines(self) -> tuple[str, ...]:
        '''
            Builds detailed kinematic bounds and transmission lines.

            :return: Tuple of formatted verbose specification lines.
            :exceptions: None.
        '''

    def get_version(self) -> str:
        '''
            Returns the info provider version string representation.

            :return: Semantic version string.
        '''
