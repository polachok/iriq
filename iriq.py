#!/usr/bin/env python

import sys
import os
import pygtk
pygtk.require('2.0')
import gtk
import gtk.glade

Settings = {}

class gui(gtk.glade.XML):
    def __init__(self):
	w = lambda x: self.wTree.get_widget(x)

	self.local_path = os.path.realpath(os.path.dirname(sys.argv[0]))
	gladefile = os.path.join(self.local_path, "iriq.glade")
	windowname = "MainWindow"
	self.wTree = gtk.glade.XML(gladefile)
	self.wTree.signal_autoconnect(self)

	# Fill the gui
	w("MainWindow").set_title("Blah")
	w("DecTiledBtn").set_active(int(Settings["Echinus*decoratetiled"]))
	w("ShowTagBarBtn").set_active(int(Settings["Echinus*tagbar"]))

    def window_destroyed(self, widget):
	gtk.main_quit()

class parser(file):
    def __init__(self, fname):
	f = open(fname, mode='r+')
	self.read(f)

    def read(self, f):
	for line in f.readlines():
	    try:
		l = line.split(':')
		Settings[l[0]] = l[1]
	    except:
		pass
	print Settings

if __name__ == "__main__":
	#par = parser(sys.argv[1])
	par = parser("echinusrc")
	app = gui()
	gtk.main()
