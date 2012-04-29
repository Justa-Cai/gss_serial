import gtk
import vte #@UnresolvedImport
import gobject
import os
import sqlite3
import sys
from serial import Serial
from bottomToolbar import BottomToolBar

class MyDlg(gtk.Window):
    def __init__(self):
        super(MyDlg, self).__init__()
        self.set_size_request(600, 480)
        self.set_position(gtk.WIN_POS_CENTER)
        self.connect("destroy", gtk.main_quit)
      
        # vbox 
        self.vbox = vbox = gtk.VBox() 
        
        # menubar
        agr = gtk.AccelGroup()
        self.add_accel_group(agr)
        
        mb = gtk.MenuBar()
        menu = gtk.Menu()
        menufile = gtk.MenuItem('_File')
        menufile.set_submenu(menu)
        
        menuitem = gtk.MenuItem('_New Connect')
        key, mod = gtk.accelerator_parse("<Control>N")
        menuitem.add_accelerator("activate", agr, key, mod, gtk.ACCEL_VISIBLE)
        menu.append(menuitem)
        
        menuitem = gtk.MenuItem('_Quit')
        key, mod = gtk.accelerator_parse("<Control><Shift>W")
        menuitem.add_accelerator("activate", agr, key, mod, gtk.ACCEL_VISIBLE)
        menuitem.connect('activate', gtk.main_quit)
        menu.append(menuitem)
        
        mb.append(menufile)
        vbox.add(mb)
        
        # vte ctrl
        self.serial = Serial(port='/dev/ttyUSB0', baudrate=115200)
        self.serial.setTimeout(0)
        gobject.io_add_watch(self.serial, gobject.IO_IN, self.OnSerialRead)
        self.terminal = vte.Terminal() 
        self.terminal.connect("commit", self.OnTerminalWrite)
        vbox.add(self.terminal)
        
        # botton toolbar
        self.toolbar = toolbar = BottomToolBar(feed_cb = self.feedTerminal)
        vbox.pack_end(toolbar)
    
        self.add(vbox) 
        self.show_all()
      
    def OnTerminalWrite(self, widget, data, size):
        if self.serial.isOpen():
            self.serial.write(data)
    
    def OnSerialRead(self, widget, condition):
        data = self.serial.read(1024)
        self.terminal.feed(data)
        return True
    
    def feedTerminal(self, data):
        if self.serial.isOpen():
            self.serial.write(data)
        
if __name__ == "__main__":
    MyDlg()
    gtk.main()
