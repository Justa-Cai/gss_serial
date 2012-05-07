""" 
data store class

Reference:
- pysqlite
  http://docs.python.org/library/sqlite3.html

"""


import sqlite3
import os
from serial import Serial
data_utils = None

def GetDataUtils():
    global data_utils
    if data_utils==None:
        data_utils = DataUtils()
    return  data_utils

class DataUtils:
    def __init__(self, path=None):
        if path == None:
            path = os.path.expanduser('~/.gss_serial/config.db')
        self.db_connect = db_connect = sqlite3.connect(path)
        c = db_connect.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS DATA (id INTEGER PRIMARY KEY, pos INTEGER, Name TEXT, Caption TEXT, QuickText TEXT) ''')
        c.execute('''CREATE TABLE IF NOT EXISTS CONFIG (COMBOX_POS INTEGER) ''')
        c.execute('''CREATE TABLE IF NOT EXISTS HISTORY (id INTEGER PRIMARY KEY, TYPE TEXT, HOST_OR_PORT TEXT, USER_OR_BAURATE TEXT) ''')
        
        c.execute('SELECT Name FROM DATA')
        if len(c.fetchall()) == 0:
            c.execute('INSERT INTO CONFIG VALUES(0)')
            c.execute(''' INSERT INTO DATA VALUES(NULL, 0, "defaults", "1", "21") ''')
            c.execute(''' INSERT INTO DATA VALUES(NULL, 0, "defaults", "12", "22") ''')
            c.execute(''' INSERT INTO DATA VALUES(NULL, 0, "defaults", "13", "23") ''')
            c.execute(''' INSERT INTO DATA VALUES(NULL, 1, "defaultsX", "14", "24") ''')
            c.execute(''' INSERT INTO DATA VALUES(NULL, 1, "defaultsX", "1", "25") ''')
            c.execute(''' INSERT INTO DATA VALUES(NULL, 1, "defaultsX", "1", "26") ''')
            db_connect.commit()
            
        
        c.close()
    
    def __del__(self):
        self.db_connect.commit()
        pass

    def GetConnect(self):    
        return self.db_connect
    
    """
    1 history
    2 bottom quick input bar
    """
    def GetBottomToolbarConfig(self):
        pass
    
class GSS_Serial(Serial):
    def __init__(self, port, baudrate):
        super(GSS_Serial, self).__init__(port=port, baudrate=baudrate)
        self.__map={}
        
    def set_data(self, key, val):
        self.__map[key] = val
        
    def get_data(self, key):
        return self.__map[key]
    
if __name__ == '__main__':
    utils = GetDataUtils()
    conn = utils.GetConnect()
    c = conn.cursor()
    
    c.execute('DROP TABLE DATA')
    
    c.execute('SELECT COMBOX_POS FROM CONFIG')
    print c.fetchall()
    
    c.execute('UPDATE CONFIG SET COMBOX_POS=(?)', str(1))
    
    c.execute('SELECT COMBOX_POS FROM CONFIG')
    print c.fetchall()
    
    c.execute('SELECT * FROM DATA')
    print c.fetchall()
    
    c.close()
    conn.commit()
    
    
    
    
    
    
    