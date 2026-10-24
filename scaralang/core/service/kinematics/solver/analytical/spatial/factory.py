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
    Factory constructing SpatialKinematicsSolver instances.
'''

from __future__ import annotations

from scaralang.core.model.kinematics.profile.vertical import VerticalBounds
from scaralang.core.service.kinematics.solver.analytical.planar.isolver import IPlanarKinematicsSolver
from scaralang.core.service.kinematics.solver.analytical.spatial.pose.factory import SpatialPoseKinematicsSolverFactory
from scaralang.core.service.kinematics.solver.analytical.spatial.pose.isolver import ISpatialPoseKinematicsSolver
from scaralang.core.service.kinematics.solver.analytical.spatial.solver import SpatialKinematicsSolver

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class SpatialKinematicsSolverFactory:
    '''
        Factory providing configured SpatialKinematicsSolver instances.

        It defines:

            :methods:
                | create - Builds a SpatialKinematicsSolver from planar solver and vertical limits.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(
        cls,
        planar: IPlanarKinematicsSolver,
        vertical: VerticalBounds,
        pose_solver: ISpatialPoseKinematicsSolver | None = None,
    ) -> SpatialKinematicsSolver:
        '''
            Builds a SpatialKinematicsSolver with injected planar solver and vertical limits.

            :param planar: Required IPlanarKinematicsSolver collaborator instance.
            :param vertical: Required VerticalBounds model instance.
            :param pose_solver: Optional ISpatialPoseKinematicsSolver collaborator instance.
            :return: Configured SpatialKinematicsSolver instance.
            :exceptions: None.
        '''
        resolved_pose: ISpatialPoseKinematicsSolver
        if pose_solver is None:
            resolved_pose = SpatialPoseKinematicsSolverFactory.create(
                planar=planar,
                vertical=vertical,
            )
        else:
            resolved_pose = pose_solver

        return SpatialKinematicsSolver(
            planar=planar,
            vertical=vertical,
            pose_solver=resolved_pose,
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns factory version string representation.

            :return: Factory version string.
            :exceptions: None.
        '''
        return __version__
