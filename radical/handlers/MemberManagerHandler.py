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

from radical.auth import AuthController, require, member_of, name_is
from radical import template

from radical.database.Member import Member
from radical.MemberFactory import MemberFactory

class MemberManagerHandler:
    
    # all methods in this controller (and subcontrollers) is
    # open only to members of the admin group
    
    _cp_config = {
        'auth.require': [member_of('admin')]
    }
    
    @cherrypy.expose
    @cherrypy.tools.mako(filename="member.html")
    def index(self):
        db = cherrypy.request.db
        members = db.query(Member).all()

        return {'title':"Radical - Member Manager", 'members':members}

    @cherrypy.expose
    @cherrypy.tools.mako(filename="edituser.html")
    def add(self, first_name=None, last_name=None, email=None, password=None, password_comfirm=None, active=None, notes=None, m_type=None):
        if first_name == None and last_name == None and email == None and password == None and password_comfirm == None:
            return serve_template(templatename="edituser.html", title="Radical - Create New Member", pageTitle="Create New Member", postUrl="/member/add")
        else:
            if active == 'on':
                active = True
            else:
                active = False

            if not password == password_comfirm:
                return {'title':"Radical - Create New Member", 
                        'pageTitle':"Create New Member", 
                        'postUrl':"/member/add", 
                        'error':"Error: Password Comfirm doesn't match the password."
                        }

            db = cherrypy.request.db
            m = Member(email, password, first_name, last_name, active, m_type, notes)

            db.add(m)
            db.commit()

            raise cherrypy.HTTPRedirect("/member")

    @cherrypy.expose
    @cherrypy.tools.mako(filename="edituser.html")
    def edit(self, mid = None, first_name=None, last_name=None, email=None, password=None, password_comfirm=None, active=None, notes=None, m_type=None):
        db = cherrypy.request.db
        mid = int(mid)
        m = db.query(Member).filter(Member.id == mid).first()
        if first_name == None and last_name == None and email == None:
            if mid == None:
                raise cherrypy.HTTPRedirect("/member")
            else:
                if m == None:
                    raise cherrypy.HTTPRedirect("/member")
                else:
                    return {'title':"Radical - Edit: %s %s" % (m.firstName, m.lastName), 
                            'pageTitle':"Edit: %s %s" % (m.firstName, m.lastName), 
                            'postUrl':"/member/edit/%i" % (mid), 
                            'firstName':m.firstName, 
                            'lastName':m.lastName, 
                            'email':m.email,
                            'notes':m.notes, 
                            'active':m.active, 
                            'mType':m.type,
                            'edit':True, 
                            'member':m
                            }
        else:
            if active == 'on':
                active = True
            else:
                active = False

            if not password == password_comfirm:
                return {'title':"Radical - Edit: %s %s" % (m.firstName, m.lastName), 
                        'pageTitle':"Edit: %s %s" % (m.firstName, m.lastName), 
                        'postUrl':"/member/edit/%i" % (mid),
                        'firstName':first_name, 
                        'lastName':last_name, 
                        'email':email, 
                        'notes':notes, 
                        'active':active, 
                        'mType':m_type, 
                        'edit':True, 
                        'error':"Error: Password Comfirm doesn't match the password.", 
                        'member':m
                        }

            

            m.firstName = first_name
            m.lastName = last_name
            m.email = email
            m.notes = notes
            m.active = active
            m.type = m_type

            if not password == None and not password == '':
                m.change_password(password)

            db.commit()
            
            raise cherrypy.HTTPRedirect("/member")

    @cherrypy.expose
    def delete(self, mid, comfirm=None):
        m = cherrypy.request.db.query(Member).filter(Member.id==mid).first()
        if comfirm == 'True':
            cherrypy.request.db.delete(m)
            cherrypy.request.db.commit()
        raise cherrypy.HTTPRedirect("/member")
