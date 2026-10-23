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
    Factory instantiating and providing IScaraPlanExporter instances.
'''

from __future__ import annotations

from scaralang.core.service.exporter.scara.exporter import ScaraPlanExporter
from scaralang.core.service.exporter.scara.formatter.factory import ScaraWaypointFormatterFactory
from scaralang.core.service.exporter.scara.formatter.iformatter import IScaraWaypointFormatter
from scaralang.core.service.exporter.scara.iexporter import IScaraPlanExporter

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ScaraPlanExporterFactory:
    '''
        Factory providing IScaraPlanExporter instances.

        It defines:

            :methods:
                | create - Returns a new IScaraPlanExporter instance.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(cls) -> IScaraPlanExporter:
        '''
            Builds and returns an IScaraPlanExporter instance.

            :return: IScaraPlanExporter structural protocol instance.
            :exceptions: None.
        '''
        formatter: IScaraWaypointFormatter = (
            ScaraWaypointFormatterFactory.create()
        )
        return ScaraPlanExporter(formatter=formatter)

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory version string.

            :return: Factory version string.
            :exceptions: None.
        '''
        return __version__
