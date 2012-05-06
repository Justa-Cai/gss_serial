import sqlite3
conn = sqlite3.connect('/tmp/test.db')
c = conn.cursor()
c.execute('''DROP TABLE DATA''')
c.execute('''CREATE TABLE IF NOT EXISTS DATA (Name TEXT, Caption TEXT, QuickText TEXT )''')
purchases = [('83', 'Caption', 'QuickText'),
             ('83', 'Caption', 'QuickText1'),
             ('83', 'Caption', 'QuickText1'),
             ('83', 'Caption', 'QuickText1'),
             ('83', 'Caption', 'QuickText1'),
             ('84', 'Caption', 'QuickText1'),
             ('84', 'Caption', 'QuickText1'),
             ('84', 'Caption', 'QuickText1'),
             ('84', 'Caption', 'QuickText1'),
             ('84', 'Caption', 'QuickText1'),
             ('84', 'Caption', 'QuickText1'),
             ('85', 'CaptionX', 'QuickText2'),
             ('85', 'CaptionX', 'QuickText2'),
             ('85', 'CaptionX', 'QuickText2'),
             ('85', 'CaptionX', 'QuickText2'),
             ('85', 'CaptionX', 'QuickText2'),
             ('85', 'CaptionX', 'QuickText2'),
             ]
c.executemany('INSERT INTO DATA VALUES(?,?,?)', purchases)
conn.commit()
c.execute("""SELECT Caption,QuickText FROM DATA WHERE Name='83'""")
print c.fetchall()
c.close()