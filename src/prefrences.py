#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
##
#    
#    Copyright (C) 2007  Mola Pahnadayan
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
##

import os
import pygtk
pygtk.require('2.0')

import gtk,gtk.glade
import gtk.gdk
import calendar
import os.path
import sys
import gconf
import locale

DATA_DIR= "/usr/share/jalali-calendar"

class dp:
    def __init__(self):
        self.glade=gtk.glade.XML(DATA_DIR+"/interface.glade","dialog2")
        self.bwindow=self.glade.get_widget("dialog2")
        dict={"on_okbutton1_clicked":self.bsquit,
              "on_radiobutton1_activate":self.radio_check,
               "on_dialog2_destroy":self.bquit,
               }
        self.glade.signal_autoconnect(dict)
        
        self.cbutton1=self.glade.get_widget("checkbutton1")
        self.conf_client = gconf.client_get_default()
        self.conf_client.add_dir("/apps/jcalendar", gconf.CLIENT_PRELOAD_NONE)
        show_time=self.conf_client.get_bool("/apps/jcalendar/show_time")
        self.cbutton1.set_active(show_time)

        self.combobox=self.glade.get_widget("combobox3")
        type=show_time=self.conf_client.get_int("/apps/jcalendar/time_type")
        self.combobox.set_active(type)

        self.cbutton2=self.glade.get_widget("checkbutton2")
        show_sec=self.conf_client.get_bool("/apps/jcalendar/show_sec")
        self.cbutton2.set_active(show_sec)
        
        self.cal_size=self.conf_client.get_int("/apps/jcalendar/cal_size")
        self.glade.get_widget("r%s"%(self.cal_size)).set_active(True)
        
    
    def bsquit(self,obg,data=None):
        self.conf_client.set_bool("/apps/jcalendar/show_time", self.cbutton1.get_active())
        self.conf_client.set_int("/apps/jcalendar/time_type", self.combobox.get_active())
        self.conf_client.set_bool("/apps/jcalendar/show_sec", self.cbutton2.get_active())
        self.conf_client.set_int("/apps/jcalendar/cal_size", self.cal_size)
        self.bwindow.destroy()
    
    def radio_check(self,obj=None,data=None):
        if obj.get_active():
            self.cal_size=int(obj.get_name()[1])
        
    def bquit(self,obg,data=None):
        self.bwindow.destroy()