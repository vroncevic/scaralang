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
    Factory instantiating and wiring kinematics subsystem components.
'''

from __future__ import annotations

from scaralang.core.service.kinematics.dependencies import KinematicsDependencies
from scaralang.core.service.kinematics.envelope.factory import WorkspaceEnvelopeFactory
from scaralang.core.service.kinematics.envelope.ienvelope import IWorkspaceEnvelope
from scaralang.core.service.kinematics.provides import KinematicsProvides
from scaralang.core.service.kinematics.solver.planar.factory import PlanarKinematicsSolverFactory
from scaralang.core.service.kinematics.solver.planar.isolver import IPlanarKinematicsSolver
from scaralang.core.service.kinematics.solver.spatial.factory import SpatialKinematicsSolverFactory
from scaralang.core.service.kinematics.solver.spatial.isolver import ISpatialKinematicsSolver
from scaralang.core.service.kinematics.workspace.factory import WorkspaceFactory
from scaralang.core.service.kinematics.workspace.ievaluator import IWorkspaceBoundsEvaluator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.9'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class KinematicsFactory:
    '''
        Factory instantiating and wiring kinematics subsystem components.

        It defines:

            :methods:
                | create - Builds KinematicsProvides instance with injected dependencies.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(cls, dependencies: KinematicsDependencies) -> KinematicsProvides:
        '''
            Builds KinematicsProvides instance with injected dependencies.

            :param dependencies: Required KinematicsDependencies instance.
            :return: KinematicsProvides output dataclass.
            :exceptions: None.
        '''
        planar: IPlanarKinematicsSolver = PlanarKinematicsSolverFactory.create(
            links=dependencies.bounds.links,
        )
        spatial: ISpatialKinematicsSolver = SpatialKinematicsSolverFactory.create(
            planar=planar,
            vertical=dependencies.bounds.vertical,
        )
        workspace: IWorkspaceBoundsEvaluator = WorkspaceFactory.create(
            bounds=dependencies.bounds,
            planar=planar,
        )
        envelope: IWorkspaceEnvelope = WorkspaceEnvelopeFactory.create(
            bounds=dependencies.bounds,
        )

        return KinematicsProvides(
            envelope=envelope,
            planar=planar,
            spatial=spatial,
            workspace=workspace,
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns factory version string representation.

            :return: Factory version string.
            :exceptions: None.
        '''
        return __version__
