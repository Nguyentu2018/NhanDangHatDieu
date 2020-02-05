import sqlite3

conn = sqlite3.connect("data2.db")
c = conn.cursor()

# tao mot table moi neu no chua co trong data
def create_table(name):
    name = name.replace(' ', '_')
    c.execute("""CREATE TABLE IF NOT EXISTS """ + name + """(
                uh INTEGER,
                us INTEGER,
                uv INTEGER,
                lh INTEGER,
                ls INTEGER,
                lv INTEGER)""")

# nhap lieu vao table trong data
def data_entry(name, data):
    name = name.replace(' ', '_')
    c.execute('INSERT INTO ' + name + ' VALUES(?, ?, ?, ?, ?, ?)',
              (data))
    # save
    # conn.commit()

def read_from_db(name):
    name = name.replace(' ', '_')
    c.execute('SELECT * FROM ' + name)
    data = c.fetchall()
    return data

def del_and_update(name):
    name = name.replace(' ', '_')
    # c.execute("""UPDATE """ + name + """ SET px = 0, pz = 0 WHERE py = 200""")
    # c.execute("SELECT * FROM " + name)
    # [print(row) for row in c.fetchall()]
    # conn.commit()
    sql = 'DROP TABLE IF EXISTS ' + name
    c.execute(sql)
    conn.commit()
    # c.execute("SELECT * FROM " + name)
    # [print(row) for row in c.fetchall()]

def get_all_nameTableDB():
    sql = "SELECT name FROM sqlite_master WHERE type='table'"
    c.execute(sql)
    name = c.fetchall()
    namepg = []
    for i in range(len(name)):
        namepg.append(name[i][0])
    # print(namepg)
    return namepg

# name = "ct3"
# data = [0, 0, 0, 0, 'p', 15]
# read_from_db(name)
# create_table(name)
# data_entry(name, data)
# get_all_nameTableDB()
# c.close()
# conn.close()