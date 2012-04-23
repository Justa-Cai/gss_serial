import gtk
import vte #@UnresolvedImport
import gobject
import os
import sqlite3
import sys

class QuickInputData:
    """ quick input data abstract class """
    def __init__(self, caption, quicktext):
        self.quicktext = caption
        self.caption =  quicktext

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
        path = os.path.expanduser('~/.gss_serial')
        if os.path.exists(path) == False:
            os.mkdir(path)
        path = os.path.expanduser('~/.gss_serial/config.db')
        self.conn = conn = sqlite3.connect(path)
        c = conn.cursor()
        c.execute('DROP TABLE IF EXISTS DATA')
        c.execute('''CREATE TABLE IF NOT EXISTS DATA (Name TEXT, Caption TEXT, QuickText TEXT) ''')
        c.execute('''CREATE TABLE IF NOT EXISTS CONFIG (COMBOX_POS INT) ''')
        c.execute('SELECT Name FROM DATA')
        if len(c.fetchall()) == 0:
            c.execute('INSERT INTO CONFIG VALUES(0)')
            c.execute(''' INSERT INTO DATA VALUES("defaults", "1", "2") ''')
            c.execute(''' INSERT INTO DATA VALUES("defaults", "12", "2") ''')
            c.execute(''' INSERT INTO DATA VALUES("defaults", "13", "2") ''')
            c.execute(''' INSERT INTO DATA VALUES("defaultsX", "14", "2") ''')
            c.execute(''' INSERT INTO DATA VALUES("defaultsX", "1", "2") ''')
            c.execute(''' INSERT INTO DATA VALUES("defaultsX", "1", "2") ''')
            
        # GET combox pos
        c.execute('SELECT COMBOX_POS FROM CONFIG')
        self.combox_cur = c.fetchone()[0]
        
        # store tmp data into self.comboxMap
        c.execute('SELECT DISTINCT Name FROM DATA')
        for i in c.fetchall():
            # combox_text
            for j in i:
                # btn_info
                str = 'SELECT Caption,QuickText FROM DATA WHERE Name="%s"' % j
                c.execute(str)
                btn_info = [] 
                self.combox.append_text(j)
                for k in c.fetchall():
                    if len(k[0])>0 and len(k[1])>0:
                        btn_info.append(k)
                self.comboxMap[j] = btn_info               
        c.close()              
        
    def RemoveAllBtns(self):
        print "RemoveAll"
        print "!!buttons len:%d" % len(self.buttons)
        for i in self.buttons:
            self.hbox.remove(i)
            for handler in self.buttons_handlers_map[i]:
                i.disconnect(handler)
            self.buttons.remove(i)                
            i.destroy()
        
        for i in self.buttons:
            self.hbox.remove(i)
            for handler in self.buttons_handlers_map[i]:
                i.disconnect(handler)
            self.buttons.remove(i)                
            i.destroy()
        print "buttons len:%d" % len(self.buttons)
        self.buttons_handlers_map.clear()
   
    def UpdateBtns(self, value): 
        #print value
        self.quickTextMap = {}
        for i in value:
            btn = gtk.Button(i[0])
            self.quickTextMap[btn] = i[1]
            self.hbox.pack_start(btn, False, False, 0)
            self.buttons.append(btn)
            handler1 = btn.connect("button-press-event", self.OnBtnRightClick)
            handler2 = btn.connect("clicked", self.OnBtnClick)
            self.buttons_handlers_map[btn]=(handler1, handler2)
        self.hbox.show_all()
        
    def SwitchComboxPos(self, pos):
        tick=0
        for key in self.comboxMap:
            if tick == pos:
                self.RemoveAllBtns()
                self.UpdateBtns(self.comboxMap[key])
                break
            tick+=1
        
    def OnComboxChanged(self, widget):            
        self.SwitchComboxPos(self.combox.get_active())
        
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
        
    # --- end combox btn event
    
    # ---start quick btn event
    def OnBtnClick(self, widget):
        print 'OnBtnClick....'
        if self.feed_cb:
            self.feed_cb(self.quickTextMap[widget])    
        
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
        pass
        
    def OnMenuDelBtn(self, event, widget):
        # TODO:
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
        self.terminal = vte.Terminal() 
        vbox.add(self.terminal)
        # botton toolbar
        self.toolbar = toolbar = BottomToolBar()
        vbox.pack_end(toolbar)
       
        self.add(vbox) 
        self.show_all()
        
if __name__ == "__main__":
    MyDlg()
    gtk.main()
