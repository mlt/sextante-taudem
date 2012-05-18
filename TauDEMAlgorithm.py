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

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from qgis.core import *

from sextante.core.GeoAlgorithm import GeoAlgorithm
from sextante.core.SextanteLog import SextanteLog
from sextante.core.SextanteUtils import SextanteUtils
from sextante.core.SextanteConfig import SextanteConfig
from sextante.core.GeoAlgorithmExecutionException import GeoAlgorithmExecutionException
from sextante.core.QGisLayers import QGisLayers
from sextante.core.LayerExporter import LayerExporter

from sextante.parameters.ParameterTable import ParameterTable
from sextante.parameters.ParameterMultipleInput import ParameterMultipleInput
from sextante.parameters.ParameterRaster import ParameterRaster
from sextante.parameters.ParameterVector import ParameterVector
from sextante.parameters.ParameterBoolean import ParameterBoolean
from sextante.parameters.ParameterFactory import ParameterFactory
from sextante.parameters.ParameterNumber import ParameterNumber
from sextante.parameters.ParameterSelection import ParameterSelection

from sextante.outputs.OutputTable import OutputTable
from sextante.outputs.OutputRaster import OutputRaster
from sextante.outputs.OutputVector import OutputVector
from sextante.outputs.OutputFactory import OutputFactory

from sextante_taudem.TauDEMUtils import TauDEMUtils

class TauDEMAlgorithm(GeoAlgorithm):

    def __init__(self, descriptionfile):
        GeoAlgorithm.__init__(self)
        self.descriptionFile = descriptionfile
        self.defineCharacteristicsFromFile()

    def getCopy(self):
        newone = TauDEMAlgorithm(self.descriptionFile)
        newone.provider = self.provider
        return newone

    def getIcon(self):
        return  QIcon(os.path.dirname(__file__) + "/icons/taudem.png")

    def defineCharacteristicsFromFile(self):
        lines = open(self.descriptionFile)
        line = lines.readline().strip("\n").strip()
        self.name = line
        line = lines.readline().strip("\n").strip()
        self.cmdName = line
        line = lines.readline().strip("\n").strip()
        self.group = line
        while line != "":
          try:
              line = line.strip("\n").strip()
              if line.startswith("Parameter"):
                  param = ParameterFactory.getFromString(line)
                  self.addParameter(param)
              else:
                  self.addOutput(OutputFactory.getFromString(line))
              line = lines.readline().strip("\n").strip()
          except Exception, e:
              SextanteLog.addToLog(SextanteLog.LOG_ERROR, "Could not load TauDEM algorithm: " + self.descriptionFile + "\n" + line)
              raise e
        lines.close()

    def processAlgorithm(self, progress):
        path = TauDEMUtils.taudemPath()
        if path == "":
            raise GeoAlgorithmExecutionException("TauDEM folder is not configured.\nPlease configure it before running TauDEM algorithms.")

        commands = []
        commands.append("mpiexec -n")


        for param in self.parameters:
            if param.value == None or param.value == "":
                continue
            if isinstance(param, (ParameterRaster, ParameterVector)):
                commands.append(param.name)
                commands.append(param.value)
            elif isinstance(param, ParameterBoolean):
                if param.value:
                    commands.append(param.name)
                    commands.append(str(param.value).lower())
            else:
                commands.append(param.name)
                commands.append(str(param.value))

        for out in self.outputs:
            commands.append(out.name)
            commands.append(out.value);

        loglines = []
        loglines.append("TauDEM execution command")
        for line in commands:
            loglines.append(line)
        SextanteLog.addToLog(SextanteLog.LOG_INFO, loglines)
        TauDEMUtils.executeOtb(commands, progress)
