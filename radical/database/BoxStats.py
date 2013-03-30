# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
# This file is part of LizardPanel
### BEGIN LICENSE
# Copyright (C) 2013 Samuel Taylor <samtaylor.uk@gmail.com>
# This program is free software: you can redistribute it and/or modify it 
# under the terms of the GNU General Public License version 3, as published 
# by the Free Software Foundation.
# 
# This program is distributed in the hope that it will be useful, but 
# WITHOUT ANY WARRANTY; without even the implied warranties of 
# MERCHANTABILITY, SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR 
# PURPOSE.  See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along 
# with this program.  If not, see <http://www.gnu.org/licenses/>.
### END LICENSE

from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy import Column, Date, Integer, String, Boolean, Text, Float, BIGINT, DATETIME
from sqlalchemy.orm import relationship, backref, sessionmaker

from radical.database import Base
from radical.helpers import humanize_bytes

__all__ = ['BoxStats']

class BoxStats(Base):
    __tablename__ = "boxStatus"
    id = Column(Integer, primary_key=True)
    boxId = Column(Integer, ForeignKey('boxes.id'))
    timestamp = Column(DATETIME) 
    status = Column(String)
    os = Column(String)
    kernel = Column(String)
    uptime = Column(String)
    loadAvg = Column(Float)
    usedMemory = Column(BIGINT)
    totalMemory = Column(BIGINT)
    usedDisk = Column(BIGINT)
    totalDisk = Column(BIGINT)
    cpuModel = Column(String)
    cpuNumberCore = Column(Integer)

    def __init__(self, boxId, status, os, kernel, uptime, loadAvg, usedMemory, totalMemory, usedDisk, totalDisk, cpuModel, cpuNumberCore, timestamp=datetime.now()):
        self.boxId = boxId
        self.timestamp = timestamp
        self.status = status
        self.os = os
        self.kernel = kernel
        self.uptime = uptime
        self.loadAvg = loadAvg
        self.usedMemory = usedMemory
        self.totalMemory = totalMemory
        self.usedDisk = usedDisk
        self.totalDisk = totalDisk
        self.cpuModel = cpuModel
        self.cpuNumberCore = cpuNumberCore

        self.percentMemory = None
        self.percentDisk = None
        self.humanUsedMemory = None
        self.humanTotalMemory = None
        self.humanUsedDisk = None
        self.humanTotalDisk = None

    def set_percent(self):

        try:
            self.percentMemory = 100*float(self.usedMemory)/float(self.totalMemory)
        except:
            self.percentMemory = 0

        self.humanUsedMemory = humanize_bytes(int(self.usedMemory))
        self.humanTotalMemory = humanize_bytes(int(self.totalMemory))

        try:
            self.percentDisk = 100*float(self.usedDisk)/float(self.totalDisk)
        except:
            self.percentDisk = 0

        self.humanUsedDisk = humanize_bytes(int(self.usedMemory))
        self.humanTotalDisk = humanize_bytes(int(self.totalMemory))