#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import pygtk
pygtk.require('2.0')
import gtk
import cairo
import gtk.glade

Settings = {}
Lines = {}

Col = [ "fg", "bg", "border", "button" ]

class gui(gtk.glade.XML):
    def active(self):
	return not self.wTree.get_widget("ActInactCbox").get_active()

    def getcolor(self, sel, which):
	s = "Echinus*" + ("selected" if sel else "normal") + "."
	s = s + Col[which]
	return gtk.gdk.color_parse(Settings[s].strip())

    def color(self):
	return self.getcolor(self.active(), self.wTree.get_widget("ColorCbox").get_active())

    def checkbutton(self, w, s):
	Settings[s] = int(w.get_active())

    def fontbutton(self, w, s):
	# XXX: Fix bold italic and so
	Settings[s] = w.get_font_name().replace(' ', '-')
	print Settings[s]

    def actinactcbox(self, w, s):
	self.redraw()
	print w.get_active_text()

    def colorcbox(self, w, s):
	self.redraw()
	print w.get_active()
	print w.get_active_text()

    def colorbtn(self, w):
	self.redraw()
	s = w.get_color().to_string()
	c = '#'+s[1:3]+s[6:8]+s[10:12]
	s = "Echinus*" + ("selected" if self.active() else "normal") + "."
	s = s + Col[self.wTree.get_widget("ColorCbox").get_active()]
	Settings[s] = c

    def redraw(self):
	w = lambda x: self.wTree.get_widget(x)
	w("ColorBtn").set_color(self.color())

    def destroy(self, widget):
	par.write()
	gtk.main_quit()

    def redraw_preview(self, w, e):
	c = lambda x: self.getcolor(self.active, Col.index(x))
	width, height = w.window.get_size()
	cr = w.window.cairo_create()
	#cr.set_source_rgb(1.0, 1.0, 1.0)
	cr.set_source_color(c("bg"))
	cr.rectangle(e.area.x, e.area.y,
		e.area.width, e.area.height)
	cr.clip()
	# background
	cr.set_source_color(c("bg"))
	#cr.set_source_rgb(1.0, 1.0, 1.0)
	cr.rectangle(0, 0, width, height)
	cr.fill()
	# draw a rectangle
	cr.set_source_rgb(1.0, 1.0, 1.0)
	cr.rectangle(10, 10, width - 20, height - 20)
	cr.fill()
	cr.translate(20, 20)
	cr.scale((width - 40) / 1.0, (height - 40) / 1.0)
	# window
	#cr.set_line_width(0.01)
	cr.set_line_width(max(cr.device_to_user_distance(2, 2)))
	#cr.set_source_rgb(0.0, 0.0, 0.8)
	cr.set_source_color(c("bg"))
	cr.move_to(0, 0)
	cr.rectangle(0, 0, 1, 0.1)
	cr.fill()
	cr.set_source_color(c("border"))
	cr.move_to(0, 0)
	cr.rectangle(0, 0, 1, 1)
	cr.stroke()
	# text
	cr.set_source_color(c("fg"))
	cr.select_font_face("Georgia",
	cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
	cr.set_font_size(0.08)
	x_bearing, y_bearing, width, height = cr.text_extents("хуй")[:4]
	cr.move_to(0.01, 0.1-height/1-y_bearing)
	cr.show_text("хуй")

    def __init__(self):
	w = lambda x: self.wTree.get_widget(x)

	self.local_path = os.path.realpath(os.path.dirname(sys.argv[0]))
	gladefile = os.path.join(self.local_path, "iriq.glade")
	windowname = "MainWindow"
	self.wTree = gtk.glade.XML(gladefile)
	self.wTree.signal_autoconnect(self)

	# Fill the gui
	w("MainWindow").set_title("Blah")
	w("MainWindow").connect("destroy", self.destroy)

	w("DecTiledBtn").set_active(int(Settings["Echinus*decoratetiled"]))
	w("DecTiledBtn").connect("toggled", self.checkbutton, "Echinus*decoratetiled")

	w("ShowTagBarBtn").set_active(int(Settings["Echinus*tagbar"]))
	w("ShowTagBarBtn").connect("toggled", self.checkbutton, "Echinus*tagbar")

	w("FontSelectorBtn").set_font_name(Settings["Echinus*font"].replace('-', ' '))
	w("FontSelectorBtn").connect("font-set", self.fontbutton, "Echinus*font")

	w("ActInactCbox").set_active(0)
	w("ActInactCbox").connect("changed", self.actinactcbox, "Blah")

	w("ColorCbox").set_active(0)
	w("ColorCbox").connect("changed", self.colorcbox, "Blah")

	w("ColorBtn").set_color(self.color())
	w("ColorBtn").connect("color-set", self.colorbtn)

	w("PreviewArea").connect("expose-event", self.redraw_preview)


class parser(file):
    def __init__(self, fname):
	f = open(fname, mode='r+')
	self.read(f)

    def read(self, f):
	global Settings
	global Lines
	# len(x) > 1 is not correct, strips empty lines
	Settings = dict(filter(lambda x: len(x)>1, map(lambda x: x.strip().split(':'), f.readlines())))
	f.seek(0)
	j = 0
	for i in f:
	    t = i.strip().split(':')
	    if len(t) > 1:
		Lines[j] = t[0]
		j = j+1
	Lines.keys().sort()

    def write(self):
	t = open("test", mode='w')
	for i in Lines:
	    t.write(Lines[i]+': '+Settings[Lines[i]]+'\n')


if __name__ == "__main__":
	#par = parser(sys.argv[1])
	par = parser("echinusrc")
	app = gui()
	gtk.main()
