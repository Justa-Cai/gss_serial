import gtk
import vte #@UnresolvedImport
import gobject
import os
import sqlite3
import sys
from serial import Serial

class QuickInputData:
    """ quick input data abstract class """
    def __init__(self, id, combox_id, combox_name, quick_caption, quick_text):
        self.id = id
        self.combox_id = combox_id
        self.combox_name = combox_name
        self.quick_caption = quick_caption
        self.quick_text =  quick_text 
    

class ConfigureDlg(gtk.Dialog):
    """ Configure Dialog """
    def __init__(self):
        super(ConfigureDlg, self).__init__()
        self.set_title('QuickText Set')
        
        self.set_size_request(500, 120)
        self.set_position(gtk.WIN_POS_CENTER)
        
        vbox = gtk.VBox()
        
        hbox = gtk.HBox()
        hbox.pack_start(gtk.Label('Caption:    '), False, False, 2);
        self.entry_caption = gtk.Entry()
        hbox.pack_start(self.entry_caption, True, True, 2)
        vbox.pack_start(hbox, False, False, 0);
        
        hbox = gtk.HBox()
        hbox.pack_start(gtk.Label('QuickText:'), False, False, 2);
        self.entry_quickInput = gtk.Entry()
        hbox.pack_start(self.entry_quickInput, True, True, 2)
        vbox.pack_start(hbox, False, False, 0);
        
        self.add_button("OK", gtk.RESPONSE_OK)
        self.add_button("Cancle", gtk.RESPONSE_CANCEL)
         
        self.vbox.pack_start(vbox)
        self.show_all()
        
    def GetQuickTextBtnCaption(self):
        return self.entry_caption.get_text()
    
    def GetQuickText(self):
        return self.entry_quickInput.get_text()
    
class BottomToolBar(gtk.Bin):
    def __init__(self, feed_cb=None):
        super(BottomToolBar, self).__init__()
        self.feed_cb = feed_cb
        self.buttons = []
        self.buttons_handlers_map = {}
        self.quickData = []
        self.hbox = hbox = gtk.HBox()
        
        # combox
        self.combox = combox = gtk.combo_box_new_text()
        combox.connect('changed', self.OnComboxChanged)
        #combox.connect("button-press-event", self.OnComboxRightClick)
        hbox.pack_start(combox, False, False, 0)
        
        self.hbox.show_all()
        self.add(hbox)
        self.LoadConfigData()
        self.combox.set_active(self.combox_cur)
        self.SwitchComboxPos(self.combox_cur)
    
    def LoadConfigData(self):
        self.comboxMap = {}  # comboxtext:(caption text, quicktext)
        self.combox.clear()
        path = os.path.expanduser('~/.gss_serial')
        if os.path.exists(path) == False:
            os.mkdir(path)
        path = os.path.expanduser('~/.gss_serial/config.db')
        self.conn = conn = sqlite3.connect(path)
        c = conn.cursor()
        #c.execute('DROP TABLE IF EXISTS DATA')
        c.execute('''CREATE TABLE IF NOT EXISTS DATA (id INTEGER PRIMARY KEY, pos INTEGER, Name TEXT, Caption TEXT, QuickText TEXT) ''')
        c.execute('''CREATE TABLE IF NOT EXISTS CONFIG (COMBOX_POS INTEGER) ''')
        c.execute('SELECT Name FROM DATA')
        if len(c.fetchall()) == 0:
            c.execute('INSERT INTO CONFIG VALUES(0)')
            c.execute(''' INSERT INTO DATA VALUES(NULL, 0, "defaults", "1", "21") ''')
            c.execute(''' INSERT INTO DATA VALUES(NULL, 0, "defaults", "12", "22") ''')
            c.execute(''' INSERT INTO DATA VALUES(NULL, 0, "defaults", "13", "23") ''')
            c.execute(''' INSERT INTO DATA VALUES(NULL, 1, "defaultsX", "14", "24") ''')
            c.execute(''' INSERT INTO DATA VALUES(NULL, 1, "defaultsX", "1", "25") ''')
            c.execute(''' INSERT INTO DATA VALUES(NULL, 1, "defaultsX", "1", "26") ''')
            
        # GET combox pos
        c.execute('SELECT COMBOX_POS FROM CONFIG')
        self.combox_cur = c.fetchone()[0]

        # store tmp data into self.comboxMap
        del self.quickData[:]
        c.execute('SELECT * FROM DATA')
        for i in c.fetchall():
            data = QuickInputData(i[0], i[1], i[2], i[3], i[4])
            self.quickData.append(data)
        
        for i in self.GetQuickComboxNames():
            self.combox.append_text(i)
        c.close()              
        
    def GetQuickComboxNames(self):
        data = []
        j = -1
        for item in self.quickData:
            if j != item.combox_id:
                data.append(item.combox_name)
                j = item.combox_id
        return data
    
    def GetQuickButtonsByComboxPos(self, pos):
        data = []
        for item in self.quickData:
            if item.combox_id == pos:
                data.append(item)
        return data
        
    def RemoveAllBtns(self):
        for i in self.buttons:
            self.hbox.remove(i)
            for handler in self.buttons_handlers_map[i]:
                i.disconnect(handler)
            self.buttons.remove(i)                
            i.destroy()
        
        # why can't clear list????
        for i in self.buttons:
            self.hbox.remove(i)
            for handler in self.buttons_handlers_map[i]:
                i.disconnect(handler)
            self.buttons.remove(i)                
            i.destroy()
        #print "buttons len:%d" % len(self.buttons)
        self.buttons_handlers_map.clear()
   
    def UpdateBtns(self, data): 
        self.quickTextMap = {}
        for item in data:
            btn = gtk.Button(item.quick_caption)
            self.quickTextMap[btn] = item
            self.hbox.pack_start(btn, False, False, 0)
            self.buttons.append(btn)
            handler1 = btn.connect("button-press-event", self.OnBtnRightClick)
            handler2 = btn.connect("clicked", self.OnBtnClick)
            self.buttons_handlers_map[btn]=(handler1, handler2)
        self.hbox.show_all()
        
    def SwitchComboxPos(self, pos):
        self.combox.set_active(pos)
        self.RemoveAllBtns()
        self.UpdateBtns(self.GetQuickButtonsByComboxPos(pos))
        
    # --- start combox btn event
    def OnComboxRightClick(self, widget):
        # TODO: add configure dlg
        dlg = ConfigureDlg()
        if dlg.run() == gtk.RESPONSE_OK:
            button = gtk.Button("%s" % dlg.GetQuickTextBtnCaption())
            self.hbox.pack_start(button, False, False, 0)
            self.hbox.show_all()
            self.buttons.append(button)
        dlg.destroy()
        
    def OnComboxChanged(self, widget):            
        self.SwitchComboxPos(self.combox.get_active())
        
    # --- end combox btn event
    
    # ---start quick btn event
    def OnBtnClick(self, widget):
        if self.feed_cb:
            self.feed_cb(self.quickTextMap[widget].quick_text + '\n')    
        
    def OnBtnRightClick(self, widget, event):
        if event.button == 3:
            menu = gtk.Menu()
            gtk.MenuItem('pop').set_submenu(menu)
                        
            menu_item= gtk.MenuItem('_Modify')
            menu_item.connect("activate", self.OnMenuModifyBtn, widget)
            menu.add(menu_item)
            
            menu_item = gtk.MenuItem('_Del')
            menu_item.connect('activate', self.OnMenuDelBtn, widget)
            menu.add(menu_item)
            
            menu.popup(None, None, None, event.button, event.time)
            menu.show_all()
            
    def OnMenuModifyBtn(self, event, widget):
        # TODO:
        dlg = ConfigureDlg()
        item = self.quickTextMap[widget]
        dlg.entry_caption.set_text(item.quick_caption)
        dlg.entry_quickInput.set_text(item.quick_text)
        if dlg.run() == gtk.RESPONSE_OK :
            # first update database
            if not (dlg.entry_caption.get_text_length() == 0 or dlg.entry_quickInput.get_text_length() ==0) :
                item.quick_caption = dlg.entry_caption.get_text()
                item.quick_text = dlg.entry_quickInput.get_text()
                c = self.conn.cursor()
                str = 'UPDATE DATA SET Caption="%s", QuickText="%s" WHERE id=%d' % (item.quick_caption, item.quick_text, item.id)
                print str
                c.execute(str)
                self.conn.commit() 
                c.close()
                self.LoadConfigData()
        dlg.destroy()
        pass
        
    def OnMenuDelBtn(self, event, widget):
        # TODO: remove widget and update ui
        pass
        # ---end quick btn event
        
    def do_size_request(self, req):
        (w,h) = self.hbox.size_request()
        req.width = w
        req.height = h
        
    def do_size_allocate(self, alloc):
        self.allocation = alloc
        self.hbox.size_allocate(alloc)
    
gobject.type_register(BottomToolBar) #@UndefinedVariable

class MyDlg(gtk.Window):
    def __init__(self):
        super(MyDlg, self).__init__()
        self.set_size_request(600, 480)
        self.set_position(gtk.WIN_POS_CENTER)
        self.connect("destroy", gtk.main_quit)
      
        # vbox 
        self.vbox = vbox = gtk.VBox() 
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
