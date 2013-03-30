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

from sqlalchemy import ForeignKey, Table
from sqlalchemy import Column, Date, Integer, String, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref, sessionmaker

from radical.database import Base

__all__ = ['Member']

#groupMembersTable = Table('groupMembers', Base.metadata,
#    Column('memberId', Integer, ForeignKey('members.id')),
#    Column('groupId', Integer, ForeignKey('groups.id'))
#)

class Member(Base):
    __tablename__ = "members"

    id = Column(Integer, primary_key=True)
    email = Column(String)
    password = Column(String)
    passwordSalt = Column(String)
    firstName = Column(String)
    lastName = Column(String)
    active = Column(Boolean)
    type = Column(String)
    notes = Column(Text)
 #   groupsOwner = relationship("Group", backref="owner")
 #   groups = relationship("Group", secondary=groupMembersTable, backref="members")

    def __init__(self, email, password, firstName, lastName, active, type, notes, passwordSalt=None):
        self.email = email
        self.firstName = firstName
        self.lastName = lastName
        self.active = active
        self.type = type
        self.notes = notes

        if passwordSalt == None:
            self.change_password(password)
        else:
            self.password = password
            self.passwordSalt = passwordSalt

    def check_password(self, password):
        if not self.password == None:
            if self.password == self.encrypt_password(password, self.passwordSalt):
                return True
            else:
                return False

    def change_password(self, password):
        self.passwordSalt = self.generate_salt()
        self.password = self.encrypt_password(password, self.passwordSalt)

    def encrypt_password(self, password, salt):
            password = hashlib.sha512(str(salt) + str(password)).hexdigest()
            return password

    def generate_salt(self):
            return os.urandom(32).encode('base_64')

    def get_gravatar_url(self, size=32):
        gravatar_url = "http://www.gravatar.com/avatar/" + hashlib.md5(self.email.lower()).hexdigest() + "?"
        gravatar_url += urllib.urlencode({'s':str(size), 'd':'retro'})
        return gravatar_url