import sqlite3
def createDB():
    try:
        conn = sqlite3.connect("hasm.db")
        print("Openned Database successfully!")
        #conn.execute('''drop table Register''')
        conn.execute('''CREATE TABLE IF NOT EXISTS Register(id INTEGER PRIMARY KEY AUTOINCREMENT, firstname TEXT NOT NULL , lastname text not null, email TEXT NOT NULL , password TEXT NOT NULL)''')
        conn.execute('''CREATE  TABLE IF NOT EXISTS Cart(orderID Integer PRIMARY KEY AUTOINCREMENT , id Integer, price Integer, quantity Integer, FOREIGN KEY(id) REFERENCES Register(id))''')

        #conn.execute('''INSERT INTO users VALUES (?,?,?,?)''')
        #conn.execute('''DROP TABLE Register''')
        #conn.execute('''INSERT INTO Register(firstname, lastname, email, password) VALUES ('Mohamed', "Sheikh-ali", 'masg@ghalm', 'password')''')
        print("Table was created !!!")
        conn.commit()
        conn.close()

    except sqlite3.OperationalError as err:
        print(err)
        print("Database already exists!")
createDB()
