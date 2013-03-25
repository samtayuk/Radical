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

from lizardpanel.auth import AuthController, require, member_of, name_is
from lizardpanel.template import serve_template

from lizardpanel.MemberFactory import MemberFactory
from lizardpanel.Member import Member

class MemberManagerHandler:
    
    # all methods in this controller (and subcontrollers) is
    # open only to members of the admin group
    
    _cp_config = {
        'auth.require': [member_of('admin')]
    }
    
    @cherrypy.expose
    def index(self):
        members = MemberFactory().get_all_members()
        return serve_template(templatename="member.html", title="LizzardPanel - Member Manager", members=members)

    @cherrypy.expose
    def add(self, first_name=None, last_name=None, email=None, password=None, password_comfirm=None, active=None, notes=None, m_type=None):
        if first_name == None and last_name == None and email == None and password == None and password_comfirm == None:
            return serve_template(templatename="edituser.html", title="LizzardPanel - Create New Member", pageTitle="Create New Member", postUrl="/member/add")
        else:
            if active == 'on':
                active = True
            else:
                active = False

            if not password == password_comfirm:
                return serve_template(templatename="edituser.html", title="LizzardPanel - Create New Member", pageTitle="Create New Member", postUrl="/member/add", error="Error: Password Comfirm doesn't match the password.")

            m = Member().create_member(email, password, first_name, last_name, notes, active, m_type)
            if m == None:
                return serve_template(templatename="edituser.html", title="LizzardPanel - Create New Member", pageTitle="Create New Member", error="Error has occured when trying to create a new member.")
            else:
                raise cherrypy.HTTPRedirect("/member")

    @cherrypy.expose
    def edit(self, mid = None, first_name=None, last_name=None, email=None, password=None, password_comfirm=None, active=None, notes=None, m_type=None):
        mid = int(mid)
        if first_name == None and last_name == None and email == None:
            if mid == None:
                raise cherrypy.HTTPRedirect("/member")
            else:
                m = Member().get_member_by_mid(mid)
                if m == None:
                    raise cherrypy.HTTPRedirect("/member")
                else:
                    return serve_template(templatename="edituser.html", title="LizzardPanel - Edit: %s %s" % (m.firstName, m.lastName), pageTitle="Edit: %s %s" % (m.firstName, m.lastName), postUrl="/member/edit/%i" % (mid), firstName=m.firstName, lastName=m.lastName, email=m.email, notes=m.notes, active=m.active, mType=m.type, edit=True, member=m)
        else:
            m = Member().get_member_by_mid(mid)

            if active == 'on':
                active = True
            else:
                active = False

            if not password == password_comfirm:
                return serve_template(templatename="edituser.html", title="LizzardPanel - Edit: %s %s" % (m.firstName, m.lastName), pageTitle="Edit: %s %s" % (m.firstName, m.lastName), postUrl="/member/edit/%i" % (mid), firstName=first_name, lastName=last_name, email=email, notes=notes, active=active, mType=m_type, edit=True, error="Error: Password Comfirm doesn't match the password.", member=m)

            m.change_first_name(first_name)
            m.change_last_name(last_name)
            m.change_email(email)
            m.change_notes(notes)
            m.change_active(active)
            m.change_type(m_type)
            print "Type: " + m_type
            print "Type: " + str(active)

            m.save_changes()

            if not password == None and not password == '':
                print "WTF: " + str(password)
                m.change_password(password)
            
            raise cherrypy.HTTPRedirect("/member")

    @cherrypy.expose
    def delete(self, mid, comfirm=None):
        if comfirm == 'True':
            MemberFactory().delete_member(mid)
        raise cherrypy.HTTPRedirect("/member")
