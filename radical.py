#!/usr/bin/python
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
import cherrypy

from radical.handlers.RootHandler import RootHandler
from radical.handlers import ErrorHandlers
from radical import scheduler

if __name__ == '__main__':

    baseDir = os.path.dirname(os.path.realpath(__file__))

    conf = {'/':{
                'tools.mako.collection_size':500,
                'tools.mako.directories': os.path.join(baseDir, 'data', 'interface', 'default'),
                'tools.db.on': True,
            },
            '/interface':{
                'tools.staticdir.on': True,
                'tools.staticdir.dir': os.path.join(baseDir, 'data', 'interface')
            },
            '/bootstrap':{
                'tools.staticdir.on': True,
                'tools.staticdir.dir': os.path.join(baseDir, 'data', 'bootstrap')
            },
        }


    # Template engine tool
    from radical.template import MakoLoader
    main = MakoLoader()
    cherrypy.tools.mako = cherrypy.Tool('on_start_resource', main)
    
    # Database access tool
    from radical.lib.tool.db import SATool
    cherrypy.tools.db = SATool()

    # Database connection management plugin
    from radical.lib.plugin.db import SAEnginePlugin
    cherrypy.engine.db = SAEnginePlugin(cherrypy.engine)
    cherrypy.engine.db.subscribe()

    cherrypy.config.update({'error_page.404': ErrorHandlers.error_page_404, 'error_page.401': ErrorHandlers.error_page_401})
    
    scheduler.start_scheduler()

    cherrypy.tree.mount(RootHandler(), '/', conf)
    cherrypy.engine.start()
    cherrypy.engine.block()