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

import hashlib
import os
import urllib
import cherrypy
from sqlalchemy import ForeignKey
from sqlalchemy import Column, Date, Integer, String, Boolean, Text
from sqlalchemy.orm import relationship, backref, sessionmaker

from radical.database import Base
from radical.database.BoxStats import BoxStats

__all__ = ['Box']

class Box(Base):
    __tablename__ = "boxes"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    ip = Column(String)
    sshUser = Column(String)
    sshPassword = Column(String)
    sshPort = Column(Integer)
    notes = Column(Text)

    def __init__(self, name, ip, sshUser, sshPassword, sshPort, notes):
        self.name = name
        self.ip = ip
        self.sshUser = sshUser
        self.sshPassword = sshPassword
        self.sshPort = sshPort
        self.notes = notes
        self.stats = None

    def add_new_stats(self, session, status, os='', kernel='', uptime='', loadAvg=0.00, usedMemory=0, totalMemory=0, usedSwap=0, totalSwap=0, usedDisk=0, totalDisk=0, cpuModel='', cpuNumberCore=0, hostname=''):
        bs = BoxStats(self.id, status, os, kernel, uptime, loadAvg, usedMemory, totalMemory, usedSwap, totalSwap, usedDisk, totalDisk, cpuModel, cpuNumberCore, hostname)
        session.add(bs)

    def get_last_stats(self, session=None):
        if session == None:
            session = cherrypy.request.db
        return session.query(BoxStats).filter(BoxStats.boxId == self.id).order_by(BoxStats.timestamp.desc()).first()
