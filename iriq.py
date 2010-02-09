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
	name, space, size = w.get_font_name().rpartition(" ")
	Settings[s] = name+"-"+size
	self.redraw()

    def font(self):
	name, size = Settings['Echinus*font'].split('-')
	return name, float(size)

    def actinactcbox(self, w, s):
	self.redraw()

    def colorcbox(self, w, s):
	self.redraw()

    def colorbtn(self, w):
	sl = w.get_color().to_string()
	c = '#'+sl[1:3]+sl[5:7]+sl[9:11]
	s = "Echinus*" + ("selected" if self.active() else "normal") + "."
	s = s + Col[self.wTree.get_widget("ColorCbox").get_active()]
	Settings[s] = c
	self.redraw()

    def redraw(self):
	w = lambda x: self.wTree.get_widget(x)
	w("ColorBtn").set_color(self.color())
	self.preview_expose(w("PreviewArea"))

    def destroy(self, widget):
	par.write()
	gtk.main_quit()

    def preview_expose(self, w, e=None):
	width, height = w.window.get_size()
	cr = w.window.cairo_create()
	if e != None:
	    cr.rectangle(e.area.x, e.area.y,
		    e.area.width, e.area.height)
	    cr.clip()
	else:
	    cr.rectangle(0, 0,
		    width, height)
	    cr.clip()
	self.preview_redraw(cr, width, height)

    def preview_redraw(self, cr, width, height):
	c = lambda x: self.getcolor(self.active(), Col.index(x))
	# background
	cr.set_source_rgb(0.0, 0.0, 0.0)
	cr.rectangle(0, 0, width, height)
	cr.fill()
	# window
	cr.set_line_width(max(cr.device_to_user_distance(1, 1)))
	cr.set_source_color(c("bg"))
	cr.move_to(0, 0)
	cr.rectangle(10, 10, width-20, height-20)
	cr.fill()
	# border
	cr.set_source_color(c("border"))
	cr.move_to(0, 0)
	cr.rectangle(10, 10, width-20, height-20)
	cr.stroke()
	# text
	cr.set_source_color(c("fg"))
	cr.select_font_face(self.font()[0],
	cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
	cr.set_font_size(self.font()[1])
	x_bearing, y_bearing, width, height = cr.text_extents("хуй")[:4]
	cr.move_to(15, 20)
	cr.show_text("хуй")

    def tag_selector_init(self, w):
	n = int(Settings["Echinus*tags.number"])
	for i in range(0, n-1):
	    w.append_text("Tag "+str(i)+": "+Settings["Echinus*tags.name"+str(i)].strip())

    def tagselectcbox(self, wi, s):
	w = lambda x: self.wTree.get_widget(x)
	if wi.get_active() > 0:
	    w("TagNameEntry").set_visibility(True)
	    w("TagNameEntry").set_text(Settings["Echinus*tags.name"+str(wi.get_active()-1)].strip())
	    w("TagNameEntry").show()
	    w("TagNameLabel").show()
	else:
	    w("TagNameEntry").set_visibility(False)
	    w("TagNameEntry").hide()
	    w("TagNameLabel").hide()

    def tagnameentry(self, wi, e):
	w = lambda x: self.wTree.get_widget(x)
	n = w("TagSelectCbox").get_active()
	Settings["Echinus*tags.name"+str(n-1)] = wi.get_text()
	w("TagSelectCbox").remove_text(n)
	w("TagSelectCbox").insert_text(n, "Tag "+str(n-1)+": "+Settings["Echinus*tags.name"+str(n-1)])
	print wi.get_text()

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

	w("PreviewArea").connect("expose-event", self.preview_expose)

	# Tags & rules page
	self.tag_selector_init(w("TagSelectCbox"))
	w("TagSelectCbox").connect("changed", self.tagselectcbox, "Blah")
	w("TagSelectCbox").set_active(0)
	w("TagNameEntry").connect("focus-out-event", self.tagnameentry)

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
