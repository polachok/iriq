#!/usr/bin/env python

import sys
import os
import pygtk
pygtk.require('2.0')
import gtk
import gtk.glade

Settings = {}
Lines = {}

Col = ( "fg", "bg", "border", "button" )

class gui(gtk.glade.XML):
    def active(self):
	return not self.wTree.get_widget("ActInactCbox").get_active()

    def color(self):
	s = "Echinus*" + ("selected" if self.active() else "normal") + "."
	s = s + Col[self.wTree.get_widget("ColorCbox").get_active()]
	return gtk.gdk.color_parse(Settings[s].strip())

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
	s = w.get_color().to_string()
	c = '#'+s[1:3]+s[6:8]+s[10:12]
	s = "Echinus*" + ("selected" if self.active() else "normal") + "."
	s = s + Col[self.wTree.get_widget("ColorCbox").get_active()]
	Settings[s] = c

    def redraw(self):
	w = lambda x: self.wTree.get_widget(x)
	w("ColorBtn").set_color(self.color())

    def destroy(self, widget):
	print "OLOLOO"
	par.write()
	gtk.main_quit()

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
