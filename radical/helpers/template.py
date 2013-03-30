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

import os
import sys
from urlparse import urlparse
from collections import OrderedDict

import cherrypy

from mako.template import Template
from mako.lookup import TemplateLookup
from mako import exceptions

import radical.auth

def serve_template(templatename, **kwargs):

    interface_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '..', 'data', 'interface')
    template_dir = os.path.join(str(interface_dir), 'default')
    
    print template_dir

    _hplookup = TemplateLookup(directories=[template_dir])

    nav = {'Home': {'url':'/','icon':'icon-home', 'required_type': 'user'},
           'Members': {'url':'/member','icon':'icon-user', 'required_type': 'admin'},
           'Groups': {'url':'/group','icon':'icon-group', 'required_type': 'user'},
           'Game Servers': {'url':'/server','icon':'icon-play-circle', 'required_type': 'user'},
           'Boxes': {'url':'/box','icon':'icon-laptop', 'required_type': 'admin'},
           'Settings': {'url':'/settings','icon':'icon-cog', 'required_type': 'admin'},
           }

    currentPath = urlparse(cherrypy.url()).path
    if currentPath.endswith('/'):
        currentPath = currentPath[:-1]

    genNav = {}

    currentMember = radical.auth.get_current_member()

    for navName, navOpt in nav.iteritems():
        if not currentMember == None:
            if not navOpt['required_type'] == 'admin' or currentMember.type == navOpt['required_type']:
                genNav[navName] = {'url': navOpt['url']}

                if 'icon' in navOpt:
                    genNav[navName]['icon'] = navOpt['icon']

                path = navOpt['url']
                if path.endswith('/'):
                    path = path[:-1]

                if currentPath == path:
                    genNav[navName]['selected'] = True

    try:
        template = _hplookup.get_template(templatename)
        return template.render(navItems=genNav, currentMember=currentMember, **kwargs)
    except:
        return exceptions.html_error_template().render()
