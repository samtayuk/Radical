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

import cherrypy
import glob
import os
import xml.etree.ElementTree as ET

from radical.auth import AuthController, require, member_of, name_is
from radical.lib.tool import template
from radical.database import GameProfile
from radical import DATA_DIR

class Settings:
    
    _cp_config = {
        'auth.require': [member_of('admin')]
    }

    @cherrypy.expose
    @cherrypy.tools.mako(filename="gameprofiles.html")
    def gameprofiles(self, cmd=None):
        if cmd == 'import':
            for xmlFile in glob.glob(os.path.join(DATA_DIR, 'gameprofiles','*.xml')):
                print xmlFile
                tree = ET.parse(xmlFile)
                root = tree.getroot()
                
                key = root.attrib['key']
                version = root.attrib['version']

                #Check to see if profile exists in database
                check = cherrypy.request.db.query(GameProfile).filter(GameProfile.key == key).filter(GameProfile.version == version).first()
                if not check == None:
                    continue

                name = root.find('name').text
                maxSlots = root.find('maxslots').text
                command = root.find('command').text
                mapDirectory = root.find('mapdirectory').text

                options = {}
                for option in root.find('options').findall('option'):
                    options[option.get('id')] = {'name': option.get('name'),
                                                      'type': option.get('type'),
                                                      'required': option.get('required'),
                                                      'key': option.get('key'),
                                                      'separator': option.get('key'),
                                                      'values': []
                                                      }

                    for value in option.findall('value'):
                        options[option.get('id')]['values'].append({'name': value.get('name'), 
                                                                         'value': value.text
                                                                         })

                    xmlInstaller = root.find('installer')
                    installer = {'type': xmlInstaller.get('type'), 'url': xmlInstaller.find('url').text}

                gp = GameProfile(key, version, name, maxSlots, command, mapDirectory, options, installer)
                cherrypy.request.db.add(gp)

            cherrypy.request.db.commit()
            raise cherrypy.HTTPRedirect("/settings/gameprofiles")

        gameProfiles = cherrypy.request.db.query(GameProfile).all()

        return {'title':"Radical", 'pageTitle': "Game Profiles", 'gameProfiles': gameProfiles}