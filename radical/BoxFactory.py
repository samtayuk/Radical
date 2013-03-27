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

from radical.helpers import db
from radical.Box import Box

class BoxFactory :
    '''(NULL)'''
    def __init__(self) :
        #get database connection
        self.con = db.get_connection()
        self.cur = self.con.cursor()

    def create_new_box(self, name, ip, sshUser, sshPassword, sshPort, notes):
        self.cur.execute("""INSERT INTO `box` (`bid`, `name`, `ip`, `ssh_user`, `ssh_password`, `ssh_port`, `notes`, `ssh_salt`) 
                                       VALUES (NULL, %s, %s, %s, %s, %s, %s, '');""",
                                              (name, ip, sshUser, sshPassword, sshPort, notes))
        self.con.commit()

        b = self.get_box_by_bid(self.cur.lastrowid)
        b.add_new_stats('pending')

        return b

    def get_all_boxes(self):
        self.cur.execute("SELECT `bid` FROM `box`;")
        rows = self.cur.fetchall()

        boxes = []
        for row in rows:
            boxes.append(self.get_box_by_bid(row[0]))
        return boxes
    
    def get_box_by_bid(self, bid):
        return Box().get_box_by_bid(bid)