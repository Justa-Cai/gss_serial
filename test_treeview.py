""" 
Test gtk.TreeView

Reference:
- TreeView,TreeModel,ListStore
  http://www.pygtk.org/docs/pygtk/class-gtktreeview.html
  http://www.pygtk.org/docs/pygtk/class-gtktreemodel.html 
  http://www.pygtk.org/docs/pygtk/class-gtkliststore.html
  http://www.pygtk.org/docs/pygtk/class-gtktreestore.html
"""
import gtk

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
        
        menuitem = gtk.MenuItem('_Quit')
        key, mod = gtk.accelerator_parse("<Control>W")
        menuitem.add_accelerator("activate", agr, key, mod, gtk.ACCEL_VISIBLE)
        menuitem.connect('activate', gtk.main_quit)
        menu.append(menuitem)
        
        menuitem = gtk.MenuItem('_Listbox')
        key, mod = gtk.accelerator_parse("<Control>L")
        menuitem.add_accelerator("activate", agr, key, mod, gtk.ACCEL_VISIBLE)
        menuitem.connect('activate', self.OnTestListbox)
        menu.append(menuitem)

        menuitem = gtk.MenuItem('_Treeview')
        key, mod = gtk.accelerator_parse("<Control>T")
        menuitem.add_accelerator("activate", agr, key, mod, gtk.ACCEL_VISIBLE)
        menuitem.connect('activate', self.OnTestTreeView)
        menu.append(menuitem)

        self.listview = listview =  gtk.TreeView()
        listview.connect('row-activated', self.OnListViewOnActivated)
        
        vbox.pack_start(mb, False, False)
        vbox.pack_start(listview)
        self.add(vbox)
        self.show_all()
        
        
    def OnTestListbox(self, event):
        self.ClearColumns()
        store = gtk.ListStore(str, str, str)
        store.append(['col1', 'col2fdsf', 'col3'])
        store.append(['col1fdsf', 'col2', 'col3'])
        store.append(['col1', 'col2', 'col3fdsfs'])
        store.append(['col1', 'col2', 'col3'])
        store.append(['col1', 'col2', 'col3'])
        
        
        listview = self.listview 
        column = gtk.TreeViewColumn("COL1", gtk.CellRendererText(), text=0)
        column.set_sort_column_id(-1)
        listview.append_column(column)
        
        column = gtk.TreeViewColumn("COL2", gtk.CellRendererText(), text=1)
        column.set_sort_column_id(0)
        listview.append_column(column)
        
        column = gtk.TreeViewColumn("COL3", gtk.CellRendererText(), text=2)
        column.set_sort_column_id(0)
        listview.append_column(column)
        
        listview.set_model(store)
        listview.show_all()
    
    def OnTestTreeView(self, event):
        self.ClearColumns()
        
        store = gtk.TreeStore(str)
        it = store.append(None, ["Tree1"])
        store.append(it, ["T1"])
        store.append(it, ["T1"])
        store.append(it, ["T1"])
        store.append(it, ["T1"])
        store.append(it, ["T1"])
        
        it = store.append(None, ["Tree2"])
        store.append(it, ["T1"])
        store.append(it, ["T1"])
        store.append(it, ["T1"])
        store.append(it, ["T1"])
        store.append(it, ["T2"])
        
        listview = self.listview 
        column = gtk.TreeViewColumn("Test", gtk.CellRendererText(), text=0)
        column.set_sort_column_id(-1)
        listview.append_column(column)
        
        listview.set_model(store)
        listview.show_all()
        listview.expand_all()
        
    def ClearColumns(self):
        listview = self.listview
        for i in listview.get_columns():
            listview.remove_column(i)
        listview.set_model()
        
    def OnListViewOnActivated(self, widget, path, view_column):
        print path, view_column
        model = widget.get_model()
        iter = model.get_iter(path)
        print model.get_value(iter, 0)
        
        
if __name__ == '__main__':
    TestDlg()
    gtk.main()