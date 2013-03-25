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

import db
import hashlib
import os
import urllib

class Member :
    '''(NULL)'''
    def __init__(self) :
        self.mid = None # int
        self.firstName = None # string
        self.lastName = None # string
        self.email = None # string
        self.active = None # bool
        self.notes = None # string
        self.type = None # string
        self.rid = None # int
        
        #get database connection
        self.con = db.get_connection()
        self.cur = self.con.cursor()
        pass

    def create_member(self, email, password, firstName, lastName, notes, active, mType):
        salt = self.generate_salt()
        password = self.encrypt_password(password, salt)

        self.cur.execute("INSERT INTO `member` (`email`, `password`, `first_name`, `last_name`, `active`, `notes`, `type`, `salt`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);", (email, password, firstName, lastName, active, notes, mType, salt))
        self.con.commit()

        return self.get_member_by_email(email)

    def get_member_by_mid(self, mid):
        self.cur.execute("SELECT * FROM `member` WHERE `mid` = %s;", (mid))
        res = self.cur.fetchone()
        if res == None:
            return None
        else:
            self.mid = res[0]
            self.email = res[1]
            self.firstName = res[3]
            self.lastName = res[4]
            self.active = res[5]
            self.notes = res[6]
            self.type =  res[7]
            return self

    def get_member_by_email(self, email):
        if not email == None:
            self.cur.execute("SELECT * FROM `member` WHERE `email` = %s;", (email))
            res = self.cur.fetchone()
            if res == None:
                return None
            else:
                self.mid = res[0]
                self.email = res[1]
                self.firstName = res[3]
                self.lastName = res[4]
                self.active = res[5]
                self.notes = res[6]
                self.type =  res[7]
        
        return self

    def check_password(self, password):
        self.cur.execute("SELECT `password`, `salt` FROM `member` WHERE `mid` = %s;", (self.mid))
        res = self.cur.fetchone()

        if not res == None:
            if res[0] == self.encrypt_password(password, res[1]):
                return True
            else:
                return False

    def change_first_name(self, firstName):
        self.firstName = firstName

    def change_last_name(self, lastName):
        self.lastName = lastName

    def change_email(self, email):
        self.email = email

    def change_notes(self, notes):
        self.notes = notes

    def change_type(self, mType):
        self.type = mType

    def change_password(self, password):
        salt = self.generate_salt()
        password = self.encrypt_password(password, salt)
        self.cur.execute("UPDATE `member` SET  `password` =  %s, `salt` = %s WHERE `mid` = %s;", (password, salt, self.mid))
        self.con.commit()

    def change_active(self, active):
        self.active = active

    def save_changes(self):
        self.cur.execute("UPDATE `member` SET  `email` =  %s, `first_name` = %s, `last_name` = %s, `active` = %s, `notes` = %s, `type` = %s WHERE `mid` = %s;", (self.email, self.firstName, self.lastName, self.active, self.notes,  self.type, self.mid))
        self.con.commit()

    def encrypt_password(self, password, salt):
        password = hashlib.sha512(str(salt) + str(password)).hexdigest()
        return password

    def generate_salt(self):
        return os.urandom(16).encode('base_64')

    def get_gravatar(self, size):
        # Set your variables here
        default = "http://www.example.com/default.jpg"

        # construct the url
        gravatar_url = "http://www.gravatar.com/avatar/" + hashlib.md5(self.email.lower()).hexdigest() + "?"
        gravatar_url += urllib.urlencode({'s':str(size)})
        return gravatar_url


