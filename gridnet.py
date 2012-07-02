# -*- coding: utf-8 -*-

#******************************************************************************
#
# TauDEM SEXTANTE Provider
# ---------------------------------------------------------
# A suite of Digital Elevation Model (DEM) tools for the extraction and
# analysis of hydrologic information from topography as represented by
# a DEM of vector layer.
#
# Copyright (C) 2012 Alexander Bruy (alexander.bruy@gmail.com)
#
# This source is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 2 of the License, or (at your option)
# any later version.
#
# This code is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# A copy of the GNU General Public License is available on the World Wide Web
# at <http://www.gnu.org/licenses/>. You can also obtain it by writing
# to the Free Software Foundation, 51 Franklin Street, Suite 500 Boston,
# MA 02110-1335 USA.
#
#******************************************************************************

import os

from PyQt4.QtGui import *

from sextante.core.GeoAlgorithm import GeoAlgorithm
from sextante.core.SextanteLog import SextanteLog
from sextante.core.SextanteUtils import SextanteUtils
from sextante.core.SextanteConfig import SextanteConfig
from sextante.core.GeoAlgorithmExecutionException import GeoAlgorithmExecutionException

from sextante.parameters.ParameterRaster import ParameterRaster
from sextante.parameters.ParameterVector import ParameterVector
from sextante.parameters.ParameterNumber import ParameterNumber

from sextante.outputs.OutputRaster import OutputRaster

from sextante_taudem.TauDEMUtils import TauDEMUtils

class GridNet(GeoAlgorithm):
    PROCESS_NUMBER = "PROCESS_NUMBER"
    D8_FLOW_DIR_GRID = "D8_FLOW_DIR_GRID"
    OUTLETS_SHAPE = "OUTLETS_SHAPE"
    MASK_GRID = "MASK_GRID"
    THRESHOLD = "THRESHOLD"

    LONGEST_LEN_GRID = "LONGEST_LEN_GRID"
    TOTAL_LEN_GRID = "TOTAL_LEN_GRID"
    STRAHLER_GRID = "STRAHLER_GRID"

    def getIcon(self):
        return  QIcon(os.path.dirname(__file__) + "/icons/taudem.png")

    def defineCharacteristics(self):
        self.name = "Grid Network"
        self.cmdName = "gridnet"
        self.group = "Basic Grid Analysis tools"

        self.addParameter(ParameterNumber(self.PROCESS_NUMBER, "Number of Processes", 1, 99, 2))
        self.addParameter(ParameterRaster(self.D8_FLOW_DIR_GRID, "D8 Flow Direction Grid", False))
        self.addParameter(ParameterVector(self.OUTLETS_SHAPE, "Outlets Shapefile", ParameterVector.VECTOR_TYPE_POINT, True))
        self.addParameter(ParameterRaster(self.MASK_GRID, "Mask Grid", True))
        self.addParameter(ParameterNumber(self.THRESHOLD, "Proportion Threshold", 0, None, 100))

        self.addOutput(OutputRaster(self.LONGEST_LEN_GRID, "Longest Upslope Length Grid"))
        self.addOutput(OutputRaster(self.TOTAL_LEN_GRID, "Total Upslope Length Grid"))
        self.addOutput(OutputRaster(self.STRAHLER_GRID, "Strahler Network Order Grid"))

    def processAlgorithm(self, progress):
        commands = []
        commands.append(os.path.join(TauDEMUtils.mpiexecPath(), "mpiexec"))

        commands.append("-n")
        commands.append(str(self.getParameterValue(self.PROCESS_NUMBER)))
        commands.append(os.path.join(TauDEMUtils.taudemPath(), self.cmdName))
        commands.append("-p")
        commands.append(self.getParameterValue(self.D8_FLOW_DIR_GRID))
        param = self.getParameterValue(self.OUTLETS_SHAPE)
        if param is not None:
          commands.append("-o")
          commands.append(param)
        param = self.getParameterValue(self.MASK_GRID)
        if param is not None:
          commands.append("-mask")
          commands.append(param)
          commands.append("-thresh")
          commands.append(self.getParameterValue(self.THRESHOLD))

        commands.append("-plen")
        commands.append(self.getOutputValue(self.LONGEST_LEN_GRID))
        commands.append("-tlen")
        commands.append(self.getOutputValue(self.TOTAL_LEN_GRID))
        commands.append("-gord")
        commands.append(self.getOutputValue(self.STRAHLER_GRID))

        loglines = []
        loglines.append("TauDEM execution command")
        for line in commands:
            loglines.append(line)
        SextanteLog.addToLog(SextanteLog.LOG_INFO, loglines)

        TauDEMUtils.executeTauDEM(commands, progress)
