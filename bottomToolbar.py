import gtk
import os
import sqlite3
import sys
import gobject

from utils import *


class QuickInputData:
    """ quick input data abstract class """
    def __init__(self, id, combox_id, combox_name, quick_caption, quick_text):
        self.id = id
        self.combox_id = combox_id
        self.combox_name = combox_name
        self.quick_caption = quick_caption
        self.quick_text =  quick_text

class ConfigureNewToolbarDlg(gtk.Dialog):
    """ ConfigureNewToolbarDlg"""
    def __init__(self):
        super(ConfigureNewToolbarDlg, self).__init__()
        self.set_title('Add New toolbar')

        self.set_size_request(300, 100)
        self.set_position(gtk.WIN_POS_CENTER)

        vbox = gtk.VBox()

        hbox = gtk.HBox()
        hbox.pack_start(gtk.Label('Toolbar Name:    '), False, False, 2);
        self.entry_toolbarName = gtk.Entry()
        hbox.pack_start(self.entry_toolbarName, True, True, 2)
        vbox.pack_start(hbox, False, False, 0);

        self.add_button("OK", gtk.RESPONSE_OK)
        self.add_button("Cancle", gtk.RESPONSE_CANCEL)

        self.vbox.pack_start(vbox)
        self.show_all()

    def GetToolbarName(self):
        return self.entry_toolbarName.get_text()
    
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
        # TODO: why combox can't emit button-press-event
        #combox.connect("button-press-event", self.OnComboxRightClick)
        #combox.set_events(gtk.gdk.BUTTON_PRESS_MASK)
        hbox.pack_start(combox, False, False, 0)

        self.hbox.show_all()
        self.add(hbox)
        self.LoadConfigData()
        self.combox.set_active(self.combox_cur)

        self.SwitchComboxPos(self.combox_cur)

    def ClearComboxData(self):
        self.combox.get_model().clear()

    def LoadConfigData(self):
        #self.combox.clear()
        self.ClearComboxData()

        #path = os.path.expanduser('~/.gss_serial/config.db')
        #self.conn = conn = sqlite3.connect(path)
        self.conn = conn = GetDataUtils().GetConnect()
        c = conn.cursor()
        #c.execute('DROP TABLE IF EXISTS DATA')
        """
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
        """
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
            self.combox.append_text(i.combox_name)

        self.combox.append_text(".....")
        c.close()
        self.SwitchComboxPos(self.combox_cur)

    def GetQuickComboxNames(self):
        data = []
        m = {}
        j = -1
        for item in self.quickData:
            if j != item.combox_id and  not m.has_key(item.combox_id):
                data.append(item)
                j = item.combox_id
                m[j] = True
        return data

    def GetQuickButtonsByComboxPos(self, pos):
        data = []
        for item in self.quickData:
            if item.combox_id == pos:
                data.append(item)
        return data

    def GetQuickComboxIdFree(self):
        data = self.GetQuickComboxNames()
        j = 0
        num = []
        for i in data:
            num.append(i.combox_id)
        s = set(num)

        while True:
            if j not in s:
                return j
            else:
                j+=1


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
        pos_store = self.GetQuickComboxNames()[pos].combox_id
        self.UpdateBtns(self.GetQuickButtonsByComboxPos(pos_store))
        #self.UpdateBtns(self.GetQuickButtonsByComboxPos(pos))

    # --- start combox btn event
    def OnComboxRightClick(self, widget):
        # TODO: check why combox cant't receive 'button-press-event'
        dlg = ConfigureNewToolbarDlg()
        if dlg.run() == gtk.RESPONSE_OK and len(dlg.GetToolbarName())>0:
            c = self.conn.cursor()
            #pos = len(self.combox.get_model()) - 1
            pos = self.GetQuickComboxIdFree()
            str = 'INSERT INTO DATA VALUES(NULL, %d, "%s", "", "")' % (pos, dlg.GetToolbarName())
            c.execute(str)
            self.conn.commit()
            c.close()
            self.combox_cur = 0
            self.LoadConfigData()
        dlg.destroy()

    def OnComboxChanged(self, widget):
        pos = self.combox.get_active()
        if pos == -1:
            return

        max_pos = len(self.combox.get_model())
        if max_pos -1 == pos:
            self.OnComboxRightClick(None)
            self.combox.set_active(self.combox_cur_old)
            return True

        self.SwitchComboxPos(pos)
        self.combox_cur = self.combox.get_active()
        c = self.conn.cursor()
        str = 'UPDATE CONFIG SET COMBOX_POS=%d ' % self.combox_cur
        c.execute(str)
        self.conn.commit()
        c.close()
        self.combox_cur_old = self.combox_cur

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

            menu_item = gtk.MenuItem('Add Toolbar')
            menu_item.connect('activate', self.OnMenuAddToolbar, widget)
            menu.add(menu_item)

            menu_item = gtk.MenuItem('Del Toolbar')
            menu_item.connect('activate', self.OnMenuDelToolbar, widget)
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
                c.execute(str)
                str = 'UPDATE CONFIG SET COMBOX_POS=%d ' % self.combox_cur
                c.execute(str)
                self.conn.commit()
                c.close()
                self.LoadConfigData()
        dlg.destroy()
        pass

    def OnMenuDelBtn(self, event, widget):
        # TODO: remove widget and update ui
        item = self.quickTextMap[widget]
        c = self.conn.cursor()
        str = 'DELETE FROM DATA WHERE id=%d' % item.id
        c.execute(str)
        self.conn.commit()
        c.close()
        self.LoadConfigData()

    def OnMenuAddToolbar(self, event, widget):
        self.OnComboxRightClick(None)

    def OnMenuDelToolbar(self, event, widget):
        # TODO: remove widget and update ui
        item = self.quickTextMap[widget]
        c = self.conn.cursor()
        str = 'DELETE FROM DATA WHERE pos=%d' % item.combox_id
        c.execute(str)
        self.conn.commit()
        c.close()
        self.combox.set_active(0)
        self.LoadConfigData()
    # ---end quick btn event

    def do_size_request(self, req):
        (w,h) = self.hbox.size_request()
        req.width = w
        req.height = h

    def do_size_allocate(self, alloc):
        self.allocation = alloc
        self.hbox.size_allocate(alloc)

gobject.type_register(BottomToolBar) #@UndefinedVariable

