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

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from libs.apscheduler.scheduler import Scheduler

from radical.database import Box
from radical.helpers.SshConnector import SshConnector

def get_box_status(session, box):
    
    i = 0
    while True:
        i += 1
        try:
            ssh = SshConnector(box.ip, box.sshUser, box.sshPassword, box.sshPort)
        except:
            if i >= 3:
                box.add_new_stats(session, 'offline')
                return False
        else:
            break
            



    commands = {'os':"lsb_release -ds", 
                'kernel':"uname -sri", 
                'uptime':"uptime | awk 'BEGIN { FS=\" |, \" } { print $2 }'",
                'loadAvg':"cut -f3 -d' ' /proc/loadavg",
                'usedMemory':"free -b | grep Mem | awk '{print $3}'",
                'totalMemory':"free -b | grep Mem | awk '{print $2}'",
                'usedSwap':"free -b | grep Swap | awk '{print $3}'",
                'totalSwap':"free -b | grep Swap | awk '{print $2}'",
                'usedDisk':"df -l --total | grep total | awk '{print $3}'",
                'avaDisk':"df -l --total | grep total | awk '{print $4}'",
                'cpuModel':"cat /proc/cpuinfo | grep 'model name' | sed -e 's/.*: //' | uniq",
                'cpuNumberCore':"cat /proc/cpuinfo | grep 'cpu core' | sed -e 's/.*: //' | uniq",
                'hostname': "hostname -A",
                }

    results = {}

    for key, command in commands.iteritems():
        stdin, stdout, stderr = ssh.exec_command(command)
        data = stdout.readline()
        results[key] = data.strip("\n")

    ssh.close()

    results['usedDisk'] = float(results['usedDisk']) * 1024
    results['avaDisk'] = float(results['avaDisk']) * 1024
    results['totalDisk'] =  results['usedDisk'] +  results['avaDisk']

    box.add_new_stats(session, 'online' ,results['os'], results['kernel'], results['uptime'], results['loadAvg'], results['usedMemory'], results['totalMemory'], results['usedSwap'], results['totalSwap'], results['usedDisk'], results['totalDisk'], results['cpuModel'], results['cpuNumberCore'], results['hostname'])
    return True

def get_boxes_status():
    print 'Started Check'
    engine = create_engine('sqlite:///twiseless.db', echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()

    boxes = session.query(Box).all()

    for box in boxes:
        print box.name
        get_box_status(session, box)

    session.commit()

scheduler = None
def start_scheduler():
    scheduler = Scheduler()
    scheduler.add_interval_job(get_boxes_status, seconds=30)
    scheduler.start()
