import md5
import connection
import sqlite3
import config


def auth(user,password):
        key = read_key()
        try:
                hash = md5.new(password)
                if (user == key[0]) and (hash.hexdigest() == key[1]):
                        return True
        except TypeError:
                return False
        return False

def read_key():
        conn = connection.connectDB(config.DB_path)
        c = conn.cursor()
        c.execute("select * from auth")
        list = c.fetchone()
        if list == None:
                list = createKey("admin","admin")
                c.execute("insert into auth values(?,?) ",list)
                conn.commit()
        c.close() 
        return list

def createKey(username,password):
        list = []
        if(len(username) == 0 or len(password) == 0):
                return list
        pashash = md5.new()
        pashash.update(password)
        password = pashash.hexdigest()
        list.append(username)
        list.append(password)
        return list

def updateKey(username,password):
        conn = connection.connectDB(config.DB_path)
        c = conn.cursor()
        list = createKey(username,password)
        c.execute("delete from auth")
        c.execute("insert into auth values(?,?) ",list)
        conn.commit()
        c.close()
