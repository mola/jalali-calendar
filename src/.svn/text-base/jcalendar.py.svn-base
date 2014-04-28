#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
os.environ['LANG']="fa_IR.UTF-8"

import pygtk
pygtk.require('2.0')

import gtk,gobject
import sys
import gnome.ui
import gnomeapplet
import utility
import time
import datetime
import gconf
import pynotify
import caldialog
import birthdaydialog
import holiday
import prefrences

PIXDIR = "/usr/share/jalali-calendar/date/"
mon_name = ["فروردین","اردیبهشت","خرداد","تیر","مرداد","شهریور","مهر","آبان","آذر","دی","بهمن","اسفند"]

def convert_to_str(num):
    s = str(num)
    uni_c = [u'\u06f0',u'\u06f1',u'\u06f2',u'\u06f3',u'\u06f4',u'\u06f5',u'\u06f6',u'\u06f7',u'\u06f8',u'\u06f9']
    res = u""
    if len(s)>0:
        for i in s:
            res += uni_c[int(i)]
    return res
class Jcalendar:
    timeout_interval = 1000
    def timeout_callback(self,obj=None,Time=None):
        jdate=utility.convert_to_jalali(time.time())
        self.year=jdate[0]
        self.month=jdate[1]
        self.day=jdate[2]
        if self.show_time==True:
            self.set_time()
        if self.lastday!=jdate[2]:
            if self.get_day_details():
                backimage = self.iamge_composite(PIXDIR+"bx-02.png",PIXDIR+"x-"+str(jdate[2])+".png")
            else:
                backimage = self.iamge_composite(PIXDIR+"bx-01.png",PIXDIR+"x-"+str(jdate[2])+".png")
            self.image.set_from_pixbuf(backimage)
            self.tbutton.set_image(self.image)
            self.tooltips.set_tip(self.tbutton,convert_to_str(self.day)+" "+mon_name[self.month-1]+" "+convert_to_str(self.year))

        self.lastday = jdate[2]
        return True
		
    def iamge_composite(self,add1,add2):
		pixbuf1 = gtk.gdk.pixbuf_new_from_file(add2)
		pixbuf2 = gtk.gdk.pixbuf_new_from_file(add1)
		pixbuf1.composite(pixbuf2, 0, 0, 21, 21, 1, 1, 1, 1, gtk.gdk.INTERP_BILINEAR, 255)
		return pixbuf2
	
    def button_press(self,obj,event=None):
		if event.button !=1:
			obj.stop_emission("button_press_event")
		return False
		
    def cal_show(self,obj,data=None):
		if obj.get_active():
			self.dialog=caldialog.Main(self.year,self.month,self.day,self.cal_size)
			self.dialog.show()
		else:
			self.dialog.destroy()

    def about_show(self,obj=None,data=None):
		about = gnome.ui.About("Jalali calendar applet","1.6.7","GPL",
							   "Applet to check jalali calendar",
							   ["نویسنده مولا پهنادایان","\n با تشکر از",
                                "هدایت وطن‌خواه","حسن شفیعی منفرد"])
		about.show()
	
    def birthday_add(self,obj=None,data=None):
		x=birthdaydialog.birthdialog()
		
    def set_show_time(self,obj=None,data=None):
		if self.show_time==False:
			self.show_time=True
			self.lastmin -= 1
			self.set_time()
		else:
			self.show_time=False
			self.tbutton.set_label("")
		self.conf_client.set_bool("/apps/jcalendar/show_time", self.show_time)
	
    def set_time(self):
        t = datetime.datetime.now()
        t = t.timetuple()
        if (self.lastmin!=t[4])or(self.show_sec==True):
            hour = str(t[3])
            if (self.type==0):
                clock=" AM"
                if (t[3]>12):
                    hour = str(t[3]-12)
                    clock=" PM"
            else:
                clock=" "
            if t[3]==0:
				hour="12"
            min = str(t[4])
            if t[4]<=9:
				min="0"+str(t[4])
            todo = hour+":"+min
            if self.show_sec:
                if t[5]<10:
                    tmp=":0"
                else:
                    tmp=":"
                todo += tmp+str(t[5])
            todo+=clock
            self.tbutton.set_label(todo)
            sec=self.tbutton.get_label()
        self.lastmin=t[4]

    def day_of_week(self,year,month,day):
		days=utility.scalar_Days(year,month,day)
		days=utility.jalalyDate(days)
		return days

    def get_day_details(self):
		checkholiday = False
		customday = -1
		if (holiday.holiday.has_key(self.year)):
			for holi in holiday.holiday.get(self.year):
				if (self.month==holi[0])and(self.day==holi[1]):
					checkholiday = True
		if self.day_of_week(self.year,self.month,self.day)==6:
			checkholiday = True
        
		return checkholiday

    def show_pre(self,obj=None,data=None):
        dialog=prefrences.dp()
        zz=dialog.bwindow.run()
        self.show_time=self.conf_client.get_bool("/apps/jcalendar/show_time")
        self.type=show_time=self.conf_client.get_int("/apps/jcalendar/time_type")
        self.show_sec=self.conf_client.get_bool("/apps/jcalendar/show_sec")
        self.cal_size=self.conf_client.get_int("/apps/jcalendar/cal_size")
        if self.show_time==False:
            self.show_sec=False
            self.tbutton.set_label("")
        else:
            self.lastmin -= 1
            self.set_time()

    def print_day(self,obj=None,Time=None):
        
        pynotify.init("Jcalendar")
        list=caldialog.get_customday(self.month,self.day)
        slist= ""
        for element in list:
            slist+=element[3]+'\n'
        n = pynotify.Notification("امروز", slist)
        n.set_urgency(pynotify.URGENCY_NORMAL )
        n.set_timeout(60*1000)
        n.set_icon_from_pixbuf(self.image.get_pixbuf())
        n.attach_to_widget(self.image)
        if not n.show():
            print "Can't create notify"
        return False


    def __init__(self,applet,iid):
        self.propxml="""
		<popup name="button3">
		<menuitem name="Item1" verb="Customday" label="_Custom day" pixtype="stock" pixname="gtk-add"/>
		<menuitem name="Item2" verb="Preferences" label="_Preferences"  pixtype="stock" pixname="gtk-preferences"/>
		<menuitem name="Item3" verb="About" label="_About..." pixtype="stock" pixname="gnome-stock-about"/>
		</popup>"""
		
        self.verbs = [ ("About", self.about_show ),
					   ("Customday",self.birthday_add),
					   ("Preferences",self.show_pre)  ]
		
        self.conf_client = gconf.client_get_default()
        self.conf_client.add_dir("/apps/jcalendar", gconf.CLIENT_PRELOAD_NONE)
        self.show_time=self.conf_client.get_bool("/apps/jcalendar/show_time")
        self.type=show_time=self.conf_client.get_int("/apps/jcalendar/time_type")
        self.show_sec=self.conf_client.get_bool("/apps/jcalendar/show_sec")
        self.cal_size=self.conf_client.get_int("/apps/jcalendar/cal_size")
        
        jdate=utility.convert_to_jalali(time.time())
		
        self.year=jdate[0]
        self.month=jdate[1]
        self.day=jdate[2]
        self.lastday = self.day
        self.lastmin = -1
        self.applet = applet
        self.image = gtk.Image()
        if self.get_day_details():
			backimage = self.iamge_composite(PIXDIR+"bx-02.png",PIXDIR+"x-"+str(jdate[2])+".png")
        else:
			backimage = self.iamge_composite(PIXDIR+"bx-01.png",PIXDIR+"x-"+str(jdate[2])+".png")

        self.image.set_from_pixbuf(backimage)
        todo = ""
        self.tooltips = gtk.Tooltips()
        self.tbutton=gtk.ToggleButton()
        self.tbutton.set_relief(2)
        self.tbutton.set_image(self.image)
        self.tbutton.connect("button_press_event",self.button_press)
        self.tbutton.connect("toggled",self.cal_show)
        if self.show_time:
			self.set_time()
        self.tooltips.set_tip(self.tbutton,convert_to_str(self.day)+" "+mon_name[self.month-1]+" "+convert_to_str(self.year))
        self.applet.setup_menu(self.propxml,self.verbs,None)
        self.applet.add(self.tbutton)
        self.applet.show_all()
        self.applet.set_background_widget(self.applet)
        gobject.timeout_add(self.timeout_interval,self.timeout_callback, self)
        gobject.timeout_add(6000,self.print_day, self)
		
def jcalendar_applet_factory(applet, iid):
	Jcalendar(applet,iid)
	return gtk.TRUE

if len(sys.argv) == 2 and sys.argv[1] == "run-in-window":
	main_window = gtk.Window(gtk.WINDOW_TOPLEVEL)
	main_window.set_title("Japplet Applet")
	main_window.connect("destroy", gtk.main_quit) 
	app = gnomeapplet.Applet()
	jcalendar_applet_factory(app, None)
	app.reparent(main_window)
	main_window.show_all()
	gtk.main()
	sys.exit()

if __name__ == '__main__':
	gnomeapplet.bonobo_factory("OAFIID:GNOME_PyJcalendarApplet_Factory", 
							   gnomeapplet.Applet.__gtype__, 
							   "Jcalendar", "0", jcalendar_applet_factory)
