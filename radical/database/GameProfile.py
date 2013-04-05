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

import json

from sqlalchemy import Column, Date, Integer, String, Boolean, Text
from sqlalchemy.orm import relationship, backref, sessionmaker
from sqlalchemy.ext.hybrid import hybrid_property

from radical.database import Base

__all__ = ['GameProfile']

class GameProfile(Base):
	__tablename__ = "gameprofiles"

    id = Column(Integer, primary_key=True)
    key = Column(String)
    version = Column(Integer)
    name = Column(String)
    maxSlots = Column(Integer)
    command = Column(String)
    mapDirectory = Column(String)
    _options = Column('options', String)
    _installer = Column('installer', String)

    def __init__(self, key, version, name, maxSlots, command, mapDirectory, options, installer):
    	self.key = key
    	self.version = version
    	self.name = name
    	self.maxSlots = maxSlots
    	self.command = command
    	self.mapDirectory = mapDirectory
    	self.options = options
    	self.installer = installer

    @property
    def options(self):
        return json.loads(self._options)

    @options.setter
    def options(self, options):
        self._options = json.dumps(options)

    @property
    def installer(self):
        return json.loads(self._installer)

    @installer.setter
    def installer(self, installer):
        self._installer = json.dumps(installer)


	
