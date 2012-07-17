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
import subprocess

from sextante.core.SextanteConfig import SextanteConfig
from sextante.core.SextanteLog import SextanteLog
from sextante.core.SextanteUtils import SextanteUtils

class TauDEMUtils:

    TAUDEM_FOLDER = "TAUDEM_FOLDER"
    MPIEXEC_FOLDER = "MPIEXEC_FOLDER"
    MPI_PROCESSES = "MPI_PROCESSES"

    @staticmethod
    def taudemPath():
        folder = SextanteConfig.getSetting(TauDEMUtils.TAUDEM_FOLDER)
        if folder == None:
            folder = ""

        return folder

    @staticmethod
    def mpiexecPath():
        folder = SextanteConfig.getSetting(TauDEMUtils.MPIEXEC_FOLDER)
        if folder == None:
            folder = ""

        return folder

    @staticmethod
    def taudemDescriptionPath():
        return os.path.normpath(os.path.join(os.path.dirname(__file__), "description"))

    @staticmethod
    def executeTauDEM(command, progress):
        loglines = []
        loglines.append("TauDEM execution console output")
        fused_command = ''.join(['"%s" ' % c for c in command])
        proc = subprocess.Popen(fused_command, shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True).stdout
        for line in iter(proc.readline, ""):
            loglines.append(line)
        SextanteLog.addToLog(SextanteLog.LOG_INFO, loglines)
