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

from urlparse import urlparse
import cherrypy
from mako.lookup import TemplateLookup

import radical.auth

class MakoHandler(cherrypy.dispatch.LateParamPageHandler):
    """Callable which sets response.body."""
    
    def __init__(self, template, next_handler):
        self.template = template
        self.next_handler = next_handler
    
    def __call__(self):
        env = globals().copy()
        env.update(self.next_handler())
        
        nav = {'Home': {'url':'/','icon':'icon-home', 'required_type': 'user'},
               'Members': {'url':'/member','icon':'icon-user', 'required_type': 'admin'},
               'Groups': {'url':'/group','icon':'icon-group', 'required_type': 'user'},
               'Game Servers': {'url':'/server','icon':'icon-play-circle', 'required_type': 'user'},
               'Boxes': {'url':'/box','icon':'icon-laptop', 'required_type': 'admin'},
               'Settings': {'url':'/settings','icon':'icon-cog', 'required_type': 'admin'},}

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
        
        return self.template.render(navItems=genNav, currentMember=currentMember, **env)


class MakoLoader(object):
    
    def __init__(self):
        self.lookups = {}
    
    def __call__(self, filename, directories, module_directory=None,
                 collection_size=-1):
        # Find the appropriate template lookup.
        key = (tuple(directories), module_directory)
        try:
            lookup = self.lookups[key]
        except KeyError:
            lookup = TemplateLookup(directories=directories,
                                    module_directory=module_directory,
                                    collection_size=collection_size,
                                    )
            self.lookups[key] = lookup
        cherrypy.request.lookup = lookup
        
        # Replace the current handler.
        cherrypy.request.template = t = lookup.get_template(filename)
        cherrypy.request.handler = MakoHandler(t, cherrypy.request.handler)

cherrypy.tools.mako = cherrypy.Tool('on_start_resource', MakoLoader())

    