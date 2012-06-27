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
from sextante.parameters.ParameterVector import ParameterVector
from sextante.parameters.ParameterBoolean import ParameterBoolean

from sextante.outputs.OutputRaster import OutputRaster

from sextante_taudem.TauDEMUtils import TauDEMUtils

class DinfTransLimAccum(GeoAlgorithm):
    PROCESS_NUMBER = "PROCESS_NUMBER"
    DINF_FLOW_DIR_GRID = "DINF_FLOW_DIR_GRID"
    SUPPLY_GRID = "SUPPLY_GRID"
    CAPACITY_GRID = "CAPACITY_GRID"
    IN_CONCENTR_GRID = "IN_CONCENTR_GRID"
    OUTLETS_SHAPE = "OUTLETS_SHAPE"
    EDGE_CONTAM = "EDGE_CONTAM"

    TRANSP_LIM_ACCUM_GRID = "TRANSP_LIM_ACCUM_GRID"
    DEPOSITION_GRID = "DEPOSITION_GRID"
    OUT_CONCENTR_GRID = "OUT_CONCENTR_GRID"

    def getIcon(self):
        return  QIcon(os.path.dirname(__file__) + "/icons/taudem.png")

    def defineCharacteristics(self):
        self.name = "D-Infinity Transport Limited Accumulation"
        self.cmdName = "dinftranslimaccum"
        self.group = "Specialized Grid Analysis tools"

        self.addParameter(ParameterNumber(self.PROCESS_NUMBER, "Number of Processes", 1, 99, 2))

        self.addParameter(ParameterRaster(self.DINF_FLOW_DIR_GRID, "D-Infinity Flow Direction Grid", False))
        self.addParameter(ParameterRaster(self.SUPPLY_GRID, "Supply Grid", False))
        self.addParameter(ParameterRaster(self.CAPACITY_GRID, "Transport Capacity Grid", False))
        self.addParameter(ParameterVector(self.OUTLETS_SHAPE, "Outlets Shapefile", ParameterVector.VECTOR_TYPE_POINT, True))
        self.addParameter(ParameterBoolean(self.EDGE_CONTAM, "Check for edge contamination", True))

        self.addOutput(OutputRaster(self.TRANSP_LIM_ACCUM_GRID, "Transport Limited Accumulation Grid"))
        self.addOutput(OutputRaster(self.DEPOSITION_GRID, "Deposition Grid"))

    def processAlgorithm(self, progress):
        path = TauDEMUtils.taudemPath()
        if path == "":
            raise GeoAlgorithmExecutionException("TauDEM folder is not configured.\nPlease configure it before running TauDEM algorithms.")

        commands = []
        commands.append("mpiexec")
        commands.append("-n")
        commands.append(str(self.getParameterValue(self.PROCESS_NUMBER)))
        commands.append(path + os.sep + self.cmdName)

        commands.append("-ang")
        commands.append(self.getParameterValue(self.DINF_FLOW_DIR_GRID))
        commands.append("-tsup")
        commands.append(self.getParameterValue(self.SUPPLY_GRID))
        commands.append("-tc")
        commands.append(self.getParameterValue(self.CAPACITY_GRID))
        param = self.getParameterValue(self.OUTLETS_SHAPE)
        if param is not None:
          commands.append("-o")
          commands.append(param)
        if str(self.getParameterValue(self.EDGE_CONTAM)).lower() == "false":
            commands.append("-nc")

        commands.append("-tla")
        commands.append(self.getOutputValue(self.TRANSP_LIM_ACCUM_GRID))
        commands.append("-tdep")
        commands.append(self.getOutputValue(self.DEPOSITION_GRID))

        loglines = []
        loglines.append("TauDEM execution command")
        for line in commands:
            loglines.append(line)
        SextanteLog.addToLog(SextanteLog.LOG_INFO, loglines)

        TauDEMUtils.executeTauDEM(commands, progress)

    def helpFile(self):
        return os.path.join(os.path.dirname(__file__), "help", self.cmdName + ".html")
