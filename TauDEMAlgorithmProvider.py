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

from sextante.core.AlgorithmProvider import AlgorithmProvider
from sextante.core.SextanteConfig import SextanteConfig
from sextante.core.SextanteConfig import Setting
from sextante.core.SextanteLog import SextanteLog

from sextante_taudem.TauDEMAlgorithm import TauDEMAlgorithm
from sextante_taudem.TauDEMUtils import TauDEMUtils

from sextante_taudem.peukerdouglas import PeukerDouglas
from sextante_taudem.slopearea import SlopeArea
from sextante_taudem.lengtharea import LengthArea
from sextante_taudem.dropanalysis import DropAnalysis
from sextante_taudem.dinfdistdown import DinfDistDown
from sextante_taudem.dinfdistup import DinfDistUp
from sextante_taudem.gridnet import GridNet
from sextante_taudem.dinftranslimaccum import DinfTransLimAccum
from sextante_taudem.dinftranslimaccum2 import DinfTransLimAccum2

class TauDEMAlgorithmProvider(AlgorithmProvider):

    def __init__(self):
        AlgorithmProvider.__init__(self)
        self.createAlgsList()

    def getDescription(self):
        return "TauDEM (hydrologic analysis)"

    def getName(self):
        return "taudem"

    def getIcon(self):
        return QIcon(os.path.dirname(__file__) + "/icons/taudem.png")

    def initializeSettings(self):
        AlgorithmProvider.initializeSettings(self)
        SextanteConfig.addSetting(Setting(self.getDescription(), TauDEMUtils.TAUDEM_FOLDER, "TauDEM command line tools folder", TauDEMUtils.taudemPath()))
        SextanteConfig.addSetting(Setting(self.getDescription(), TauDEMUtils.MPIEXEC_FOLDER, "mpiexec folder", TauDEMUtils.mpiexecPath()))

    def unload(self):
        AlgorithmProvider.unload(self)
        SextanteConfig.removeSetting(TauDEMUtils.TAUDEM_FOLDER)
        SextanteConfig.removeSetting(TauDEMUtils.MPIEXEC_FOLDER)

    def _loadAlgorithms(self):
        self.algs = self.preloadedAlgs

    def createAlgsList(self):
        self.preloadedAlgs = []
        folder = TauDEMUtils.taudemDescriptionPath()
        for descriptionFile in os.listdir(folder):
            if descriptionFile.endswith("txt"):
                try:
                    alg = TauDEMAlgorithm(os.path.join(folder, descriptionFile))
                    if alg.name.strip() != "":
                        self.preloadedAlgs.append(alg)
                    else:
                        SextanteLog.addToLog(SextanteLog.LOG_ERROR, "Could not open TauDEM algorithm: " + descriptionFile)
                except Exception, e:
                    SextanteLog.addToLog(SextanteLog.LOG_ERROR, "Could not open TauDEM algorithm: " + descriptionFile)

        self.preloadedAlgs.append(PeukerDouglas())
        self.preloadedAlgs.append(SlopeArea())
        self.preloadedAlgs.append(LengthArea())
        self.preloadedAlgs.append(DropAnalysis())
        self.preloadedAlgs.append(DinfDistDown())
        self.preloadedAlgs.append(DinfDistUp())
        self.preloadedAlgs.append(GridNet())
        self.preloadedAlgs.append(DinfTransLimAccum())
        self.preloadedAlgs.append(DinfTransLimAccum2())
