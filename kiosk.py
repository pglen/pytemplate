#!/usr/bin/env python3

import os, sys, getopt, signal, select, socket, time, struct
import random, stat, warnings

sys.path.append('guilib')
from mainwin import  *

from pyvguicom import comline
from pyvguicom import custwidg

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GObject
from gi.repository import GLib
from gi.repository import Pango

gi.require_version('PangoCairo', '1.0')
from gi.repository import PangoCairo

warnings.simplefilter("default")

# Step screen gloals
class  Switcher:
    screenarr = []
    gl_cnt = 0
    gl_curr = 0
    kw = None

# ------------------------------------------------------------------------
# Globals

version = "0.00"

# ------------------------------------------------------------------------

def phelp():

    comline.phelplong()
    sys.exit(0)

# ------------------------------------------------------------------------
def pversion():
    print( os.path.basename(sys.argv[0]), "Version", version)
    sys.exit(0)

    # option, var_name, initial_val, function, help
optarr = [\
    ["d:",  "debug=",   "pgdebug",  0,      None,     "Debug level. 0=none 10=noisy. Default: 0" ],
    ["l:",  "load",     "load",     "",     None,     "Load file on startup."],
    ["v",   "verbose",  "verbose",  0,      None,     "Verbose. Show more info."],
    ["q",   "quiet",    "quiet",    0,      None,     "Quiet. Show less info."],
    ["f",   "fullscr",  "fullscr",  0,      None,     "Start full screen."],
    ["V",   "version",  None,       None,   pversion, "Print Version string."],
    ["h",   "help",     None,       None,   phelp,    "Show Help. (this screen)"],
    ]

#comline.setprog("Usage: template.py [options]")
comline.sethead("Kiosk GUI for pykiosk language")
comline.setargs("[options]")
comline.setfoot("")
conf = comline.ConfigLong(optarr)

#conf.printvars()

class KioskWin(custwidg.SimpleWidget):

    def __init__(self):
        super().__init__()
        self.arrarr = []
        self.arrarr.append([])

    def fontsize(self, sizex):
        self.fd.set_absolute_size(sizex * self.stepy * Pango.SCALE)
        self.layout.set_font_description(self.fd)

    def do_draw(self, cr):
        allocation = self.get_allocation()

        self.stepx = allocation.width // 64
        self.stepy = allocation.height // 64

        if self.cnt == 0:
            self.layout = PangoCairo.create_layout(cr)
            self.cnt += 1

        bg_color = Gdk.RGBA(.80, .80, .80)
        cr.set_source_rgba(*list(bg_color));
        cr.rectangle(0, 0, allocation.width, allocation.height)

        text = "pyKiosk"
        self.fontsize(allocation.width / self.stepy / 5 )
        self.layout.set_text(text) # %d" % self.cnt)
        sss = self.layout.get_size()
        #print("sss", sss[0] / Pango.SCALE, sss[1] / Pango.SCALE )
        xxx = allocation.width  / 2 - (sss[0] / 2) / Pango.SCALE
        yyy = allocation.height / 2 - (sss[1] / 2) / Pango.SCALE

        cr.move_to(xxx, yyy)
        fg_color = Gdk.RGBA(.83, .83, .83)
        cr.set_source_rgba(*list(fg_color));
        PangoCairo.show_layout(cr, self.layout)
        self.renderscreen(cr)

    def rect2pos(self, cr, fg_color, www, hhh, xxx, yyy):
        cr.set_line_width(1)
        cr.set_source_rgba(*list(fg_color))
        cr.rectangle(self.stepx * xxx, self.stepy * yyy,
                       self.stepx * www, self.stepy * hhh)
        cr.stroke()
        cr.rectangle(self.stepx * xxx, self.stepy * yyy,
                       self.stepx * www, self.stepy * hhh)
        cr.fill()

    def line2pos(self, cr, fg_color, www, xxx, yyy, lenx):
        cr.set_source_rgba(*list(fg_color))
        cr.set_line_width(www)
        cr.move_to(self.stepx * xxx, self.stepy * yyy)
        cr.line_to(self.stepx * (xxx +  lenx), self.stepy * yyy )
        cr.stroke()

    def text2pos(self, cr, fg_color, tsize, xxx, yyy, text):
        #print(fg_color, tsize, xxx, yyy, text)
        self.fontsize(tsize)
        self.layout.set_font_description(self.fd)
        cr.move_to(xxx * self.stepx, yyy * self.stepy)
        cr.set_source_rgba(*list(fg_color))
        self.layout.set_text(text)
        PangoCairo.show_layout(cr, self.layout)

    def renderscreen(self, cr):

        cc = Switcher.gl_curr
        for aa in self.arrarr[cc]:
            try:
                if aa[0] == 0:
                    self.text2pos(cr, *aa[1:])
                if aa[0] == 1:
                    self.line2pos(cr, *aa[1:])
                if aa[0] == 2:
                    self.rect2pos(cr, *aa[1:])
            except:
                print("render:", aa, sys.exc_info())

    def reload(self, butt):
        load(self)

def demo():

    #print("load")
    # cr, fg_color, tsize, xxx, yyy, text
    fg_color = Gdk.RGBA(.2, .2, .2)
    bg_color = Gdk.RGBA(.75, .75, .75)
    bg_color2 = Gdk.RGBA(.85, .85, .85)

    #kw.arrarr[0].append((0, fg_color, 5, 1,  0,  "Column 1"))
    #kw.arrarr[0].append((0, fg_color, 5, 20, 0,  "Column 2"))
    #kw.arrarr[0].append((0, fg_color, 4, 35, 0,  "Column 3"))
    #kw.arrarr[0].append((0, fg_color, 4, 45, 0,  "Column 4"))
    #kw.arrarr[0].append((0, fg_color, 4, 56, 0,  "Column 5"))
    #
    #kw.arrarr[0].append((1, fg_color, 2, 1, 6, 64))
    #
    #kw.arrarr[0].append((2, bg_color, 64, 5, 1, 8))
    #kw.arrarr[0].append((2, bg_color2, 64, 5, 1, 14))
    #kw.arrarr[0].append((2, bg_color, 64, 5, 1, 20))
    #
    #kw.arrarr[0].append((0, fg_color, 3, 2,  9,  "Another"))
    #kw.arrarr[0].append((0, fg_color, 3, 20, 9,  "One"))
    #kw.arrarr[0].append((0, fg_color, 3, 35, 9,  "Bytes"))
    #kw.arrarr[0].append((0, fg_color, 3, 45, 9,  "The"))
    #kw.arrarr[0].append((0, fg_color, 3, 56, 9,  "Dust"))
    #
    #kw.arrarr[0].append((0, fg_color, 3, 2,  15,  "Another"))
    #kw.arrarr[0].append((0, fg_color, 3, 20, 15,  "One"))
    #kw.arrarr[0].append((0, fg_color, 3, 35, 15,  "Bytes"))
    #kw.arrarr[0].append((0, fg_color, 3, 45, 15,  "The"))
    #kw.arrarr[0].append((0, fg_color, 3, 56, 15,  "Dust"))
    #
    #kw.arrarr[0].append((0, fg_color, 3, 2,  21,  "Another"))
    #kw.arrarr[0].append((0, fg_color, 3, 20, 21,  "One"))
    #kw.arrarr[0].append((0, fg_color, 3, 35, 21,  "Bytes"))
    #kw.arrarr[0].append((0, fg_color, 3, 45, 21,  "The"))
    #kw.arrarr[0].append((0, fg_color, 3, 56, 21,  "Dust"))

def load(kw, fname = None):

    Switcher.screenarr = []

    global gl_fname
    if fname:
        gl_fname = fname

    if conf.verbose:
        print("loading", fname)
    try:
        if gl_fname[-3:] == ".gz":
            #print('zip', fname)
            import gzip
            fp = gzip.open(gl_fname, "rt")
        else:
            fp = open(gl_fname)
        data = fp.read()
        fp.close()
        data2 = data.split("\n")
        #print("data2", data2)
        for linex in data2:
            if not linex:
                continue
            if linex[0] == '#':
                continue
            #print("line: '" + linex + "'")
            line = linex.strip()
            try:
                line2 = line.split(",")
            except:
                line2 = line
                pass
            # Clean up
            for aa in range(len(line2)):
                line2[aa] = line2[aa].strip()
                try:
                    line2[aa] = int(line2[aa])
                except:
                    pass
            #print(line2)
            # Parse entries
            if line2[0] == "screen":
                #print("screen", line2)
                Switcher.screenarr.append(line2)
                kw.arrarr.append([])
                Switcher.gl_curr = line2[1]
            else:
                carr = line2[1].split(":")
                line2[1] = Gdk.RGBA( \
                       float(carr[0]), float(carr[1]), float(carr[2]) )
                try:
                    if line2[0] == 0:
                        line2[5] = line2[5][1:-1]
                except:
                    pass
                kw.arrarr[0].append(line2)
        if conf.verbose > 1:
            print(kw.arrarr[0])
        if conf.verbose:
            print(Switcher.screenarr)

        Switcher.gl_curr = 0
        Switcher.kw.queue_draw()
    except:
        print(sys.exc_info())
        fg_color = Gdk.RGBA(.2, .2, .2)
        kw.arrarr[0].append((0, fg_color, 8, 10, 21,  "Cannot Load File"))
    kw.queue_draw()

def timer():

    #print("timer", Switcher.gl_cnt, screenarr)
    cc = Switcher.gl_curr
    sa = Switcher.screenarr
    if Switcher.gl_cnt % sa[cc][2] == sa[cc][2] - 1:
        Switcher.gl_cnt = 0
        Switcher.gl_curr += 1
        if Switcher.gl_curr >= len(sa):
            Switcher.gl_curr = 0
        print("chscr", Switcher.gl_curr)
        Switcher.kw.queue_draw()

    Switcher.gl_cnt += 1
    return True

if __name__ == '__main__':

    args = conf.comline(sys.argv[1:])
    Switcher.kw = KioskWin()
    mw = MainWin(Switcher.kw, conf)
    if conf.load:
        #"demo.kiosk"
        load(Switcher.kw, conf.load)
    GLib.timeout_add(1000, timer)
    mw.run()
    #sys.exit(0)

# EOF