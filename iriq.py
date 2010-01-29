#!/usr/bin/env python

import sys
import os
import pygtk
pygtk.require('2.0')
import gtk
import gtk.glade

class gui(gtk.glade.XML):
    def __init__(self):
	self.local_path = os.path.realpath(os.path.dirname(sys.argv[0]))
	gladefile = os.path.join(self.local_path, "iriq2.glade")
	windowname = "MainWindow"
	self.wTree = gtk.glade.XML(gladefile)
	self.wTree.signal_autoconnect(self)
	self.main_window = self.wTree.get_widget("MainWindow")
	self.main_window.set_title("Blah")
	self.main_notebook = self.wTree.get_widget("MainNotebook")
	print self.main_notebook.get_current_page()
	self.applabel = self.wTree.get_widget("AppLabel")
	print self.applabel
	self.applabel = self.wTree.get_widget("HotkeysLabel")
	print self.applabel
	self.applabel = self.wTree.get_widget("RulesLabel")
	print self.applabel
	self.main_notebook.set_current_page(0)
    def window_destroyed(self, widget):
	gtk.main_quit()

if __name__ == "__main__":
    app = gui()
    gtk.main()
