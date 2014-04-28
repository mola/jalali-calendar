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

import pygtk
pygtk.require('2.0')

import gtk
import gtk.gdk
import calendar
import os
import os.path
import utility
from xml.dom.minidom import getDOMImplementation, parse
from xml.parsers.expat import ExpatError
from string import strip, lower

DATA_DIR="/usr/share/jalali-calendar"
mon_name = ["فروردین","اردیبهشت","خرداد","تیر","مرداد","شهریور"
            ,"مهر","آبان","آذر","دی","بهمن","اسفند"]
milady_monname = ["January","February","March","April","May","June","July",
                  "August","September","October","November","December"]
extrafile = "/.jcal_extra.xml"
imagelist={0:"balloons-aj.png",1:"marid.png",2:"shabdar.png",3:"cday.png"}

def _get_text(nodelist):
    rc = u""
    name = nodelist.nodeName
    for node in nodelist.childNodes:
        if node.nodeType == node.TEXT_NODE:
            rc = rc+ node.data
    return name,rc.strip()

def get_home():
    return os.environ.get('HOME', '')

def convert_to_str(num):
    s = str(num)
    uni_c = [u'\u06f0',u'\u06f1',u'\u06f2',u'\u06f3',u'\u06f4',u'\u06f5',u'\u06f6',u'\u06f7',u'\u06f8',u'\u06f9']
    res = u""
    if len(s)>0:
        for i in s:
            res += uni_c[int(i)]
    return res

class wmonth:
    def __init__(self):
        self.hbox=gtk.HBox()
        self.arrow_left2=gtk.Button()
        self.arrow_left2.set_relief(2)
        image=gtk.image_new_from_stock(gtk.STOCK_GO_BACK,gtk.ICON_SIZE_SMALL_TOOLBAR)
        self.arrow_left2.set_image(image)
        self.hbox.pack_start(self.arrow_left2,0,0,0)
        self.monthname=gtk.Label(" <b></b> ")
        self.monthname.set_use_markup(True)
        self.hbox.pack_start(self.monthname,0,0,0)
        self.arrow_right2=gtk.Button()
        self.arrow_right2.set_relief(2)
        image=gtk.image_new_from_stock(gtk.STOCK_GO_FORWARD,gtk.ICON_SIZE_SMALL_TOOLBAR)
        self.arrow_right2.set_image(image)

        self.hbox.pack_start(self.arrow_right2,0,0,0)
        self.hbox.show_all()
        
        self .label=gtk.HSeparator()
        self.hbox.pack_start(self.label,1,1,0)
        
        self.arrow_left=gtk.Button()
        self.arrow_left.set_relief(2)
        image=gtk.image_new_from_stock(gtk.STOCK_GO_BACK,gtk.ICON_SIZE_SMALL_TOOLBAR)
        self.arrow_left.set_image(image)
        self.hbox.pack_start(self.arrow_left,0,0,0)
        self.yearnum=gtk.Label(" <b></b> ")
        self.yearnum.set_use_markup(True)
        self.hbox.pack_start(self.yearnum,0,0,0)
        self.arrow_right=gtk.Button()
        self.arrow_right.set_relief(2)
        image=gtk.image_new_from_stock(gtk.STOCK_GO_FORWARD,gtk.ICON_SIZE_SMALL_TOOLBAR)
        self.arrow_right.set_image(image)
        self.hbox.pack_start(self.arrow_right,0,0,0)


class Main(gtk.Window):
    ww = 300
    wh = 70
    wh2 = 0
    def change_db(self,year):
        calfile=DATA_DIR+"/"+str(year)+".xml"
        if (os.path.isfile(calfile)):
            tmp = parse(calfile).documentElement
            self.db=tmp.getElementsByTagName("day")
        else:
            self.db=None
    
    def get_dayname(self,month,day):
        if (self.db==None):
            return None
        find = False
        for record in self.db:
            for element in record.childNodes:
                if element.nodeType != element.TEXT_NODE:
                    if element.nodeType != element.TEXT_NODE:
                        name, data = _get_text(element)
                        if (name=="num"):
                            sp=data.split("/")
                            if ( (month==int(sp[0])) and (day==int(sp[1])) ):
                                find = True
                        if ((name=="desc") and (find==True) ):
                            return data
        return None
   
    def __init__(self,year,month,day,size):

        self.db = None
        self.db2 = None
        
        self.change_db(year)
        #csize = [(146,300),(180,235),(205,335),(290,435)]
        #self.wh,self.ww = csize[size]
        
        self.full_list = get_customday(month,day)
        gtk.Window.__init__(self)
        self.set_keep_above(True)
        self.set_position(gtk.WIN_POS_MOUSE)
        self.set_decorated(False)
        self.set_has_frame(False)
        #self.set_resizable(False)
        self.set_border_width(0)
        self.set_skip_taskbar_hint(True)
        self.set_default_size(self.ww,self.wh)

        
        self.box2=gtk.Viewport()
        self.vbox2=gtk.VBox()
        self.vbox2.set_spacing(1)
        self.box2.add(self.vbox2)
        
        self.box1=gtk.Viewport()
        self.box1.set_border_width(5)
        self.vbox2.pack_start(self.box1,0,0,0)
        self.hbox3=gtk.HBox()
        self.date_label=gtk.Label()
        self.date_label.set_selectable(True)
        self.hbox3.pack_start(self.date_label,1,1,0)
        self.date_labelm=gtk.Label()
        self.date_labelm.set_selectable(True)
        self.hbox3.pack_start(self.date_labelm,1,1,0)
        
        self.vbox2.pack_start(self.hbox3,0,0,0)
        self.dayname=gtk.TextView()
        self.dayname.set_wrap_mode(gtk.WRAP_WORD)
        self.dayname.set_editable(False)
        self.dayname.set_cursor_visible(False)
        self.dayname.set_justification(gtk.JUSTIFY_CENTER)
        self.dayname.set_border_width(3)
        self.dayname.connect("size_request",self.checkresize)
        self.vbox2.pack_start(self.dayname,0,0,0)
        
        self.customday = gtk.TreeView()
        self.customstor = gtk.ListStore(gtk.gdk.Pixbuf,str)
        self.customday.set_model(self.customstor)
        self.customday.connect("size_request",self.checkresize_c)
        self.customday.set_headers_visible(False)
        cell0 = gtk.CellRendererPixbuf()
        col = gtk.TreeViewColumn("",cell0,pixbuf = 0)
        self.customday.append_column(col)

        cell1 = gtk.CellRendererText()
        col = gtk.TreeViewColumn("Date",cell1,text=1)
        self.customday.append_column(col)
        self.vbox2.pack_start(self.customday,0,0,0)
        
        self.add(self.box2)
        
        self.connect("destroy",self.quit)
        self.vbox=gtk.VBox()
        self.vbox.set_spacing(3)
        self.box1.add(self.vbox)

        self.header=wmonth()
        self.vbox.pack_start(self.header.hbox,0,0,0)
        self.header.arrow_left2.connect("clicked",self.month_prev)
        self.header.arrow_right2.connect("clicked",self.month_next)
        self.header.arrow_left.connect("clicked",self.year_prev)
        self.header.arrow_right.connect("clicked",self.year_next)
        #self.header.hbox.show_all()
        self.cal=calendar.pcalendar(year,month,day,DATA_DIR,loadcustomlist(),size)
        self.cal.connect("month-change",self.monthchange)
        self.cal.connect("day-change",self.daychange)
        #self.cal.show()
        self.vbox.pack_start(self.cal ,1 ,1, 0)
        self.wh += self.cal.get_cal_height()
        
        self.header.yearnum.set_label("<b>"+convert_to_str(year)+"</b>")
        self.header.monthname.set_label(' <b>'+mon_name[month-1]+'</b> ')
        self.day=day
        self.month=month
        self.year=year
        self.box2.show_all()
        self.change_lable(self.day)
        
        slabel=self.get_dayname(month,day)
        if (slabel!=None):
            buf = self.dayname.get_buffer()
            buf.set_text(slabel)
            self.dayname.set_buffer(buf)
            self.wh2=self.dayname.get_visible_rect()[3]
            self.resize(self.ww,self.wh+self.wh2)
        else:
            self.dayname.hide()
            self.wh2 = 0
    
        
        if (self.full_list != None):
            self.loadcustomday(self.month, self.day)
            self.resize(self.ww,self.wh+self.wh2+self.customday.get_visible_rect()[3])
        else:
            self.customday.hide()
            
    def checkresize(self,obj,data=None):
        self.wh2=data[1]-6
        self.resize(self.ww,self.wh+data[1]-6)

    def checkresize_c(self,obj,data=None):
        self.resize(self.ww,self.wh+self.wh2+data[1]-6)
        
    def monthchange(self,obj=None,month=None,year=None):
        self.header.yearnum.set_label("<b>"+convert_to_str(year)+"</b>")
        self.header.monthname.set_label(' <b>'+mon_name[month-1]+'</b> ')
        self.change_lable(self.day)

        if (self.year!=year):
            self.change_db(year)

        slabel=self.get_dayname(month,self.day)
        if (slabel!=None):
            buf = self.dayname.get_buffer()
            buf.set_text(slabel)
            self.dayname.set_buffer(buf)
            self.dayname.show()
        else:
            self.dayname.hide()
            self.wh2=0

        result = self.loadcustomday(self.month,self.day)
        if (result ==True):
            self.resize(self.ww,self.wh+self.wh2+self.customday.get_visible_rect()[3])
        else:
            self.customday.hide()
        
        if (result==False)and(slabel==None):
            self.resize(self.ww,self.wh)
        
        
    def daychange(self,obj=None,month=None,year=None,day=None):
        self.change_lable(day)

        self.day=day
        self.month=month
        self.year=year
        if (self.year!=year):
            self.change_db(year)
        slabel=self.get_dayname(month,day)
        if (slabel!=None):
            buf = self.dayname.get_buffer()
            buf.set_text(slabel)
            self.dayname.set_buffer(buf)
            self.dayname.show()
        else:
            self.dayname.hide()
            self.wh2=0

        result = self.loadcustomday(self.month,self.day)
        if (result ==True):
            self.resize(self.ww,self.wh+self.wh2+self.customday.get_visible_rect()[3])
        else:
            self.customday.hide()
        
        if (result==False)and(slabel==None):
            self.resize(self.ww,self.wh)


    def month_next(self,obj,data=None):
        self.cal.next_month()
        month=self.cal.get_month()
        self.header.monthname.set_label(' <b>'+mon_name[month-1]+'</b> ')
        year=self.cal.get_year()
        self.header.yearnum.set_label(' <b>'+convert_to_str(year)+'</b> ')
        self.month=month
        if (self.year!=year):
            self.change_db(year)
        else:
            self.dayname.hide()
        self.year=year
        self.change_lable(self.day)
        slabel=self.get_dayname(month,self.day)
        if (slabel!=None):
            buf = self.dayname.get_buffer()
            buf.set_text(slabel)
            self.dayname.set_buffer(buf)
            self.dayname.show()
        else:
            self.dayname.hide()
            self.wh2=0

        result = self.loadcustomday(self.month,self.day)
        if (result ==True):
            self.resize(self.ww,self.wh+self.wh2+self.customday.get_visible_rect()[3])
        else:
            self.customday.hide()
        
        if (result==False)and(slabel==None):
            self.resize(self.ww,self.wh)
        self.date_label.set_label(str(year)+"/"+str(month)+"/"+str(self.day))
        
    def month_prev(self,obj,data=None):
        self.cal.prev_month()
        month=self.cal.get_month()
        self.header.monthname.set_label(' <b>'+mon_name[month-1]+'</b> ')
        year=self.cal.get_year()
        self.header.yearnum.set_label(' <b>'+convert_to_str(year)+'</b> ')
        self.month=month
        if (self.year!=year):
            self.change_db(year)
        self.year=year
        self.change_lable(self.day)
        slabel=self.get_dayname(month,self.day)
        if (slabel!=None):
            buf = self.dayname.get_buffer()
            buf.set_text(slabel)
            self.dayname.set_buffer(buf)
            self.dayname.show()
        else:
            self.dayname.hide()
            self.wh2=0

        result = self.loadcustomday(self.month,self.day)
        if (result ==True):
            self.resize(self.ww,self.wh+self.wh2+self.customday.get_visible_rect()[3])
        else:
            self.customday.hide()
        
        #if (result==False)and(slabel==None):
        self.resize(self.ww,self.wh+self.wh2)
        self.date_label.set_label(str(year)+"/"+str(month)+"/"+str(self.day))

    def year_next(self,obj,data=None):
        self.cal.next_year()
        year=self.cal.get_year()
        self.header.yearnum.set_label(' <b>'+convert_to_str(year)+'</b> ')
        self.year=year
        self.change_lable(self.day)
        self.change_db(year)
        slabel=self.get_dayname(self.month,self.day)
        if (slabel!=None):
            buf = self.dayname.get_buffer()
            buf.set_text(slabel)
            self.dayname.set_buffer(buf)
            self.dayname.show()
        else:
            self.dayname.hide()
            self.wh2=0

        result = self.loadcustomday(self.month,self.day)
        if (result ==True):
            self.resize(self.ww,self.wh+self.wh2+self.customday.get_visible_rect()[3])
        else:
            self.customday.hide()
        
        if (result==False)and(slabel==None):
            self.resize(self.ww,self.wh)
        self.date_label.set_label(str(year)+"/"+str(self.month)+"/"+str(self.day))
    
    def year_prev(self, obj, data=None):
        self.cal.prev_year()
        year=self.cal.get_year()
        self.header.yearnum.set_label(' <b>'+convert_to_str(year)+'</b> ')
        self.year=year
        self.change_lable(self.day)
        self.change_db(year)
        slabel=self.get_dayname(self.month,self.day)
        if (slabel!=None):
            buf = self.dayname.get_buffer()
            buf.set_text(slabel)
            self.dayname.set_buffer(buf)
            self.dayname.show()
        else:
            self.dayname.hide()
            self.wh2=0

        result = self.loadcustomday(self.month,self.day)
        if (result ==True):
            self.resize(self.ww,self.wh+self.wh2+self.customday.get_visible_rect()[3])
        else:
            self.customday.hide()
        
        if (result==False)and(slabel==None):
            self.resize(self.ww,self.wh)
        self.date_label.set_label(str(year)+"/"+str(self.month)+"/"+str(self.day))

    def change_lable(self, day):
        year = self.cal.get_year()
        month=self.cal.get_month()
        y,m,d = utility.jalali_to_milady(year,month,day)
        text = "%s/%s (%s) /%s" % (y, milady_monname[m-1], m, d)
        self.date_labelm.set_label(text)
        text = "%s/%s/%s" % (year, month, day)
        self.date_label.set_label(text)

    def loadcustomday(self,mm,dd):
        find = False
        alllist=get_customday(mm,dd)
        if alllist!=None:
            find = True
            self.customstor.clear()
            for element in alllist:
                try:
                    pix = gtk.Image()
                    file = DATA_DIR+"/"+imagelist.get(int(element[2]))
                    pix.set_from_file(file)
                    p=pix.get_pixbuf()
                except:
                    p=None
                self.customstor.append([p,element[3]])
            self.customday.show()
        return find
        
    def quit(self,obj):
        self.destroy()

def getcustomfile():
    calfile=get_home()+extrafile
    if (os.path.isfile(calfile)):
        tmp = parse(calfile).documentElement
        return tmp.getElementsByTagName("day")
    else:
        return None

def loadcustomlist():
    customdb = getcustomfile()
    if customdb==None:
        return None 
    full_list = []
    for record in customdb:
        list = []
        for element in record.childNodes:
            if element.nodeType != element.TEXT_NODE:
                if element.nodeType != element.TEXT_NODE:
                    name, data = _get_text(element)
                    if (name=="num"):
                        sp=data.split("/")
                        list.append(int(sp[0]))
                        list.append(int(sp[1]))
                    if (name=="kind"):
                        list.append(int(data))
                    if (name=="desc"):
                        list.append(data)
        full_list.append(list)
    return full_list

def get_customday(mm,dd,fill=False):
    customdb = getcustomfile()
    if customdb==None:
        return None
    alllist = []
    
    for record in customdb:
        list = []
        find = False
        for element in record.childNodes:
            if element.nodeType != element.TEXT_NODE:
                if element.nodeType != element.TEXT_NODE:
                    name, data = _get_text(element)
                    if (name=="num"):
                        sp=data.split("/")
                        if ( (int(sp[0])==mm)and(int(sp[1])==dd) ):
                            find = True
                            list.append(sp[0])
                            list.append(sp[1])
                    if (find==True)and(name=="kind"):
                        list.append(data)
                    if (find==True)and(name=="desc"):
                        list.append(data)
        if list!=[]:
            alllist.append(list)
    if alllist!=[]:
        return alllist
    else:
        return None
    