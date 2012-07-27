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
from sextante.parameters.ParameterNumber import ParameterNumber

from sextante.outputs.OutputRaster import OutputRaster

from sextante_taudem.TauDEMUtils import TauDEMUtils

class SlopeArea(GeoAlgorithm):
    SLOPE_GRID = "SLOPE_GRID"
    AREA_GRID = "AREA_GRID"
    SLOPE_EXPONENT = "SLOPE_EXPONENT"
    AREA_EXPONENT = "AREA_EXPONENT"

    SLOPE_AREA_GRID = "SLOPE_AREA_GRID"

    def getIcon(self):
        return  QIcon(os.path.dirname(__file__) + "/icons/taudem.png")

    def defineCharacteristics(self):
        self.name = "Slope Area Combination"
        self.cmdName = "slopearea"
        self.group = "Stream Network Analysis tools"

        self.addParameter(ParameterRaster(self.SLOPE_GRID, "Slope Grid", False))
        self.addParameter(ParameterRaster(self.AREA_GRID, "Contributing Area Grid", False))
        self.addParameter(ParameterNumber(self.SLOPE_EXPONENT, "Slope Exponent", 0, None, 2))
        self.addParameter(ParameterNumber(self.AREA_EXPONENT, "Area Exponent", 0, None, 1))

        self.addOutput(OutputRaster(self.SLOPE_AREA_GRID, "Slope Area Grid"))

    def processAlgorithm(self, progress):
        commands = []
        commands.append(os.path.join(TauDEMUtils.mpiexecPath(), "mpiexec"))

        processNum = SextanteConfig.getSetting(TauDEMUtils.MPI_PROCESSES)
        if processNum <= 0:
          raise GeoAlgorithmExecutionException("Wrong number of MPI processes used.\nPlease set correct number before running TauDEM algorithms.")

        commands.append("-n")
        commands.append(str(processNum))
        commands.append(os.path.join(TauDEMUtils.taudemPath(), self.cmdName))
        commands.append("-slp")
        commands.append(self.getParameterValue(self.SLOPE_GRID))
        commands.append("-sca")
        commands.append(self.getParameterValue(self.AREA_GRID))
        commands.append("-par")
        commands.append(str(self.getParameterValue(self.SLOPE_EXPONENT)))
        commands.append(str(self.getParameterValue(self.AREA_EXPONENT)))
        commands.append("-sa")
        commands.append(self.getOutputValue(self.SLOPE_AREA_GRID))

        loglines = []
        loglines.append("TauDEM execution command")
        for line in commands:
            loglines.append(line)
        SextanteLog.addToLog(SextanteLog.LOG_INFO, loglines)

        TauDEMUtils.executeTauDEM(commands, progress)

    def helpFile(self):
        return os.path.join(os.path.dirname(__file__), "help", self.cmdName + ".html")
