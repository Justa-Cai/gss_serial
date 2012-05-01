""" 
Test gtk.Dialog

Reference:
- dialog:
  http://www.pygtk.org/docs/pygtk/class-gtkdialog.html
"""
import gtk
def CreateLable(title, width=14):
    label = gtk.Label(title)
    label.set_width_chars(width)
    return label

class QucikConnectDialg(gtk.Dialog):
    PROTOCOL_TYPE_SERIAL = 0
    PROTOCOL_TYPE_LOCAL_BASH = 1
    PROTOCOL_TYPE_SSH = 2
    
    SERIAL_BAURATE = (115200, 57600, 38400, 19200, 9600)
    SERIAL_DATA_BITS= (8, 7, 6, 5)
    def __init__(self):
        super(QucikConnectDialg, self).__init__()
        self.set_size_request(420, 320)
        self.set_position(gtk.WIN_POS_CENTER)
        self.set_title("Quick Connect...")
        vbox = self.vbox
        
        hbox = gtk.HBox()
        hbox.pack_start(CreateLable('Protocol:'), False, False)
        protocol_combox = gtk.combo_box_new_text()
        protocol_combox.append_text('Serial')
        protocol_combox.append_text('Local Bash')
        protocol_combox.append_text('SSH')
        protocol_combox.connect('changed', self.OnComboxChanged)
        
        hbox.pack_start(protocol_combox)
        
        vbox.pack_start(hbox, False, False, 5)
        
        self.add_button('Connect', gtk.RESPONSE_OK)
        self.add_button('Close', gtk.RESPONSE_CLOSE)
        
        vbox.show_all()
        self.__vbox_serial = None
        self.__vbox_local_bash = None
        self.__vbox_ssh = None
        protocol_combox.set_active(self.PROTOCOL_TYPE_LOCAL_BASH)
        
    def OnComboxChanged(self, w):
        self.CreateFrame(w.get_active())
        
    def CreateFrame(self, t):
        self.RemoveAllBox()
        if t == self.PROTOCOL_TYPE_SERIAL:
            self.CreateSerialFrame()
        elif t == self.PROTOCOL_TYPE_LOCAL_BASH:
            self.CreateLocalBashFrame()
        elif t == self.PROTOCOL_TYPE_SSH:
            self.CreateSSHFrame()
            
    def CreateSerialFrame(self):
        self.__vbox_serial = vbox = gtk.VBox()
        self.vbox.pack_start(vbox)
        
        hbox = gtk.HBox()
        hbox.pack_start(CreateLable('Port:'), False, False)
        self.__entry_port = entry_port = gtk.Entry()
        entry_port.set_text('/dev/ttyUSB0')
        hbox.pack_start(entry_port)
        vbox.pack_start(hbox, False, False)
        
        hbox = gtk.HBox()
        hbox.pack_start(CreateLable('Baurate:'), False, False)
        self.__entry_baurate= entry_baurate = gtk.Entry()
        entry_baurate.set_text('115200')
        hbox.pack_start(entry_baurate)
        vbox.pack_start(hbox, False, False)
        
        self.vbox.show_all()
        
        """
        hbox = gtk.HBox()
        hbox.pack_start(CreateLable('Baurate:'), False, False)
        self.__combox_baurate = combox_baurate = gtk.combo_box_new_text()
        for i in self.SERIAL_BAURATE:
            combox_baurate.append_text(str(i))
        combox_baurate.set_active(0)
        hbox.pack_start(combox_baurate)
        vbox.pack_start(hbox, False, False)
        
        hbox = gtk.HBox()
        hbox.pack_start(CreateLable('Data bits:'), False, False)
        self.__combox_data_bits = combox_data_bits= gtk.combo_box_new_text()
        for i in self.SERIAL_DATA_BITS:
            combox_data_bits.append_text(str(i))
        combox_data_bits.set_active(0)
        hbox.pack_start(combox_data_bits)
        vbox.pack_start(hbox, False, False)
        
        hbox = gtk.HBox()
        hbox.pack_start(CreateLable('Parity:'), False, False)
        self.__combox_data_bits = combox_data_bits= gtk.combo_box_new_text()
        combox_data_bits.set_active(0)
        hbox.pack_start(combox_data_bits)
        vbox.pack_start(hbox, False, False)
        
        hbox = gtk.HBox()
        hbox.pack_start(CreateLable('Stop Bits:'), False, False)
        self.__combox_data_bits = combox_data_bits= gtk.combo_box_new_text()
        combox_data_bits.set_active(0)
        hbox.pack_start(combox_data_bits)
        vbox.pack_start(hbox, False, False)
        """
        
        
    def CreateLocalBashFrame(self):
        self.__vbox_local_bash = vbox = gtk.VBox()
        self.vbox.pack_start(vbox)
        
        vbox.add(gtk.Label('Not Need params'))
        
        self.vbox.show_all()
        pass
    
    def CreateSSHFrame(self):
        self.__vbox_ssh = vbox = gtk.VBox()
        self.vbox.pack_start(vbox)
        
        hbox = gtk.HBox()
        hbox.pack_start(CreateLable('Host:'), False, False)
        self.__entry_host = entry_host =  gtk.Entry()
        hbox.pack_start(entry_host)
        vbox.pack_start(hbox, False, False)
        
        hbox = gtk.HBox()
        hbox.pack_start(CreateLable('User:'), False, False)
        self.__entry_username = entry_username =  gtk.Entry()
        hbox.pack_start(entry_username)
        vbox.pack_start(hbox, False, False)
        
        self.vbox.show_all()
    
    def RemoveAllBox(self):
        if self.__vbox_serial:
            self.vbox.remove(self.__vbox_serial)
        if self.__vbox_local_bash:
            self.vbox.remove(self.__vbox_local_bash)
        if self.__vbox_ssh:
            self.vbox.remove(self.__vbox_ssh)
            
        self.__vbox_serial = None
        self.__vbox_local_bash = None
        self.__vbox_ssh = None
        
    
class ConnectDialog(gtk.Dialog):        
    def __init__(self):
        super(ConnectDialog, self).__init__()
        self.set_size_request(420, 320)
        self.set_position(gtk.WIN_POS_CENTER)
        self.set_title("Connect...")
        vbox = self.vbox
        
        store = gtk.TreeStore(str, str, str)
        it = store.append(None, ["History", "", ""])
        store.append(it, ["Serial", "port", "baurate"])
        store.append(it, ["SSH", "host", "user"])
        store.append(it, ["HOST", "", ""])
        
        self.__treeview = treeview =  gtk.TreeView()
        treeview.append_column(gtk.TreeViewColumn("History", gtk.CellRendererText(), text=0))
        treeview.set_model(store)
        treeview.expand_all()
        treeview.connect('row-activated', self.OnTreeViewOnActivated)
        vbox.add(treeview)
        
        self.add_button('Connect', gtk.RESPONSE_OK)
        self.add_button('Close', gtk.RESPONSE_CLOSE)
        vbox.show_all()
        
    def OnTreeViewOnActivated(self, widget, path, col):
        model = widget.get_model()
        iter = model.get_iter(path)
        print model.get_value(iter, 0)
        
class TestDlg(gtk.Window):
    
    def __init__(self):
        super(TestDlg, self).__init__()
        self.set_size_request(600, 480)
        self.set_position(gtk.WIN_POS_CENTER)
        self.connect("destroy", gtk.main_quit)
        self.set_title("Test Tree View")
        
        self.vbox = vbox = gtk.VBox()

        # menu
        agr = gtk.AccelGroup()
        self.add_accel_group(agr)
        
        mb = gtk.MenuBar()
        menu = gtk.Menu()
        menufile = gtk.MenuItem('_File')
        menufile.set_submenu(menu)
        mb.append(menufile)
        vbox.pack_start(mb, False, False)
        
        menuitem = gtk.MenuItem('Quit')
        key, mod = gtk.accelerator_parse("<Control>W")
        menuitem.add_accelerator("activate", agr, key, mod, gtk.ACCEL_VISIBLE)
        menuitem.connect('activate', gtk.main_quit)
        menu.append(menuitem)
        
        menuitem = gtk.MenuItem('_Quick Connect')
        key, mod = gtk.accelerator_parse("<Alt>Q")
        menuitem.add_accelerator("activate", agr, key, mod, gtk.ACCEL_VISIBLE)
        menuitem.connect('activate', self.OnQucikConnectDlg)
        menu.append(menuitem)
        
        menuitem = gtk.MenuItem('_Connect')
        key, mod = gtk.accelerator_parse("<Alt>C")
        menuitem.add_accelerator("activate", agr, key, mod, gtk.ACCEL_VISIBLE)
        menuitem.connect('activate', self.OnConnectDlg)
        menu.append(menuitem)
        self.add(vbox)
        self.show_all()
        
    def OnQucikConnectDlg(self, w):
        dlg = QucikConnectDialg()
        print 'ret:', dlg.run() 
        dlg.destroy()
        pass
    
    def OnConnectDlg(self, w):
        dlg = ConnectDialog()
        print 'ret:', dlg.run() 
        dlg.destroy()
        pass


if __name__ == '__main__':
    TestDlg()
    gtk.main()