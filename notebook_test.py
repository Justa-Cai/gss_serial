import gtk

class TestDlg(gtk.Window):
    def __init__(self):
        super(TestDlg, self).__init__()
        self.set_size_request(600, 480)
        self.set_position(gtk.WIN_POS_CENTER)
        self.connect("destroy", gtk.main_quit)
        vbox = gtk.VBox()
        notebook = gtk.Notebook()
       
        tab = gtk.ScrolledWindow()
        tab.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        notebook.append_page(tab, gtk.Label('Serial'))
        
        tab = gtk.ScrolledWindow()
        tab.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        notebook.append_page(tab, gtk.Label('Serial1'))
        notebook.set_scrollable(True)
        
        #notebook.append_page()
        vbox.add(notebook)
        self.add(vbox)
        
        self.show_all()
        
        
if __name__ == '__main__':
    TestDlg()
    gtk.main()