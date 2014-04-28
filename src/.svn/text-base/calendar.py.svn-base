#!/usr/bin/env python
## -*- coding: utf-8 -*-#
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
import gobject
from gtk import gdk
import pango
import cairo
import utility
import holiday

BORDER_WIDTH = 0
days_in_months=( [0,31, 62, 93, 124, 155, 186, 216, 246, 276, 306, 336, 365],
                 [0,31, 62, 93, 124, 155, 186, 216, 246, 276, 306, 336, 366])

month_length = ( [0,31, 31, 31, 31, 31, 31, 30, 30, 30, 30, 30, 29],
                 [0,31, 31, 31, 31, 31, 31, 30, 30, 30, 30, 30, 30])

def day_of_week(year,month,day):
    days=utility.scalar_Days(year,month,day)
    days=utility.jalalyDate(days)
    return days

def weeks_in_year(year):
    return(52 + ((day_of_week(year,1,1)==4) or (day_of_week(year,12,31)==4)))

def week_number(year,month,day):
    first = day_of_week(year,1,1) - 1
    return( ( (dates_difference(year,1,1, year,month,day) + first) / 7 )+(first < 4) )

def year_to_days(year):
    return( year * 365 + (year / 4) - (year / 100) + (year / 400) )
  
def check_date(year,month,day):
    if (year < 1):
        return False
    if ((month < 1) or (month > 12)):
        return False
    if ((day < 1) or (day > month_length[utility.leap(year)][month])):
        return False
    return True

def calc_days(year, month, day):
    if (year < 1):
        return 0
    if ((month < 1) or (month > 12)):
        return 0
    lp=utility.leap(year)
    if ((day < 1) or (day > month_length[lp][month])):
        return 0
    return( year_to_days( (year-1) ) + days_in_months[lp][month] + day )

def dates_difference(year1,month1,day1,
                     year2,month2,day2):
  return( calc_days(year2, month2, day2) - calc_days(year1, month1, day1) )

#imagelist=["balloons-aj.png","marid.png","shabdar.png"]

class pcalendar(gtk.Widget):

    Dayname = ["شنبه","یک","دو","سه","چهار","پنج","جمعه"]
    left_margin = 30
    top_margin = 25
    row_height = [0,0,0,0,0,0]
    col_width = [0,0,0,0,0,0,0]
    basecol_width = 0
    day=[]
    day_mil=[]
    current_day=[0,0]
    cheight = 0
    cwidth = 0
    cfont = ['Sans 10','Sans 12','Sans 14','Sans 16']
    csfont = ['Sans 6','Sans 8','Sans 10','Sans 12']
    csize = [(106,135),(160,235),(205,335),(290,435)]
    size = 0
    def __init__(self,year,month,day,datadir=None,extra=None,size=0):
        gtk.Widget.__init__(self)
        self.size = size
        self.cheight,self.cwidth = self.csize[self.size]

        self.colormap = self.get_colormap()
        self.RED_COLOR   = self.colormap.alloc_color(60000, 10535, 10000)
        self.DEACTIVE_COLOR = self.style.fg[gtk.STATE_INSENSITIVE]
        self.NORMAL_DAY_COLOR = self.style.text[gtk.STATE_NORMAL]
        self.SELECTED_DAY_COLOR = self.style.text[gtk.STATE_SELECTED]
        self.MARKED_COLOR = self.style.base[gtk.STATE_SELECTED]
        self.BACKGROUND_COLOR = self.style.base[gtk.STATE_NORMAL]
        
        self.jyear=year
        self.jmonth=month
        self.jday=day
        i=1
        j=1
        tmp=[]
        while(i<7):
            while(j<8):
                tmp.append(0)
                j+=1
            self.day.append(tmp)
            self.day_mil.append(tmp)
            tmp=[]
            i+=1
            j=1
        self.holiday=holiday
        
        self.extraday=extra
        self.DATA_DIR=datadir
        self.imagelist=["balloons-2.png","marid_2.png","shabdar_2.png","cday-2.png",None]

    def do_realize(self):
        
        self.set_flags(self.flags() | gtk.REALIZED)
        
        self.window = gdk.Window(
                                 self.get_parent_window(),
                                 width=self.allocation.width,
                                 height=self.allocation.height,
                                 window_type=gdk.WINDOW_CHILD,
                                 wclass=gdk.INPUT_OUTPUT,
                                 event_mask=self.get_events() | gdk.EXPOSURE_MASK
                                 | gdk.BUTTON1_MOTION_MASK | gdk.BUTTON_PRESS_MASK
                                 | gtk.gdk.POINTER_MOTION_MASK
                                 | gtk.gdk.POINTER_MOTION_HINT_MASK
                                 )
        
        self.window.set_user_data(self)
        self.style.attach(self.window)
        self.style.set_background(self.window, gtk.STATE_NORMAL )
        self.window.move_resize(*self.allocation)
    
        self.connect("button_press_event", self.press_notify_event)
        self.connect("motion_notify_event", self.motion_notify_event)
        
    def do_expose_event(self, event):
        x, y, w, h = self.allocation

        cr = self.window.cairo_create()
        cr.set_source_color(self.MARKED_COLOR)
        cr.rectangle(BORDER_WIDTH, BORDER_WIDTH,w, self.top_margin)
        cr.fill()

        self.draw_day_name()

        cr.set_source_color(self.BACKGROUND_COLOR)
        cr.rectangle(self.basecol_width,self.top_margin,w-25, h )
        cr.fill()
        cr.set_source_color(self.MARKED_COLOR)
        cr.rectangle(w-25,0,w, h )
        cr.fill()
        
        self.compute_day()
        self.draw_week_number()
        self.draw_day_month()
        
    def do_size_request(self, requisition):
        requisition.height = self.cheight+50
        requisition.width = self.cwidth #155
        
    def draw_day_name(self):
        x, y, w, h = self.allocation
        cr = self.window.cairo_create()
        cr.set_source_color(self.SELECTED_DAY_COLOR)
        dy = 7 #self.left_margin
        i=6
        while (i>=0):
            _dayname = self.create_pango_layout(self.Dayname[i])
            _dayname.set_font_description(pango.FontDescription(self.cfont[self.size]))
            try:
                fontw, fonth = _dayname.get_pixel_size()
            except:
                fontw, fonth = _dayname.get_pixel_size()
            plus = ( (w-self.left_margin)/7 ) - (fontw+5)
            cr.move_to( (dy+(plus/4)) , (self.top_margin/2)-(fonth/2))
            cr.update_layout(_dayname)
            cr.show_layout(_dayname)
            self.basecol_width=fontw+5+(plus)
            if self.top_margin < fonth:
                self.top_margin = fonth
            dy += fontw+5+(plus)
            i-=1

    def draw_week_number(self):
        x, y, w, h = self.allocation
        cr = self.window.cairo_create()
        cr.set_source_color(self.SELECTED_DAY_COLOR)
        i=0
        year=self.jyear
        month =self.jmonth
        change =False
        dx = w -(self.left_margin/2)
        hrow=(h-self.top_margin)/6
        pulse=hrow/2
        while(i<6):
            if (i>3)and(self.day[i][6]<15)and(change==False):
                month += 1
                if month > 12 :
                    month =1
                    year +=1
                change= True
            week = week_number(year,month, self.day[i][6])
            if week==0:
                week = 53
            tmp=self.convert_to_str(week)
            _weeknum = self.create_pango_layout(tmp)
            _weeknum.set_font_description(pango.FontDescription(self.cfont[self.size]))
            fontw, fonth = _weeknum.get_pixel_size()
            cr.move_to(dx-(fontw/2)  , self.top_margin+((hrow*i)+(pulse-(fonth/2))) )
            cr.update_layout(_weeknum)
            cr.show_layout(_weeknum)
            i+=1
        #    
        #self.cheight = hh+self.top_margin
            
    def draw_day_month(self):
        x, y, w, h = self.allocation
        cr = self.window.cairo_create()
        dx = 2 #self.left_margin
        dy = self.top_margin
        sx,sy=self.current_day
        ibase = (self.basecol_width/3)
        hrow=(h-self.top_margin)/6
        ph = hrow/2
        cc=0
        i=0
        j=6
        cred=False

        while(i<6):
            while (j>=0):
                tmp=self.convert_to_str(self.day[i][j])
                _daynum = self.create_pango_layout(tmp)
                _daynum.set_font_description(pango.FontDescription(self.cfont[self.size]))
                day_x,day_y=_daynum.get_pixel_size()
                gray=False
                checkholiday=False
                if (i<2)and(self.day[i][j]>15):
                    cr.set_source_color(self.DEACTIVE_COLOR)
                    gray=True
                if (i>=4)and(self.day[i][j]<20):
                    cr.set_source_color(self.DEACTIVE_COLOR)
                    gray=True
                
                
                plus = ( (w-self.left_margin)/7 ) -(_daynum.get_pixel_size()[0]+5)
                if ((gray==False)and(holiday.holiday.has_key(self.jyear))):
                    for holi in holiday.holiday.get(self.jyear):
                        if (self.jmonth==holi[0])and(self.day[i][j]==holi[1]):
                            checkholiday = True
                            break

                customday =False
                if (gray==False):
                    cd = 0 
                    for ctmp in self.extraday:
                        if ((self.jmonth==int(ctmp[0]))and (self.day[i][j]==int(ctmp[1]))):
                            cd+=1
                            customday = True
                            cpix = ctmp[2]
                            if ctmp[2]>2:
                                cpix = 3
                            if cd>1:
                                cpix = 3
                if ((i==sx)and(j==sy))and(gray==False):
                    if (checkholiday==False):
                        cr.set_source_color(self.MARKED_COLOR)
                    else:
                        cr.set_source_color(self.RED_COLOR)
                    
                    temp = cc*self.basecol_width
                    #cr.rectangle(temp,dy-3,self.basecol_width,day_y+6)
                    cr.rectangle(temp,(hrow*i)+self.top_margin,self.basecol_width,hrow)
                    cr.fill()
                    cr.set_source_color(self.SELECTED_DAY_COLOR)
                    gray=True
                    cred=True
                if customday==True:
                    image = cairo.ImageSurface.create_from_png ( self.DATA_DIR+"/"+self.imagelist[cpix] )
                    cr.set_source_surface( image, dx, dy )
                    cr.paint()

                if ((j==6)or(checkholiday==True))and(gray==False):
                    cr.set_source_color(self.RED_COLOR)
                elif ( (((checkholiday==False))and(gray==False)) or customday==True):
                    cr.set_source_color(self.NORMAL_DAY_COLOR)
                
                cr.move_to( ((ibase)-(day_x/2))+(cc*self.basecol_width),self.top_margin+((hrow*i)+(ph-(day_y/2))))

                cr.update_layout(_daynum)
                cr.show_layout(_daynum)
                if (gray==False)or(cred==True):
                    zy,zm,zd=utility.jalali_to_milady(self.jyear,self.jmonth,self.day[i][j])
                    _daynumm = self.create_pango_layout(str(zd))
                    _daynumm.set_font_description(pango.FontDescription(self.csfont[self.size]))
                    mw, mh = _daynumm.get_pixel_size()
                    cr.set_source_color(self.DEACTIVE_COLOR)
                    if ((i==sx)and(j==sy)):
                        cr.set_source_color(self.SELECTED_DAY_COLOR)
                    cr.move_to( ((ibase*2)-(mw/2)+(cc*self.basecol_width)) , self.top_margin+((hrow*i)+(ph+(mh/4))))
                    cr.update_layout(_daynumm)
                    cr.show_layout(_daynumm)
                cred=False
                dx += day_x+5+(plus)
                cc+=1
                self.col_width[j]=dx
                j-=1

            i+=1
            j=6
            cc=0
            hh = ( ( (h-self.top_margin)/6 ) -(day_y+5) )
            dy += day_y+5+hh
            self.row_height[i-1]=dy
            dx = 0 #self.left_margin

    def convert_to_str(self,num):
        s = str(num)
        uni_c = [u'\u06f0',u'\u06f1',u'\u06f2',u'\u06f3',u'\u06f4',u'\u06f5',u'\u06f6',u'\u06f7',u'\u06f8',u'\u06f9']
        res = u""
        if len(s)>0:
            for i in s:
                res += uni_c[int(i)]
        return res
    def compute_day(self):
        pyear = year = self.jyear
        month= self.jmonth
        pmonth = month -1
        if pmonth <= 0 :
            pmonth =12
            pyear -=1
        prev_month_length = month_length[utility.leap(pyear)][pmonth]
        prev_day_week = day_of_week(pyear, pmonth, prev_month_length)
        
        current_month_length=month_length[utility.leap(year)][month]
        sc = utility.scalar_Days(self.jyear, self.jmonth, 1)
        current_day_week = utility.jalalyDate(sc)
        
        day = (prev_month_length-(current_day_week-1))

        if ( current_day_week==0):
            day=1

        i=0
        j=0
        sday = 0
        while(i<6):
            while(j<7):
                self.day[i][j]=day
                if (self.jday==day)and(sday==0):
                    self.current_day=[i,j]
                day+=1
                if (i>3)and(day>current_month_length):
                    day =1
                    sday=1

                if (i<2)and(day>prev_month_length):
                    day =1
                j+=1
            i+=1
            j=0
            
    def press_notify_event(self,obj,data):
        x,y,data=data.window.get_pointer()
        col=self.find_col(x)
        row=self.find_row(y)
        if (row>=0)and(col>=0):
            self.jday = self.day[row][col]
            self.current_day=[0,0]
            if (row==0)and(self.day[row][col]>15):
                self.jmonth -= 1
                if self.jmonth <= 0 :
                    self.jmonth =12
                    self.jyear -=1
                self.emit("month-change",self.jmonth,self.jyear)

            if (row>3)and(self.day[row][col]<15):
                self.jmonth += 1
                if self.jmonth > 12 :
                    self.jmonth =1
                    self.jyear +=1
                self.emit("month-change",self.jmonth,self.jyear)
            
            self.emit("day-change",self.jmonth,self.jyear,self.day[row][col])
            alloc = self.get_allocation()
            rect = gdk.Rectangle(0, 0, alloc.width, alloc.height)
            self.window.invalidate_rect(rect,True)
        return True
    
    def find_col(self,x):
        #if (x<self.left_margin):
         #   return -1
        col=6
        i=6
        #for i in self.col_width :
        while (i>=0):
            if (x<self.col_width[i]):
                return col
            col-=1
            i-=1
        return -1

    def find_row(self,y):
        if (y<self.top_margin):
            return -1
        row=0
        for i in self.row_height :
            if (y<i):
                return row
            row+=1
        return -1
    
    def motion_notify_event(self,obj,event):
        pass
    
    def next_month(self):
        self.jmonth += 1
        if self.jmonth > 12 :
            self.jmonth =1
            self.jyear +=1
        alloc = self.get_allocation()
        rect = gdk.Rectangle(0, 0, alloc.width, alloc.height)
        self.window.invalidate_rect(rect,True)
            
    def prev_month(self):
        self.jmonth -= 1
        if self.jmonth <= 0 :
            self.jmonth =12
            self.jyear -=1
        alloc = self.get_allocation()
        rect = gdk.Rectangle(0, 0, alloc.width, alloc.height)
        self.window.invalidate_rect(rect,True)

    def next_year(self):
        self.jyear+=1
        alloc = self.get_allocation()
        rect = gdk.Rectangle(0, 0, alloc.width, alloc.height)
        self.window.invalidate_rect(rect,True)
        
    def prev_year(self):
        self.jyear-=1
        alloc = self.get_allocation()
        rect = gdk.Rectangle(0, 0, alloc.width, alloc.height)
        self.window.invalidate_rect(rect,True)
    
    def get_month(self):
        return self.jmonth

    def get_year(self):
        return self.jyear
    
    def get_day(self):
        return self.jyear
    
    def get_cal_height(self):
        #x, y, w, h = self.allocation
        return self.cheight

gobject.signal_new("month-change",pcalendar, gobject.SIGNAL_RUN_LAST ,
                   gobject.TYPE_NONE, [gobject.TYPE_INT,gobject.TYPE_INT])
gobject.signal_new("day-change",pcalendar, gobject.SIGNAL_RUN_LAST ,
                   gobject.TYPE_NONE, [gobject.TYPE_INT,gobject.TYPE_INT,gobject.TYPE_INT])

gobject.type_register(pcalendar)
