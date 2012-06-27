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

class LengthArea(GeoAlgorithm):
    PROCESS_NUMBER = "PROCESS_NUMBER"
    LENGTH_GRID = "LENGTH_GRID"
    CONTRIB_AREA_GRID = "CONTRIB_AREA_GRID"
    THRESHOLD = "THRESHOLD"
    EXPONENT = "EXPONENT"

    STREAM_SOURCE_GRID = "STREAM_SOURCE_GRID"

    def getIcon(self):
        return  QIcon(os.path.dirname(__file__) + "/icons/taudem.png")

    def defineCharacteristics(self):
        self.name = "Length Area Stream Source"
        self.cmdName = "lengtharea"
        self.group = "Stream Network Analysis tools"

        self.addParameter(ParameterNumber(self.PROCESS_NUMBER, "Number of Processes", 1, 99, 2))
        self.addParameter(ParameterRaster(self.LENGTH_GRID, "Length Grid", False))
        self.addParameter(ParameterRaster(self.CONTRIB_AREA_GRID, "Contributing Area Grid", False))
        self.addParameter(ParameterNumber(self.THRESHOLD, "Threshold", 0, None, 0.03))
        self.addParameter(ParameterNumber(self.EXPONENT, "Exponent", 0, None, 1.3))

        self.addOutput(OutputRaster(self.STREAM_SOURCE_GRID, "Stream Source Grid"))

    def processAlgorithm(self, progress):
        path = TauDEMUtils.taudemPath()
        if path == "":
            raise GeoAlgorithmExecutionException("TauDEM folder is not configured.\nPlease configure it before running TauDEM algorithms.")

        commands = []
        commands.append("mpiexec")
        commands.append("-n")
        commands.append(str(self.getParameterValue(self.PROCESS_NUMBER)))
        commands.append(path + os.sep + self.cmdName)
        commands.append("-plen")
        commands.append(self.getParameterValue(self.LENGTH_GRID))
        commands.append("-ad8")
        commands.append(self.getParameterValue(self.CONTRIB_AREA_GRID))
        commands.append("-par")
        commands.append(str(self.getParameterValue(self.THRESHOLD)))
        commands.append(str(self.getParameterValue(self.EXPONENT)))
        commands.append("-ss")
        commands.append(self.getOutputValue(self.STREAM_SOURCE_GRID))

        loglines = []
        loglines.append("TauDEM execution command")
        for line in commands:
            loglines.append(line)
        SextanteLog.addToLog(SextanteLog.LOG_INFO, loglines)

        TauDEMUtils.executeTauDEM(commands, progress)

    def helpFile(self):
        return os.path.join(os.path.dirname(__file__), "help", self.cmdName + ".html")
