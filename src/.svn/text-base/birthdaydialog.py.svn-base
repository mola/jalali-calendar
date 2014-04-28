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
import locale
from xml.dom.minidom import getDOMImplementation, parse
from xml.parsers.expat import ExpatError
from string import strip, lower

def _get_text(nodelist):
    rc = u""
    name = nodelist.nodeName
    for node in nodelist.childNodes:
        if node.nodeType == node.TEXT_NODE:
            rc = rc+ node.data
    return name,rc.strip()

imagelist=["balloons-aj.png","marid.png","shabdar.png","cday.png"]
extrafile = "/.jcal_extra.xml"
DATA_DIR="/usr/share/jalali-calendar"

def get_home():
        return os.environ.get('HOME', '')
    
class birthdialog:
    
    def __init__(self):
        self.glade=gtk.glade.XML(DATA_DIR+"/interface.glade","dialog1")
        self.bwindow=self.glade.get_widget("dialog1")
        dict={"on_closebutton1_clicked":self.bquit,
               "on_dialog1_destroy":self.bquit,
               "on_button1_clicked":self.element_add,
               "on_button3_clicked":self.element_delete,
               "on_button2_clicked":self.element_edit,
               "on_treeview1_cursor_changed":self.element_change
               }
        self.glade.signal_autoconnect(dict)
        
        self.combobox1=self.glade.get_widget("combobox1")
        self.spinbutton1=self.glade.get_widget("spinbutton1")
        self.combobox2=self.glade.get_widget("combobox2")
        self.entry1=self.glade.get_widget("entry1")
        self.edit_but=self.glade.get_widget("button2")

        self.treestore = gtk.ListStore(gtk.gdk.Pixbuf,str,str,int,int)
        self.treeview=self.glade.get_widget("treeview1")
        self.treeview.set_model(self.treestore)
        
        cell0 = gtk.CellRendererPixbuf()
        col = gtk.TreeViewColumn("",cell0,pixbuf = 0)
        self.treeview.append_column(col)

        cell1 = gtk.CellRendererText()
        col = gtk.TreeViewColumn("تاریخ",cell1,text=1)
        self.treeview.append_column(col)
        self.treeview.set_search_column(1)

        cell3 = gtk.CellRendererText()
        col = gtk.TreeViewColumn("توضیح",cell3,text=2)
        self.treeview.append_column(col)
        
        self.db=None
        self.fxml = None
        self.getfile()
        self.loadlist()
        self.selected_cursor = None
        self.combobox1.set_active(0)
        self.combobox2.set_active(3)
        
    def getfile(self):
        home = get_home()
        if not(os.path.isfile(home+extrafile)):
            self.db=None
            return
        calfile=home+extrafile
        self.fxml = parse(calfile)
        self.db=self.fxml.getElementsByTagName("day")
    
    def loadlist(self):
        if (self.db==None):
            return None
        element_code=1
        pix = gtk.Image()
        for record in self.db:
            list = []
            for element in record.childNodes:
                if element.nodeType != element.TEXT_NODE:
                    if element.nodeType != element.TEXT_NODE:
                        name, data = _get_text(element)
                        if (name=="num"):
                            sp=data.split("/")
                            list.append(sp[0])
                            list.append(sp[1])
                        if (name=="kind"):
                            list.append(data)
                        if (name=="desc"):
                            list.append(data)
            try:
                file = DATA_DIR+"/"+imagelist[int(list[2])]
                pix.set_from_file(file)
                p=pix.get_pixbuf()
            except:
                p=None
            self.treestore.append([p,list[0]+"/"+list[1],list[3],element_code,int(list[2])])
            element_code+=1
        if element_code==1:
            self.edit_but.set_property('sensitive', False)

    def element_add(self,obj,data=None):
        if not(os.path.isfile(get_home()+extrafile)):
            self.create_homefile()
        self.add()
        self.treestore.clear()
        self.getfile()
        self.loadlist()
        
    def element_delete(self,obj,data=None):
        self.delete()
        self.treestore.clear()
        self.getfile()
        self.loadlist()

    def element_edit(self,obj,data=None):
        self.delete()
        self.add()
        self.treestore.clear()
        self.getfile()
        self.loadlist()
        self.entry1.set_text("")
        
    def add(self):
        if self.fxml==None:
            return
        newday = self.fxml.createElement("day")
        field_day = self.fxml.createElement("num")
        mon = str(self.combobox1.get_active()+1)
        day = str(int(self.spinbutton1.get_value()))
        field_day_text = self.fxml.createTextNode(mon+"/"+day)
        
        field_kind = self.fxml.createElement("kind")
        kind = str(self.combobox2.get_active())
        field_kind_text = self.fxml.createTextNode(kind)

        field_desc = self.fxml.createElement("desc")
        text = self.entry1.get_text()
        field_desc_text = self.fxml.createTextNode(text)

        field_day.appendChild(field_day_text)
        field_kind.appendChild(field_kind_text)
        field_desc.appendChild(field_desc_text)
        
        newday.appendChild(field_day)
        newday.appendChild(field_kind)
        newday.appendChild(field_desc)
        
        db2=self.fxml.getElementsByTagName("customday")[0]
        db2.appendChild(newday)
        
        libxml = open(get_home()+extrafile,'w')
        libxml.write(self.fxml.toprettyxml(" "))
        libxml.close()
        
        self.entry1.set_text("")
        
    def element_change(self,obj,data=None):
        selection=obj.get_selection()
        (mode,iter)=selection.get_selected()
        self.selected_cursor=mode.get(iter,3)[0]
        sp= mode.get(iter,1)[0].split("/")
        self.combobox1.set_active(int(sp[0])-1)
        self.spinbutton1.set_value(int(sp[1]))
        self.combobox2.set_active(int(mode.get(iter,4)[0]))
        self.entry1.set_text(mode.get(iter,2)[0])
        self.edit_but.set_property('sensitive', True)
        
        
    def delete (self):
        if (self.db==None):
            return None
        el_code=1
        find =False

        db2=self.fxml.getElementsByTagName("customday")[0]
        for record in db2.getElementsByTagName("day"):
            for element in record.childNodes:
                if (el_code==self.selected_cursor):
                    removeday = db2.removeChild(record)
                    removeday.unlink()
                    find = True
                    break
            if find ==True:
                break
            el_code+=1

        libxml = open(get_home()+extrafile,'w')
        libxml.write(self.fxml.toprettyxml(" "))
        libxml.close()
        
    def create_homefile(self):
        xml = open(get_home()+extrafile,'w')
        xml.write('<?xml version="1.0" ?>')
        xml.write("")
        xml.write('<customday>')
        xml.write("")
        xml.write('</customday>')
        xml.close()
        self.fxml = parse(get_home()+extrafile)

        
    def bquit(self,obg,data=None):
        self.bwindow.destroy()