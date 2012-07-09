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
from sextante.parameters.ParameterBoolean import ParameterBoolean
from sextante.parameters.ParameterSelection import ParameterSelection

from sextante.outputs.OutputRaster import OutputRaster

from sextante_taudem.TauDEMUtils import TauDEMUtils

class DinfDistDown(GeoAlgorithm):
    PROCESS_NUMBER = "PROCESS_NUMBER"
    DINF_FLOW_DIR_GRID = "DINF_FLOW_DIR_GRID"
    PIT_FILLED_GRID = "PIT_FILLED_GRID"
    STREAM_GRID = "STREAM_GRID"
    WEIGHT_PATH_GRID = "WEIGHT_PATH_GRID"
    STAT_METHOD = "STAT_METHOD"
    DIST_METHOD = "DIST_METHOD"
    EDGE_CONTAM = "EDGE_CONTAM"

    DIST_DOWN_GRID = "DIST_DOWN_GRID"

    STATISTICS = ["Minimum", "Maximum", "Average"]
    STAT_DICT = {0:"min",
                 1:"max",
                 2:"ave"}

    DISTANCE = ["Pythagoras", "Horizontal", "Vertical", "Surface"]
    DIST_DICT = {0:"p",
                 1:"h",
                 2:"v",
                 3:"s"}

    def getIcon(self):
        return  QIcon(os.path.dirname(__file__) + "/icons/taudem.png")

    def defineCharacteristics(self):
        self.name = "D-Infinity Distance Down"
        self.cmdName = "dinfdistdown"
        self.group = "Specialized Grid Analysis tools"

        self.addParameter(ParameterNumber(self.PROCESS_NUMBER, "Number of Processes", 1, 99, 2))
        self.addParameter(ParameterRaster(self.DINF_FLOW_DIR_GRID, "D-Infinity Flow Direction Grid", False))
        self.addParameter(ParameterRaster(self.PIT_FILLED_GRID, "Pit Filled Elevation Grid", False))
        self.addParameter(ParameterRaster(self.STREAM_GRID, "Stream Raster Grid", False))
        self.addParameter(ParameterRaster(self.WEIGHT_PATH_GRID, "Weight Path Grid", True))
        self.addParameter(ParameterSelection(self.STAT_METHOD, "Statistical Method", self.STATISTICS, 2))
        self.addParameter(ParameterSelection(self.DIST_METHOD, "Distance Method", self.DISTANCE, 1))
        self.addParameter(ParameterBoolean(self.EDGE_CONTAM, "Check for edge contamination", True))

        self.addOutput(OutputRaster(self.DIST_DOWN_GRID, "D-Infinity Drop to Stream Grid"))

    def processAlgorithm(self, progress):
        commands = []
        commands.append(os.path.join(TauDEMUtils.mpiexecPath(), "mpiexec"))

        commands.append("-n")
        commands.append(str(self.getParameterValue(self.PROCESS_NUMBER)))
        commands.append(os.path.join(TauDEMUtils.taudemPath(), self.cmdName))
        commands.append("-ang")
        commands.append(self.getParameterValue(self.DINF_FLOW_DIR_GRID))
        commands.append("-fel")
        commands.append(self.getParameterValue(self.PIT_FILLED_GRID))
        commands.append("-src")
        commands.append(self.getParameterValue(self.STREAM_GRID))
        wg = self.getParameterValue(self.WEIGHT_PATH_GRID)
        if wg is not None:
          commands.append("-wg")
          commands.append(self.getParameterValue(self.WEIGHT_PATH_GRID))
        commands.append("-m")
        commands.append(str(self.STAT_DICT[self.getParameterValue(self.STAT_METHOD)]))
        commands.append(str(self.DIST_DICT[self.getParameterValue(self.DIST_METHOD)]))
        if str(self.getParameterValue(self.EDGE_CONTAM)).lower() == "false":
            commands.append("-nc")
        commands.append("-dd")
        commands.append(self.getOutputValue(self.DIST_DOWN_GRID))

        loglines = []
        loglines.append("TauDEM execution command")
        for line in commands:
            loglines.append(line)
        SextanteLog.addToLog(SextanteLog.LOG_INFO, loglines)

        TauDEMUtils.executeTauDEM(commands, progress)

    def helpFile(self):
        return os.path.join(os.path.dirname(__file__), "help", self.cmdName + ".html")
