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

from radical.helpers import db, humanize_bytes

class Box:
    '''(NULL)'''
    def __init__(self):
        self.bid = None # int
        self.name = None # string
        self.ip = None # string
        self.sshUser = None # string
        self.sshPassword = None # string
        self.sshPort = None # int
        self.notes = None # string
        self.status = None
        self.os = None
        self.kernel = None
        self.uptime = None
        self.loadAvg = float(0.00)
        self.usedMemory = 0
        self.totalMemory = 0
        self.percentMemory = 0
        self.humanUsedMemory = '0 Mb'
        self.humanTotalMemory = '0 Mb'
        self.usedDisk = 0
        self.totalDisk = 0
        self.percentDisk = 0
        self.humanUsedDisk = '0 Mb'
        self.humanTotalDisk = '0 Mb'
        self.cpuModel = None
        self.cpuNumberCore = 0

        
        #get database connection
        self.con = db.get_connection()
        self.cur = self.con.cursor()

    def get_box_by_bid(self, bid):
        self.cur.execute("SELECT * FROM `box` WHERE `bid` = %s;", (bid))
        res = self.cur.fetchone()
        if res == None:
            return None
        else:
            self.bid = bid
            self.name = res[1]
            self.ip = res[2]
            self.sshUser = res[3]
            self.sshPassword = res[4]
            self.sshPort = res[5]
            self.notes = res[6]

            self.update_stats()

            return self

    def update_stats(self):
        self.cur.execute("SELECT * FROM `box_status` WHERE `bid` = %s ORDER BY `timestamp`  DESC LIMIT 0 , 1;", (self.bid))
        res = self.cur.fetchone()
        if not res == None:
            self.status = res[3]
            self.os = res[4]
            self.kernel = res[5]
            self.uptime = res[6]
            self.loadAvg = float(res[7])
            self.usedMemory = res[8]
            self.totalMemory = res[9]
            self.usedDisk = res[10]
            self.totalDisk = res[11]
            self.cpuModel = res[12]
            self.cpuNumberCore = res[13]

            try:
                self.percentMemory = 100*float(self.usedMemory)/float(self.totalMemory)
            except:
                self.percentMemory = 0

            self.humanUsedMemory = humanize_bytes(self.usedMemory)
            self.humanTotalMemory = humanize_bytes(self.totalMemory)

            try:
                self.percentDisk = 100*float(self.usedDisk)/float(self.totalDisk)
            except:
                self.percentDisk = 0

            self.humanUsedDisk = humanize_bytes(self.usedMemory)
            self.humanTotalDisk = humanize_bytes(self.totalMemory)

    def add_new_stats(self, status, os='', kernel='', uptime='', loadAvg=0.00, usedMemory=0, totalMemory=0, usedDisk=0, totalDisk=0, cpuModel='', cpuNumberCore=0):
        self.cur.execute("""INSERT INTO `box_status` (`bsid`, `bid`, `timestamp`, `status`, `os`, `kernel`, `uptime`, `load_avg`, `used_memory`, `total_memory`, `used_disk`, `total_disk`, `cpu_model`, `cpu_number_core`) 
                                              VALUES (NULL, %s, CURRENT_TIMESTAMP, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);""", (self.bid, status, os, kernel, uptime, float(loadAvg), usedMemory, totalMemory, usedDisk, totalDisk, cpuModel, cpuNumberCore))
        self.con.commit()

        self.update_stats()

