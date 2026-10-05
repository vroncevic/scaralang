# -*- coding: UTF-8 -*-

'''
Module
    svg_trajectory_exporter_factory.py
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
    Factory instantiating SvgTrajectoryExporter instances.
'''

from __future__ import annotations

from scaralang.core.service.exporter.svg.isvg_trajectory_exporter import ISvgTrajectoryExporter
from scaralang.core.service.exporter.svg.svg_trajectory_exporter import SvgTrajectoryExporter

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class SvgTrajectoryExporterFactory:
    '''
        Factory providing ISvgTrajectoryExporter instances.

        It defines:

            :methods:
                | create - Builds SvgTrajectoryExporter instance.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(cls) -> ISvgTrajectoryExporter:
        '''
            Builds and returns an ISvgTrajectoryExporter protocol instance.

            :return: Fully wired ISvgTrajectoryExporter protocol instance.
            :exceptions: None.
        '''
        return SvgTrajectoryExporter()

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory version string.

            :return: Factory version string.
            :exceptions: None.
        '''
        return __version__
