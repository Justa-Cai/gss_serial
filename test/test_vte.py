""" 
Test vte control (local fork and remote fork)

Reference:
- vte :
  http://developer.gnome.org/vte/0.32/VteTerminal.html

"""
import gtk
import vte #@UnresolvedImport

class TestDlg(gtk.Window):
    
    def __init__(self):
        super(TestDlg, self).__init__()
        self.set_size_request(600, 480)
        self.set_position(gtk.WIN_POS_CENTER)
        self.connect("destroy", gtk.main_quit)
        
        self.vbox = vbox = gtk.VBox()
        self.notebook = notebook = gtk.Notebook()
        
        # menu
        agr = gtk.AccelGroup()
        self.add_accel_group(agr)
        
        mb = gtk.MenuBar()
        menu = gtk.Menu()
        menufile = gtk.MenuItem('_File')
        menufile.set_submenu(menu)
        
        menuitem = gtk.MenuItem('_Quit')
        key, mod = gtk.accelerator_parse("<Control>W")
        menuitem.add_accelerator("activate", agr, key, mod, gtk.ACCEL_VISIBLE)
        menuitem.connect('activate', gtk.main_quit)
        menu.append(menuitem)
        
        menuitem = gtk.MenuItem('_Local Command')
        menuitem.connect('activate', self.CreateLocalTerminal)
        menu.append(menuitem)
        
        menuitem = gtk.MenuItem('_Remote ssh Command')
        menuitem.connect('activate', self.CreateSshTerminal)
        menu.append(menuitem)
        
        mb.append(menufile)
        
        #notebook.append_page()
        vbox.pack_start(mb, False, False)
        vbox.add(notebook)
        self.add(vbox)
        self.show_all()
        
    def CreateLocalTerminal(self, event):
        term = vte.Terminal()
        term.fork_command()
        self.CreateTab(term)
    
    def CreateSshTerminal(self, event):
        term = vte.Terminal()
        cmd = [ 'ssh', '127.0.0.1 -l star']
        term.fork_command(cmd[0], cmd)
        self.CreateTab(term)
            
    def CreateTab(self, widget):
        notebook = self.notebook
        tab = widget
        hbox = gtk.HBox()
        hbox.pack_start(gtk.Label("Serial"), True, True)
        
        close = gtk.Button()
        close.set_focus_on_click(False)
        close.set_relief(gtk.RELIEF_NONE)
        close.set_name('tab-close')
        close.connect('clicked', self.OnCloseTab)
        img = gtk.Image()
        img.set_from_stock(gtk.STOCK_CLOSE, gtk.ICON_SIZE_MENU)
        close.add(img)
        hbox.pack_start(close,False, False)
        hbox.show_all()
        
        i = notebook.append_page(tab, hbox)
        notebook.set_tab_label_packing(tab, True, True, gtk.PACK_START)
        self.notebook.show_all()
        self.notebook.set_current_page(i)
      
    def OnCloseTab(self, widet):
        notebook = self.notebook
        notebook.remove_page(notebook.get_current_page())
       
if __name__ == '__main__':
    TestDlg()
    gtk.main()