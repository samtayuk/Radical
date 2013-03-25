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

from Member import Member

class MemberFactory:
    def __init__(self):
        #get database connection
        self.con = db.get_connection()
        self.cur = self.con.cursor()
        pass

    def get_all_members(self):
        self.cur.execute("SELECT `mid` FROM `member`;")
        rows = self.cur.fetchall()

        members = []
        for row in rows:
            members.append(Member().get_member_by_mid(row[0]))
        return members

    def delete_member(self, mid):
        self.cur.execute("DELETE FROM `member` WHERE `mid` = %s;", (mid))
        self.con.commit()
